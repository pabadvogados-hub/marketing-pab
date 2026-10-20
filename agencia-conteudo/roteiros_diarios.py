"""
Agencia de Conteudo — 5 roteiros por dia, um por persona, entregues 06:00 BRT.

FLUXO DIARIO (--cron):
  1. tenta GERAR os roteiros do dia pela Claude API;
  2. se a API falhar (ex.: sem credito), cai no BANCO de roteiros pre-escritos
     e manda o proximo lote ainda nao enviado;
  3. envia os 5 por WhatsApp (Z-API, numero do SISTEMA_PAB);
  4. registra o que foi enviado e avisa quando o banco esta acabando.

Nunca falha calado: qualquer problema vira alerta no WhatsApp de controle.

Uso:
  py AGENCIA_CONTEUDO/roteiros_diarios.py                 # DRY-RUN (mostra, nao envia)
  py AGENCIA_CONTEUDO/roteiros_diarios.py --enviar        # gera pela API e envia
  py AGENCIA_CONTEUDO/roteiros_diarios.py --cron          # fluxo diario completo (crontab)
  py AGENCIA_CONTEUDO/roteiros_diarios.py --banco         # so mostra o estado do banco
  py AGENCIA_CONTEUDO/roteiros_diarios.py --de-arquivo x.json --enviar

Crontab (VPS, 06:00 BRT):
  0 6 * * * cd /opt/pab && /opt/pab/venv/bin/python \
    /opt/pab/AGENCIA_CONTEUDO/roteiros_diarios.py --cron >> /var/log/pab-roteiros.log 2>&1
"""
import os
import sys
import json
import time
import sqlite3
import argparse
import traceback
from pathlib import Path
from datetime import date, datetime

import requests

ROOT = Path(__file__).resolve().parents[1]
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "config" / ".env")
except Exception:
    pass

DB_PATH = os.getenv("PAB_DB") or str(ROOT / "SISTEMA_PAB" / "backend" / "sistema_pab.db")
DESTINO_PADRAO = os.getenv("ROTEIROS_DESTINO", "5511900000000")
WA_NUMERO_ID = int(os.getenv("ROTEIROS_WA_NUMERO_ID", "1"))
MODELO = os.getenv("ROTEIROS_MODELO", "claude-opus-5")

# Para onde vai o alerta quando algo da errado (padrao: o proprio numero do escritorio)
ALERTA = os.getenv("ROTEIROS_ALERTA", "5511900000000")

BANCO = AQUI / "banco_roteiros.json"     # lotes pre-escritos
ESTADO = AQUI / "estado.json"            # o que ja foi enviado
AVISA_BANCO_BAIXO = 2                    # avisa quando sobram N lotes ou menos


def log(msg):
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


# ============================================================
# PERSONAS — o "DNA de estilo" de cada uma
# ============================================================

PERSONAS = [
    {"chave": "tate", "nome": "Andrew Tate", "estilo": "dominancia e disciplina",
     "dna": ("Direto, confrontador, sem suavizar. Fala com o espectador como quem cobra, nao como "
             "quem pede. Frases curtas e afirmativas. Contrapoe fraqueza x forca, decisao x desculpa. "
             "Nunca pede desculpas pela opiniao. Sem palavrao. O recorte e disciplina e execucao — "
             "nada sobre mulheres, relacionamento ou dinheiro facil.")},
    {"chave": "hormozi", "nome": "Alex Hormozi", "estilo": "oferta e valor",
     "dna": ("Analitico e pratico. Ensina um mecanismo com nome e partes numeradas. Numeros concretos. "
             "Sem motivacao vazia: e sempre 'aqui esta a estrutura, aplica hoje'. Frases declarativas, "
             "zero floreio. Inverte a crenca do espectador logo no inicio.")},
    {"chave": "polemico", "nome": "Ryan", "estilo": "contrarian / polemico",
     "dna": ("Ataca um consenso que todo mundo repete e mostra por que ele custa caro. Provocativo mas "
             "argumentado — nunca polemica gratuita. Termina puxando o espectador pro debate.")},
    {"chave": "robbins", "nome": "Tony Robbins", "estilo": "PNL e estado emocional",
     "dna": ("Energia alta, corpo em movimento, segunda pessoa o tempo todo. Ensina que o estado "
             "fisiologico vem antes do pensamento. Sempre da um exercicio pra pessoa fazer AGORA, "
             "dentro do video. Usa perguntas diretas.")},
    {"chave": "rohn", "nome": "Jim Rohn", "estilo": "sabedoria e aforismo",
     "dna": ("Ritmo lento e pausado. Constroi em cima de um aforismo central e desdobra em consequencia "
             "de longo prazo. Fala de ambiente, escolhas pequenas e acumulo. Tom de mentor mais velho. "
             "Frases que dao vontade de anotar.")},
]

SUBNICHOS = ["negocios e vendas", "mentalidade e crencas", "produtividade e foco",
             "storytelling e comunicacao", "disciplina e habitos"]

SCHEMA = {
    "type": "object",
    "properties": {
        "roteiros": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "persona": {"type": "string"}, "tema": {"type": "string"},
                    "gancho": {"type": "string"}, "corpo": {"type": "string"},
                    "cta": {"type": "string"},
                },
                "required": ["persona", "tema", "gancho", "corpo", "cta"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["roteiros"],
    "additionalProperties": False,
}

SYSTEM = """Voce e o roteirista de uma agencia de conteudo que produz videos verticais curtos
(Instagram Reels, TikTok, YouTube Shorts, Facebook) para UMA pessoa gravar de cara propria.

Regras inegociaveis:
1. Quem grava e o proprio criador, falando em primeira pessoa. Voce escreve NO ESTILO de cada
   referencia — nunca fingindo SER aquela pessoa e nunca citando a biografia dela.
2. NUNCA invente numeros, faturamento, historia pessoal ou resultado do criador. Quando o roteiro
   pedir um dado pessoal, escreva um marcador entre colchetes, ex: [X meses], [seu numero real].
3. Portugues do Brasil, oral, do jeito que se fala — nao do jeito que se escreve.
4. O gancho tem que segurar nos 3 primeiros segundos: uma afirmacao que gera tensao, nunca
   "fala galera" nem apresentacao.
5. O corpo entrega UMA ideia so, bem desenvolvida, com uma virada no meio. 45 a 70 segundos de fala.
6. O CTA e especifico e da um motivo pra agir (comentar uma palavra, salvar, marcar alguem).
7. Sem emoji, sem hashtag, sem markdown no texto do roteiro."""


def _prompt_do_dia(dia: date) -> str:
    idx = dia.toordinal()
    linhas = [
        f"- {p['nome']} (estilo: {p['estilo']}) | tema de hoje: {SUBNICHOS[(idx + i) % len(SUBNICHOS)]}\n"
        f"  DNA do estilo: {p['dna']}"
        for i, p in enumerate(PERSONAS)
    ]
    return (
        f"Data: {dia.strftime('%d/%m/%Y')}.\n\n"
        "Escreva 1 roteiro para cada uma das 5 personas abaixo, cada uma no tema indicado.\n"
        "Os temas conversam entre si (fazem parte da mesma marca), mas cada roteiro e independente.\n\n"
        + "\n".join(linhas)
        + "\n\nPara cada roteiro devolva: persona (APENAS o nome, ex: \"Andrew Tate\" — sem o estilo "
        "entre parenteses), tema, gancho (1-2 frases, os 3 primeiros segundos), "
        "corpo (o desenvolvimento completo, 45-70s de fala) e cta (1 frase).\n"
        "Os 5 roteiros de hoje devem ser diferentes entre si em estrutura, nao so em assunto."
    )


# ============================================================
# GERACAO (API)
# ============================================================

def gerar_roteiros(dia=None) -> list[dict]:
    import anthropic
    dia = dia or date.today()
    client = anthropic.Anthropic()
    with client.messages.stream(
        model=MODELO, max_tokens=20000, system=SYSTEM,
        output_config={"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": _prompt_do_dia(dia)}],
    ) as stream:
        msg = stream.get_final_message()
    if msg.stop_reason == "refusal":
        raise RuntimeError("geracao recusada pelo modelo")
    texto = next(b.text for b in msg.content if b.type == "text")
    return json.loads(texto)["roteiros"]


# ============================================================
# BANCO de roteiros pre-escritos (fallback quando a API nao roda)
# ============================================================

def _ler_json(p: Path, padrao):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return padrao


def estado_banco() -> dict:
    banco = _ler_json(BANCO, {"lotes": []})
    estado = _ler_json(ESTADO, {"enviados": []})
    enviados = set(estado.get("enviados", []))
    pendentes = [l for l in banco.get("lotes", []) if l.get("id") not in enviados]
    return {"total": len(banco.get("lotes", [])), "enviados": len(enviados),
            "pendentes": pendentes, "restam": len(pendentes)}


def marcar_enviado(lote_id: str):
    estado = _ler_json(ESTADO, {"enviados": []})
    estado.setdefault("enviados", []).append(lote_id)
    estado["ultimo_envio"] = datetime.now().isoformat(timespec="seconds")
    ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=2), encoding="utf-8")


# ============================================================
# ENVIO (Z-API, credenciais do SISTEMA_PAB)
# ============================================================

def _credenciais_zapi(numero_id: int = WA_NUMERO_ID) -> dict:
    if not Path(DB_PATH).exists():
        raise RuntimeError(f"banco do SISTEMA_PAB nao encontrado em {DB_PATH}")
    con = sqlite3.connect(DB_PATH)
    try:
        row = con.execute(
            "SELECT nome, zapi_instance, zapi_token, zapi_client_token "
            "FROM wa_numeros WHERE id = ? AND ativo = 1", (numero_id,)).fetchone()
    finally:
        con.close()
    if not row or not row[1]:
        raise RuntimeError(f"numero id={numero_id} sem credencial Z-API no banco")
    return {"nome": row[0], "instance": row[1], "token": row[2], "client_token": row[3]}


def enviar_whatsapp(telefone: str, mensagem: str, cred: dict) -> tuple[bool, str]:
    url = f"https://api.z-api.io/instances/{cred['instance']}/token/{cred['token']}/send-text"
    headers = {"Content-Type": "application/json"}
    if cred.get("client_token"):
        headers["Client-Token"] = cred["client_token"]
    try:
        r = requests.post(url, json={"phone": telefone, "message": mensagem},
                          headers=headers, timeout=30)
        if r.status_code in (200, 201):
            return True, (r.json().get("messageId") or "")
        return False, r.text[:300]
    except Exception as e:
        return False, str(e)


def alertar(texto: str):
    """Manda um aviso pro numero de controle. Nunca deixa o cron morrer calado."""
    try:
        cred = _credenciais_zapi()
        enviar_whatsapp(ALERTA, f"*AGENCIA DE CONTEUDO — AVISO*\n\n{texto}", cred)
    except Exception as e:
        log(f"NAO CONSEGUIU ALERTAR: {e}")


def formatar(r: dict, dia: date) -> str:
    return (f"*ROTEIRO {dia.strftime('%d/%m')} — {r['persona'].upper()}*\n"
            f"_{r['tema']}_\n\n"
            f"*GANCHO (0-3s)*\n{r['gancho']}\n\n"
            f"*CORPO*\n{r['corpo']}\n\n"
            f"*CTA*\n{r['cta']}")


def despachar(roteiros: list[dict], destino: str, dia: date) -> int:
    cred = _credenciais_zapi()
    log(f"enviando por {cred['nome']} -> {destino}")
    ok = 0
    for i, r in enumerate(roteiros, 1):
        sucesso, info = enviar_whatsapp(destino, formatar(r, dia), cred)
        log(f"  {i}/{len(roteiros)} {r['persona']}: {'OK' if sucesso else 'FALHOU ' + info}")
        ok += bool(sucesso)
        if i < len(roteiros):
            time.sleep(3)
    return ok


# ============================================================
# FLUXO DIARIO
# ============================================================

def rodar_cron(destino: str):
    dia = date.today()
    log(f"=== roteiros de {dia:%d/%m/%Y} ===")
    roteiros, origem, lote_id = None, "", None

    # 1) tenta gerar pela API
    try:
        roteiros = gerar_roteiros(dia)
        origem = f"gerado pela API ({MODELO})"
    except Exception as e:
        log(f"API indisponivel ({str(e)[:120]}) — caindo no banco de roteiros")

    # 2) fallback: banco pre-escrito
    if not roteiros:
        st = estado_banco()
        if not st["pendentes"]:
            msg = (f"O banco de roteiros ACABOU e a API esta indisponivel.\n"
                   f"Nenhum roteiro foi enviado hoje ({dia:%d/%m}).\n\n"
                   f"Para voltar a rodar: repor credito na API da Anthropic "
                   f"ou adicionar novos lotes em banco_roteiros.json.")
            log("BANCO VAZIO — nada enviado")
            alertar(msg)
            return 1
        lote = st["pendentes"][0]
        roteiros, lote_id = lote["roteiros"], lote["id"]
        origem = f"banco ({lote_id}, restavam {st['restam']})"

    log(f"origem: {origem}")

    # 3) envia
    try:
        ok = despachar(roteiros, destino, dia)
    except Exception as e:
        log(f"ERRO NO ENVIO: {e}")
        alertar(f"Falha ao enviar os roteiros de {dia:%d/%m}:\n{str(e)[:250]}")
        return 1

    if ok == 0:
        alertar(f"Nenhum dos {len(roteiros)} roteiros de {dia:%d/%m} foi entregue. "
                f"Conferir a instancia Z-API.")
        return 1

    if lote_id:
        marcar_enviado(lote_id)
        restam = estado_banco()["restam"]
        log(f"lote {lote_id} marcado como enviado; restam {restam}")
        if restam <= AVISA_BANCO_BAIXO:
            alertar(f"O banco de roteiros esta acabando: restam *{restam} dia(s)*.\n"
                    f"Repor credito na API da Anthropic ou adicionar novos lotes.")

    log(f"OK — {ok}/{len(roteiros)} entregues ({origem})")
    return 0


# ============================================================
# CLI
# ============================================================

def main():
    p = argparse.ArgumentParser(description="Agencia de conteudo — roteiros diarios.")
    p.add_argument("--cron", action="store_true", help="fluxo diario completo (API -> banco -> envia)")
    p.add_argument("--enviar", action="store_true", help="envia de verdade (sem isso e DRY-RUN)")
    p.add_argument("--para", default=DESTINO_PADRAO, help="telefone destino (55DDDNUMERO)")
    p.add_argument("--banco", action="store_true", help="mostra o estado do banco e sai")
    p.add_argument("--de-arquivo", dest="de_arquivo", help="usa roteiros prontos de um .json")
    p.add_argument("--salvar", help="salva os roteiros num .txt")
    args = p.parse_args()

    if args.banco:
        st = estado_banco()
        print(f"lotes no banco : {st['total']}")
        print(f"ja enviados    : {st['enviados']}")
        print(f"restam         : {st['restam']}")
        for l in st["pendentes"][:10]:
            print(f"  - {l['id']}: " + ", ".join(r["persona"] for r in l["roteiros"]))
        return 0

    if args.cron:
        try:
            return rodar_cron(args.para)
        except Exception:
            log("ERRO INESPERADO:\n" + traceback.format_exc())
            alertar("Erro inesperado no envio dos roteiros. Conferir /var/log/pab-roteiros.log")
            return 1

    dia = date.today()
    if args.de_arquivo:
        roteiros = json.loads(Path(args.de_arquivo).read_text(encoding="utf-8"))["roteiros"]
        print(f"{len(roteiros)} roteiros carregados de {args.de_arquivo}\n")
    else:
        print(f"Gerando os 5 roteiros de {dia:%d/%m/%Y} ({MODELO})...\n")
        roteiros = gerar_roteiros(dia)

    mensagens = [formatar(r, dia) for r in roteiros]
    if args.salvar:
        Path(args.salvar).write_text(("\n\n" + "=" * 70 + "\n\n").join(mensagens), encoding="utf-8")
        print(f"Salvo em {args.salvar}")

    if not args.enviar:
        for m in mensagens:
            print(m + "\n" + "-" * 70 + "\n")
        print(f"[DRY-RUN] {len(mensagens)} roteiros. Use --enviar para mandar.")
        return 0

    ok = despachar(roteiros, args.para, dia)
    print(f"\n{ok}/{len(roteiros)} enviados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

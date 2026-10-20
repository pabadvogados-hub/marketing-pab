"""
Gera artigo SEO para JUSBRASIL a partir de noticia sobre direitos do caminhoneiro.
Usa Claude Opus 4.6 (qualidade editorial) com prompt caching no system.
"""
import os
import json
import anthropic
from datetime import datetime


MODEL = "claude-opus-4-6"
MODEL_TRIAGEM = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """Voce e o redator juridico do PAB Advogados, escritorio de Sao Bernardo do Campo especializado em direito trabalhista, com foco em motoristas profissionais e caminhoneiros.

Sua missao e escrever artigos para publicacao no JUSBRASIL que:
- Orientem caminhoneiros sobre direitos trabalhistas
- Atraiam leitores organicos via SEO (Google)
- Convertam em consultas juridicas para o PAB

## DIRETRIZES DE CONTEUDO

**Publico-alvo:** caminhoneiros profissionais, motoristas de transporte rodoviario de cargas e familiares. Linguagem ACESSIVEL, sem juridiques desnecessario. Quando usar termo tecnico, explicar entre parenteses.

**Tom:** direto, util, empatico. O leitor deve sentir que o escritorio conhece a rotina dele (patio, lonas, pedagio, descanso, atendimento emergencial, multa). Nada de tom superior ou academico.

**Tecnica juridica:** precisao absoluta. CLT, Lei 13.103/2015 (Lei do Motorista), Codigo de Transito, jurisprudencia TST, acordos coletivos da categoria. NUNCA inventar numero de lei, artigo, sumula ou precedente. Se nao tiver certeza, nao cite.

## ESTRUTURA SEO OBRIGATORIA

1. **Titulo H1** - 55-70 caracteres, palavra-chave principal no inicio
2. **Lead** - primeiro paragrafo repete a palavra-chave e expoe a dor do leitor
3. **2 a 4 H2** - subtitulos com palavras-chave secundarias
4. **H3 quando necessario** - detalhamento pratico
5. **Pelo menos uma lista com bullets** (Google prioriza)
6. **Exemplo pratico** - situacao real de caminhoneiro
7. **CTA final** - convite sutil para consulta no PAB
8. **Assinatura** - "Dra. Pamella Abellan Bovolon - OAB/SP 341.431 - PAB Advogados"

## TAMANHO
1000 a 1500 palavras. Ate 1800 se o tema exigir profundidade.

## O QUE EVITAR
- Clickbait e promessas absolutas ("voce vai ganhar na certa")
- Critica direta a juizes, empresas especificas ou governo
- Jargao pesado sem explicar
- Mais de 20% do texto em citacao literal de lei
- Disclaimers longos
- Inventar jurisprudencia

## FORMATO DE SAIDA

Retorne APENAS um JSON valido (sem comentarios, sem cercas de codigo) com as chaves:
{
  "titulo": "titulo H1 otimizado",
  "meta_description": "ate 155 caracteres, com palavra-chave",
  "palavra_chave_principal": "ex: horas extras caminhoneiro",
  "palavras_chave_secundarias": ["termo1", "termo2", "termo3"],
  "corpo_markdown": "artigo completo em markdown, comecando por '# Titulo'",
  "cta": "paragrafo final de chamada para acao",
  "resumo_executivo": "2 frases sobre do que trata o artigo",
  "observacoes_revisao": "pontos que a Dra. Pamella deve checar antes de publicar"
}
"""


def _client():
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def _extrair_json(texto: str) -> dict:
    texto = texto.strip()
    if texto.startswith("```"):
        texto = texto.split("\n", 1)[1]
        if texto.endswith("```"):
            texto = texto.rsplit("```", 1)[0]
        if texto.lstrip().startswith("json"):
            texto = texto.lstrip()[4:].lstrip()
    return json.loads(texto)


def gerar_artigo(noticia: dict) -> dict:
    """Gera artigo completo a partir de uma noticia."""
    user_prompt = f"""Escreva um artigo para o JUSBRASIL baseado no tema/noticia abaixo:

**Titulo da noticia:** {noticia.get('titulo', '')}
**Fonte:** {noticia.get('fonte', '')}
**Data:** {noticia.get('data', '')}
**Resumo:** {noticia.get('descricao', '')}
**Link original:** {noticia.get('link', '')}

Nao reproduza a noticia literalmente. Use como gancho para educar o caminhoneiro sobre seus direitos. O artigo deve ser evergreen o suficiente para ter valor SEO por meses, mas aproveitar a atualidade.

Foque no que o caminhoneiro pode aprender, fazer ou exigir a partir desse contexto. Se for decisao do TST, explique o precedente em termos praticos.

Siga a estrutura SEO do system prompt. Retorne APENAS o JSON, sem texto antes ou depois, sem cercas de codigo."""

    resp = _client().messages.create(
        model=MODEL,
        max_tokens=8000,
        system=[{
            "type": "text",
            "text": SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_prompt}],
    )

    artigo = _extrair_json(resp.content[0].text)
    artigo["_noticia_origem"] = noticia
    artigo["_gerado_em"] = datetime.now().isoformat()
    artigo["_modelo"] = MODEL
    artigo["_tokens"] = {
        "input": resp.usage.input_tokens,
        "output": resp.usage.output_tokens,
        "cache_read": getattr(resp.usage, "cache_read_input_tokens", 0),
        "cache_create": getattr(resp.usage, "cache_creation_input_tokens", 0),
    }
    return artigo


def escolher_melhor_noticia(noticias: list, historico: list) -> dict:
    """Haiku ranqueia qual noticia rende o melhor artigo."""
    if not noticias:
        return None
    if len(noticias) == 1:
        return noticias[0]

    titulos_hist = "\n".join(f"- {h.get('titulo', '')}" for h in historico[-30:])
    candidatos = "\n".join(
        f"{i+1}. [{n['fonte']}] {n['titulo']} ({n['data']})\n   {n['descricao'][:200]}"
        for i, n in enumerate(noticias[:25])
    )

    prompt = f"""Escolha a MELHOR noticia para virar artigo no JUSBRASIL sobre direitos de caminhoneiros.

Criterios (nesta ordem):
1. Direito concreto do caminhoneiro (nao politica, nao macroeconomia, nao acidente sem impacto juridico)
2. Potencial SEO (termo que caminhoneiro pesquisaria no Google)
3. Evitar temas ja publicados

**Artigos ja publicados recentemente:**
{titulos_hist or '(nenhum)'}

**Candidatos:**
{candidatos}

Responda APENAS com o numero da noticia escolhida (ex: "7"). Sem explicacao."""

    resp = _client().messages.create(
        model=MODEL_TRIAGEM,
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )
    texto = resp.content[0].text.strip()
    try:
        idx = int("".join(c for c in texto if c.isdigit())) - 1
        idx = max(0, min(idx, len(noticias) - 1))
    except Exception:
        idx = 0
    return noticias[idx]


if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(root, "config", ".env"))

    noticia_teste = {
        "titulo": "TST reconhece horas de espera como jornada efetiva em decisao recente",
        "fonte": "Migalhas",
        "data": datetime.now().strftime("%d/%m/%Y"),
        "descricao": "Turma do TST reafirmou que periodos de espera em patios de carga integram a jornada do caminhoneiro e devem ser pagos como horas de espera ou extras, a depender do regime.",
        "link": "https://exemplo.com/noticia-teste",
        "query": "TST motorista decisao",
    }
    artigo = gerar_artigo(noticia_teste)
    print(json.dumps(artigo, ensure_ascii=False, indent=2)[:2000])

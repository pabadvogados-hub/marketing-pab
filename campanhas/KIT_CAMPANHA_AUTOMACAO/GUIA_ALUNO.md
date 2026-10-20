# 🚀 Kit Campanha com Automação (Meta Ads) — Guia do Aluno

Este kit deixa você **criar, acompanhar e otimizar uma campanha de WhatsApp na Meta (Facebook/Instagram) por código** — do jeito que a PAB faz para os caminhoneiros. Você roda tudo no **Claude Code**, na sua máquina.

> ⚠️ **O token é SÓ SEU.** Você vai gerar o seu próprio token (Passo 1). Nunca use o de outra pessoa, nunca suba o `.env` no GitHub, nunca mande o token no WhatsApp.

---

## 📦 O que vem no kit

```
KIT_CAMPANHA_AUTOMACAO/
├── GUIA_ALUNO.md            ← este guia
├── .env.example            ← modelo de configuração (copie para .env)
├── codigo/
│   ├── meta_ads_integration.py   ← o "motor": fala com a API da Meta
│   ├── relatorio_meta.py         ← relatório da campanha no terminal
│   └── atualizar_corredor.py     ← atualiza os dados do dashboard
├── templates/
│   ├── dashboard.html            ← painel visual da campanha
│   ├── mapa_calor.html           ← mapa de calor (onde o lead é mais barato)
│   └── CAMPANHA_..._BLUEPRINT.md ← a "receita" da campanha vencedora
└── LP/
    └── calculadora_caminhoneiro.html  ← landing page (isca) — TROQUE os dados!
```

---

## ✅ Pré-requisitos (o que você precisa ter)

1. **Conta no Meta Business** (business.facebook.com) com uma **conta de anúncio**.
2. **Página do Facebook conectada a um número de WhatsApp** (é por ela que os leads chegam).
3. **Python 3** instalado, com a lib `requests` (`pip install requests`).
4. **Claude Code** rodando na pasta do projeto.

---

## 🔑 Passo 1 — Gerar o SEU token permanente (System User)

Isso acaba com o inferno de gerar token novo a cada 1-2h.

1. Entre em **business.facebook.com** → ⚙️ **Configurações do Negócio**.
2. Menu **Usuários → Usuários do Sistema** → **Adicionar** → dê um nome (ex: `automacao-ads`) → tipo **Admin**.
3. Clique no usuário criado → **Adicionar ativos** → selecione sua **conta de anúncio** e sua **página** → marque **Controle total**.
4. Clique em **Gerar novo token** → escolha seu **App** (se não tiver, crie um grátis em developers.facebook.com → "Criar app" → tipo *Empresa*).
5. Marque as permissões: `ads_management`, `ads_read`, `business_management`, `pages_read_engagement`, `pages_manage_ads`, `leads_retrieval`.
6. **Copie o token** (é uma linha longa começando com `EAA...`). **Esse é o token permanente.**

> 💡 Anote também o **ID da conta de anúncio** (`act_...`) e o **App ID** — você usa no próximo passo.

---

## ⚙️ Passo 2 — Configurar o `.env`

1. Copie o arquivo `.env.example` para `.env` (sem o `.example`).
2. Cole o seu token em `META_ADS_TOKEN`, sua conta em `META_AD_ACCOUNT` e o App ID em `META_APP_ID`.
3. **Confirme que `.env` está no `.gitignore`** (nunca versione segredo).

---

## 🧪 Passo 3 — Testar a conexão

No terminal, dentro da pasta `codigo/`:

```
python meta_ads_integration.py
```

Se aparecer `Token presente: True` e a lista das suas contas → **funcionou.** 🎉

---

## 📣 Passo 4 — Criar a campanha (a receita vencedora)

A "receita" está em `templates/CAMPANHA_..._BLUEPRINT.md`: objetivo **Engajamento → mensagens no WhatsApp (CTWA)**, orçamento por conjunto (ABO), 1 território por conjunto, criativo em vídeo + CTA "Enviar mensagem".

Você tem 2 caminhos:

**A) Pelo Gerenciador de Anúncios (mais simples):** siga o blueprint clicando na interface.

**B) Por código, com o Claude Code (o jeito PAB):** cole este pedido no seu Claude Code:

> *"Use o módulo `meta_ads_integration.py` e a receita em `CAMPANHA_..._BLUEPRINT.md` para criar na minha conta uma campanha de WhatsApp (OUTCOME_ENGAGEMENT), com 1 conjunto por cidade/região do meu nicho, orçamento R$X/dia cada, usando meu vídeo e o CTA 'Enviar mensagem'. Só ative depois de eu revisar."*

> ⚠️ A **mensagem pré-preenchida** do botão do WhatsApp (o texto que já vem escrito pro lead) **precisa ser definida no Gerenciador de Anúncios** (a API não deixa nesse tipo de campanha). Configure na aba do anúncio.

---

## 📊 Passo 5 — Acompanhar e otimizar

- **Relatório rápido no terminal:**
  ```
  python relatorio_meta.py
  ```
- **Painel visual:** abra `templates/dashboard.html` no navegador. Para atualizar os números, rode `atualizar_corredor.py` (aponte para o ID da sua campanha) e recarregue.
- **Mapa de calor** (`mapa_calor.html`): mostra onde o lead sai mais barato → é onde você escala.

Regra de ouro: **pause o que está caro, jogue verba no que está barato.** O `meta_ads_integration.py` tem `pausar()`, `ativar()` e `definir_orcamento_diario()` pra isso — peça pro Claude Code fazer.

---

## 🧲 Passo 6 — Landing Page (isca) — **TROQUE OS DADOS!**

A LP em `LP/calculadora_caminhoneiro.html` é uma **calculadora de direitos** que qualifica o lead antes dele cair no WhatsApp. É um **template** — antes de usar, **troque**:

- ☎️ **O número de WhatsApp** (hoje aponta pro escritório PAB!) — procure por `5511900000000` no arquivo e coloque o SEU.
- 🖼️ As **fotos**, o **logo**, o **nome/OAB** e o **endereço**.
- 🎨 As **cores** pra sua marca.
- 🧮 A **fórmula/os campos** do cálculo pro seu nicho (se não for caminhoneiro).

> Peça pro Claude Code: *"Adapte esta LP pra minha marca: troque o WhatsApp por [SEU NÚMERO], as fotos, o nome/OAB, o endereço e as cores."*

Para publicar de verdade (e usar nos anúncios), suba num domínio (WordPress, Vercel, Netlify).

---

## 🛑 Regras de segurança (leia!)

- **Token é individual.** Cada aluno gera o seu. Não compartilhe.
- **`.env` nunca vai pro Git.** Só o `.env.example` (sem valores).
- **Troque o WhatsApp da LP** antes de rodar, senão seus leads vão pro escritório errado.
- Antes de **pausar/ativar/mudar orçamento**, confira que está mexendo na SUA conta.

---

Dúvida? Abra o Claude Code na pasta do kit e pergunte — ele lê estes arquivos e te guia. 🚛💰

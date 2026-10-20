# 🚛 BLUEPRINT — Campanha de Caminhoneiros (replicável igualzinho)

> Cópia fiel da campanha **`AK [Whatsapp] Motoristas 26/02`** (PAB Advocacia), extraída da Meta Marketing API em **11/06/2026**.
> Tudo que está aqui é o necessário para recriar a campanha **idêntica** em qualquer conta de anúncios.
> Conta de origem: **CA01** `act_000000000000`.

---

## 📐 1. ESTRUTURA GERAL

```
CAMPANHA: AK [Whatsapp] Motoristas
│  Objetivo: Leads  |  Otimização real: Conversas no WhatsApp
│
├── CONJUNTO 1 — [MG, RS, SC, SP] Marcas Caminhão   (público principal)
├── CONJUNTO 2 — [MG, RS, SC, SP] Vídeo greve        (mesmo público, criativo greve)
├── CONJUNTO 3 — [Interno Recife] Marcas Caminhão    (teste regional PE)
│
└── Cada conjunto roda 1–2 ANÚNCIOS em vídeo, CTA "Enviar mensagem no WhatsApp"
```

Modelo testado e validado: **mesmo público + mesmos textos**, variando só o vídeo. Quem ganha leva a verba.

---

## 🎯 2. NÍVEL CAMPANHA

| Configuração | Valor |
|---|---|
| Nome | AK [Whatsapp] Motoristas |
| Objetivo | **Leads** (`OUTCOME_LEADS`) |
| Tipo de compra | Leilão (`AUCTION`) |
| Estratégia de lance | **Maior volume / menor custo** (`LOWEST_COST_WITHOUT_CAP`) |
| Categorias especiais | Nenhuma |
| Orçamento | No conjunto (ABO), não na campanha |

---

## 👥 3. NÍVEL CONJUNTO — O PÚBLICO (a parte de ouro)

> **Todos os conjuntos usam o MESMO público.** Só muda a localização no conjunto de Recife.

### Otimização e destino
| Configuração | Valor |
|---|---|
| Meta de otimização | **Conversas** (`CONVERSATIONS`) |
| Evento de cobrança | Impressões |
| Destino | **WhatsApp** |
| Número de WhatsApp | `+55 11 90000-0000` |
| Página Facebook | `000000000000` |
| Instagram | `000000000000` |
| Pixel | `000000000000` (evento LEAD) |
| Advantage+ público | **Desligado** (segmentação manual) |
| Orçamento/dia | R$ 20 a R$ 30 (por conjunto) |

### Segmentação (Detailed Targeting)
| Item | Configuração |
|---|---|
| **Idade** | 24 a 65 anos |
| **Gênero** | Todos |
| **Localização (principal)** | Estados: **Minas Gerais, Rio Grande do Sul, Santa Catarina, São Paulo** — moradores + recentes |
| **Localização (Recife/teste)** | Cidades PE: Ipojuca, Jaboatão dos Guararapes, Paulista, Cabo de Santo Agostinho (raio 17 km) |
| **Interesses (qualquer um destes)** | Commercial vehicle · Renault Trucks · Volkswagen Caminhões e Ônibus · Scania · MAN Truck & Bus · DAF · Iveco · Volvo Trucks |
| **Empregadores (work)** | Volvo Trucks |
| Filtro de conteúdo | Padrão (FACEBOOK_RELAXED) |

### IDs de interesse (pra recriar via API)
```
Commercial vehicle .................. 6003175622214
Renault Trucks ...................... 6003180019352
Volkswagen Caminhões e Ônibus ....... 6003236103085
Scania .............................. 6003286945141
MAN Truck & Bus ..................... 6003318752163
DAF ................................. 6003393157977
Iveco ............................... 6003436273370
Volvo Trucks ........................ 6003739287291
Volvo Trucks (work_employer) ........ 144246985605874
```

### Regiões (geo keys BR)
```
Minas Gerais ........ 449
Rio Grande do Sul ... 456
Santa Catarina ...... 459
São Paulo (state) ... 460
```

---

## 📣 4. NÍVEL ANÚNCIO — O CRIATIVO

| Configuração | Valor |
|---|---|
| Formato | **Vídeo** (posicionamentos automáticos / Advantage+ placements) |
| Botão (CTA) | **Enviar mensagem no WhatsApp** (`WHATSAPP_MESSAGE`) |
| Títulos testados | "Saiba Mais" / "Converse conosco" |
| Descrição | (vazia) |

### ✍️ Texto principal — VARIAÇÃO A
```
Infelizmente, os Motoristas de Caminhão são umas das classes mais injustiçadas de todo o Brasil.

Mesmo tendo uma legislação específica, a maioria das transportadoras não respeitam as regras e cometem uma série de erros trabalhistas que podem gerar indenizações milionárias a esses profissionais por motivos como:

▪️Rodar mais de 8h por dia sem receber horas extras;
▪️Ter tempo de espera contabilizado como "descanso";
▪️Carregar produtos perigosos sem receber adicional de 30%;
▪️Não ter controle de horários no diário de bordo e nem no módulo de RH do rastreador do Caminhão, e muito mais.

☝️ Se você é motorista e já enfrentou essas situações, então é direito seu ser indenizado em valores que costumam variar de R$ 50.000 a R$ 1.000.000, em alguns casos.

Quer saber mais sobre assunto e como você pode receber suas indenizações no menor tempo possível?

É só clicar em SAIBA MAIS. 🚛
```

### ✍️ Texto principal — VARIAÇÃO B
```
Você CAMINHONEIRO preste atenção !!!

Mesmo tendo uma legislação específica, a maioria das transportadoras não respeitam as regras e cometem uma série de erros trabalhistas que podem gerar indenizações milionárias a esses profissionais por motivos como:

▪️Rodar mais de 8h por dia sem receber horas extras;
▪️Ter tempo de espera contabilizado como "descanso";
▪️Carregar produtos perigosos sem receber adicional de 30%;
▪️Não ter controle de horários no diário de bordo e nem no módulo de RH do rastreador do Caminhão, e muito mais.

☝️ Se você é motorista e já enfrentou essas situações, então é direito seu ser indenizado em valores que costumam variar de R$ 50.000 a R$ 1.000.000, em alguns casos.

Quer saber mais sobre assunto e como você pode receber suas indenizações no menor tempo possível?

É só clicar em SAIBA MAIS. 🚛
```

### 💬 Mensagem de boas-vindas do WhatsApp (Click-to-WhatsApp)
| Item | Conteúdo |
|---|---|
| Saudação | "Oi! Como podemos ajudar?" |
| Resposta automática (autofill) | **"Preciso de ajuda trabalhista para caminhoneiro!"** |
| Resposta rápida (botão) | "Gostaria de obter mais informações" |

### 🎬 Vídeos usados (IDs na conta de origem)
```
Conjunto principal (campeão) ... 000000000000 · 000000000000
Conjunto Vídeo greve ........... 000000000000  · 000000000000
Conjunto Novos ads ............. 000000000000 · 000000000000
```
> ⚠️ Os arquivos de vídeo precisam ser re-upados na conta de destino (IDs de vídeo não são transferíveis entre contas). Baixar os criativos na conta de origem e subir na nova.

---

## 📊 5. RESULTADO (referência de performance)

Desde 26/02/2026 (≈3,5 meses), com ~R$ 6.500 investidos:
- **732 conversas no WhatsApp** a **R$ 8,89** cada (média)
- Últimos 30 dias: custo por conversa caiu para **R$ 7,12**
- CTR ~4,5% · CPC ~R$ 0,35 · alcance 181 mil pessoas

**Conjunto campeão:** público "Marcas Caminhão" base → R$ 6,14/conversa.

---

## 🔁 6. COMO RECRIAR IGUALZINHO (via Claude Code + Meta API)

**Pré-requisitos:** conta de anúncios (`act_...`), token com `ads_management`, página do Facebook conectada, número de WhatsApp verificado, vídeos baixados.

**Ordem de criação (3 chamadas POST encadeadas):**

1. **Criar a campanha**
```bash
curl -X POST "https://graph.facebook.com/v21.0/act_<CONTA>/campaigns" \
  -d "name=[Whatsapp] Motoristas" \
  -d "objective=OUTCOME_LEADS" \
  -d "bid_strategy=LOWEST_COST_WITHOUT_CAP" \
  -d "status=PAUSED" \
  -d "special_ad_categories=[]" \
  -d "access_token=<TOKEN>"
```

2. **Criar o conjunto** (público + WhatsApp). `targeting` e `promoted_object` em JSON:
```bash
curl -X POST "https://graph.facebook.com/v21.0/act_<CONTA>/adsets" \
  -d "name=[MG,RS,SC,SP] Marcas Caminhão" \
  -d "campaign_id=<CAMPAIGN_ID>" \
  -d "optimization_goal=CONVERSATIONS" \
  -d "billing_event=IMPRESSIONS" \
  -d "destination_type=WHATSAPP" \
  -d "daily_budget=3000" \
  -d "bid_strategy=LOWEST_COST_WITHOUT_CAP" \
  -d 'promoted_object={"page_id":"<SUA_PAGINA>","whatsapp_phone_number":"<SEU_WHATSAPP>"}' \
  -d 'targeting={"age_min":24,"age_max":65,"geo_locations":{"regions":[{"key":"449"},{"key":"456"},{"key":"459"},{"key":"460"}],"location_types":["home","recent"]},"flexible_spec":[{"interests":[{"id":"6003175622214"},{"id":"6003180019352"},{"id":"6003236103085"},{"id":"6003286945141"},{"id":"6003318752163"},{"id":"6003393157977"},{"id":"6003436273370"},{"id":"6003739287291"}],"work_employers":[{"id":"144246985605874"}]}]}' \
  -d "status=PAUSED" \
  -d "access_token=<TOKEN>"
```

3. **Criar o criativo + anúncio** (subir o vídeo antes e usar o novo `video_id`, depois criar o ad apontando para o creative). O texto, o CTA WHATSAPP_MESSAGE e a mensagem de boas-vindas vão no `object_story_spec`/`asset_feed_spec`.

> 💡 No Claude Code, o aluno só precisa colar este blueprint e pedir: *"recrie esta campanha na minha conta act_XXX"* — o agente monta as 3 chamadas com os dados dele.

---

## ✅ 7. CHECKLIST DE REPLICAÇÃO

- [ ] Token com `ads_management` gerado
- [ ] Página do Facebook + número de WhatsApp do escritório conectados
- [ ] Vídeos baixados da origem e re-upados na conta de destino
- [ ] Campanha criada (Leads / menor custo)
- [ ] Conjunto criado com o público (interesses + estados + idade 24-65)
- [ ] Destino = WhatsApp + número certo
- [ ] Anúncio com os 2 textos (A e B), CTA WhatsApp, títulos "Saiba Mais"/"Converse conosco"
- [ ] Mensagem de boas-vindas configurada
- [ ] Subir PAUSADO, revisar tudo, depois ativar

---
*Arquivo gerado automaticamente a partir da Meta Marketing API. Dados brutos completos em `_raw_campanha.json` (mesma pasta).*

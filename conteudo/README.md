# CONTEUDO - JUSBRASIL Writer

Gera artigos SEO sobre direitos de caminhoneiros 3x por semana, a partir de notícias reais, para revisão e publicação manual no JUSBRASIL.

## Fluxo

1. Busca notícias dos últimos 7 dias via Google News RSS (10 queries)
2. Haiku 4.5 ranqueia a melhor para virar artigo
3. Opus 4.6 gera artigo SEO completo (1000-1500 palavras)
4. Salva DOCX formatado no Drive
5. Notifica revisor no WhatsApp (via Atende Direito)

## Arquivos

- `buscar_noticias.py` - coleta RSS Google News
- `gerar_artigo.py` - Claude Opus 4.6 (artigo) + Haiku (triagem)
- `jusbrasil_writer.py` - orquestrador principal
- `jusbrasil_writer.bat` - trigger Task Scheduler
- `historico.json` - evita republicar mesmo tema
- `execucoes.log` - log das execuções agendadas

## Uso manual

```bash
py CONTEUDO/jusbrasil_writer.py                 # fluxo completo
py CONTEUDO/jusbrasil_writer.py --teste         # gera mas não salva no Drive
py CONTEUDO/jusbrasil_writer.py --sem-notificar # pula WhatsApp
py CONTEUDO/jusbrasil_writer.py --dias 14       # busca últimos 14 dias
```

## Configuração do .env

```
# Pasta do Drive onde salvar os DOCX (crie e cole o ID aqui)
JUSBRASIL_DRIVE_FOLDER_ID=

# Telefone do revisor (receberá WhatsApp quando sair artigo pronto)
JUSBRASIL_NOTIFICAR_TELEFONE=
```

Se `JUSBRASIL_DRIVE_FOLDER_ID` ficar vazio, usa `GOOGLE_PASTA_DESTINO` como fallback.

## Agendamento (Task Scheduler)

Crie 3 triggers apontando para `CONTEUDO\jusbrasil_writer.bat`:
- Segunda 08:00
- Quarta 08:00
- Sexta 08:00

## Após a revisão

1. Abrir o DOCX no Drive
2. Revisar o corpo (validar leis citadas, ajustar tom se preciso)
3. Apagar o bloco cinza de metadados no topo
4. Copiar o corpo e colar no editor do JUSBRASIL
5. Usar título SEO e meta description do bloco de metadados ao publicar

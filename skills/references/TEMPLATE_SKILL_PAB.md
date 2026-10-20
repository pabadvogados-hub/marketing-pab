---
name: nome-com-hifens
description: Use quando [condição de gatilho: sintomas, sinônimos, nomes de comando/ferramenta que devem disparar esta skill]. Descreva SÓ quando usar, nunca o passo a passo.
trigger: /nome-com-hifens
---

# Skill: <Título curto e claro>

<Uma frase dizendo o que a skill entrega. Sem storytelling.>

## Quando usar
- <situação/sintoma 1 — verbo no início>
- <situação/sintoma 2>
- Use esta skill em vez de <alternativa manual/genérica que se quer evitar>.

## O que essa skill faz
1. <passo objetivo>
2. <passo objetivo>
3. <passo objetivo>

## Como invocar
```python
# comando/CLI real ou snippet mínimo que roda
```
<ou: descreva o fluxo de tool-calls, se não for código.>

## Regras PAB (inegociáveis)
1. <regra de domínio — ex.: from sempre WEVERTON 147851; recuo 7cm literal; peça no timbrado>
2. <regra de compliance/permissão — ex.: nunca alterar ADVBOX/Drive sem autorização>
3. <regra de qualidade — ex.: peça vai PARA REVISÃO da Aneiry/Valentina antes de protocolar>

## Erros comuns (cilada → correção)
| Cilada | Correção |
|---|---|
| <erro que já aconteceu / tentação sob pressão> | <o que fazer no lugar> |
| <ex.: dizer "pronto" sem conferir> | <conferir contra a inicial protocolada / rodar validação> |

## Referências
- `references/<arquivo>.md` — <API longa, tabela de IDs, DNA de escrita, etc. — fora do SKILL.md>
- Memória relacionada: [[slug-da-memoria]]

<!--
Checklist antes de commitar a skill:
[ ] description começa com "Use quando" e NÃO descreve o workflow
[ ] tem seção "Erros comuns" se for skill de disciplina/qualidade
[ ] docs/API longos foram pra references/, SKILL.md ficou enxuto
[ ] regras de permissão explícitas (ADVBOX/Drive/WhatsApp)
[ ] testada 1x num caso real antes de virar padrão
-->

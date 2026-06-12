# Prompts para o Codex — Dashboard Final

Use o arquivo `contexto_codex_dashboard_entrega_final.md` como briefing base para todos os prompts abaixo.

Os prompts foram escritos para o estado atual do projeto, que já possui um dashboard em `Streamlit` com as seções `Visão Geral`, `BP`, `DRE`, `DFC`, `Indicadores` e `IPRF`.

## Prompt 1 — Diagnóstico do dashboard

Leia o arquivo `contexto_codex_dashboard_entrega_final.md` e revise o dashboard atual do projeto.

Quero que você:

1. identifique os gaps entre o estado atual do dashboard e as observações do professor;
2. mostre quais pontos já estão atendidos e quais ainda precisam de ajuste;
3. proponha um backlog técnico priorizado para a entrega final.

Considere especialmente:

- excesso de emojis
- ausência ou insuficiência de tooltips
- manutenção da compatibilidade já existente com dados até `2025`
- necessidade de funcionamento para qualquer `CNPJ`
- ortografia e acentuação
- aderência ao storytelling esperado

## Prompt 2 — Limpeza visual e revisão textual

Leia o arquivo `contexto_codex_dashboard_entrega_final.md` e revise o dashboard com foco em refinamento visual e textual.

Quero que você:

1. remova ou reduza emojis em excesso;
2. revise ortografia, acentuação e padronização dos textos visíveis;
3. preserve a identidade visual útil do dashboard;
4. mantenha o tom executivo da interface.

Revise textos em:

- `Visão Geral`
- `BP`
- `DRE`
- `DFC`
- `Indicadores`
- `IPRF`

## Prompt 3 — Tooltips e explicabilidade

Leia o arquivo `contexto_codex_dashboard_entrega_final.md` e revise o dashboard com foco em explicabilidade.

Quero que você:

1. mapeie os pontos da interface que precisam de tooltip;
2. proponha e implemente tooltips com ícone de informação;
3. inclua explicações curtas sobre regras de cálculo, contexto e interpretação;
4. mantenha as tooltips úteis para a apresentação ao vivo.

Priorize:

- KPIs da `Visão Geral`
- indicadores financeiros
- score e dimensões do `IPRF`
- filtros
- destaques de `BP`, `DRE` e `DFC`

## Prompt 4 — Compatibilidade com 2025

Leia o arquivo `contexto_codex_dashboard_entrega_final.md` e trate a atualização até `2025` como já concluída.

Quero que você:

1. revise o pipeline relacionado ao dashboard apenas para garantir que a compatibilidade com `2025` foi preservada;
2. valide mart e views da camada `gold`;
3. verifique se o dashboard continua funcionando com dados até `2025`;
4. liste qualquer quebra estrutural ou inconsistência remanescente;
5. implemente apenas ajustes corretivos, se algo tiver regredido.

Considere:

- queries
- notebooks relevantes
- mart de indicadores
- benchmark
- `IPRF`
- visualização final

## Prompt 5 — Tornar o dashboard agnóstico por CNPJ

Leia o arquivo `contexto_codex_dashboard_entrega_final.md` e adapte o dashboard para funcionar com qualquer `CNPJ`.

Quero que você:

1. identifique onde a `COSAN S.A.` está rigidamente acoplada;
2. remova o hardcode quando isso impedir seleção de outras empresas;
3. mantenha `COSAN S.A.` apenas como padrão inicial, se fizer sentido;
4. ajuste benchmark e `IPRF` para responderem à empresa selecionada;
5. preserve a estrutura atual de `Visão Geral`, `BP`, `DRE`, `DFC`, `Indicadores` e `IPRF`.

## Prompt 6 — Validação final da experiência

Leia o arquivo `contexto_codex_dashboard_entrega_final.md` e faça uma revisão final da experiência do usuário no dashboard.

Quero que você:

1. revise navegação e coerência entre telas;
2. valide se a organização sustenta bem a apresentação ao vivo;
3. identifique pontos de atrito para a banca;
4. proponha e implemente os últimos ajustes de UX necessários.

Avalie especialmente:

- fluxo entre páginas
- clareza dos filtros
- legibilidade dos gráficos e tabelas
- coerência entre `Visão Geral`, `Indicadores` e `IPRF`

## Prompt 7 — Checklist final para banca

Leia o arquivo `contexto_codex_dashboard_entrega_final.md` e monte um checklist final de validação para a apresentação.

Quero que você entregue um checklist objetivo com itens de conferência antes da banca, cobrindo:

- compatibilidade já validada com dados até `2025`
- funcionamento para qualquer `CNPJ`
- benchmark geral e setorial
- funcionamento do `IPRF`
- ortografia e acentuação
- presença de tooltips
- navegação
- performance mínima do dashboard
- estabilidade para demonstração ao vivo

O checklist deve ser direto, prático e utilizável no dia da apresentação.

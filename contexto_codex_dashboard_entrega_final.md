# Contexto para o Codex — Ajustes Finais do Dashboard

## 1. Objetivo desta etapa

A entrega final do projeto acontece em `12-06-2026`. Nesta etapa, o foco não é mais construir um MVP, e sim preparar a versão final do dashboard para avaliação em banca.

O projeto atual é um dashboard em `Streamlit` construído sobre dados públicos da CVM, com arquitetura `Bronze -> Silver -> Gold`, benchmark entre empresas e cálculo de `IPRF`.

O objetivo do Codex nesta fase é atuar como apoio técnico para revisar, ajustar e fortalecer o dashboard final, garantindo aderência às observações do professor e consistência da entrega.

## 2. Contexto atual do projeto

O projeto já possui uma camada analítica funcional e um dashboard executivo construído.

Contexto principal:

- Empresa foco atual: `COSAN S.A.`
- Base atual: dados anuais `DFP`
- Painel atual:
  - `Visão Geral`
  - `BP`
  - `DRE`
  - `DFC`
  - `Indicadores`
  - `IPRF`
- Benchmark atual:
  - mediana da base total
  - mediana do setor `Agricultura (Açúcar, Álcool e Cana)`

O projeto também já possui:

- camada `silver` com `BP`, `DRE` e `DFC`
- camada `gold` com mart de indicadores financeiros
- views de benchmark anual
- views de `IPRF`
- dashboard em `Streamlit` com leitura anual e comparativa

## 3. Observações globais do professor

As observações do professor devem ser tratadas como requisitos objetivos da entrega final.

Requisitos globais:

1. Reduzir emojis em excesso no dashboard.
2. Inserir tooltips com ícone de informação para regras de cálculo, definições e contexto adicional.
3. Considerar que a atualização do pipeline e do dashboard até os dados de `2025` já foi realizada com sucesso.
4. Tornar o dashboard agnóstico para qualquer `CNPJ` que a audiência queira escolher.
5. Revisar ortografia e acentuação de todos os textos exibidos.
6. Preparar a estrutura do dashboard para sustentar o storytelling esperado na apresentação final.

## 4. Implicações práticas para este projeto

As observações do professor impactam diretamente a implementação atual do dashboard.

### Emojis

Revisar e reduzir emojis em:

- títulos
- subtítulos
- cards
- mensagens auxiliares
- avisos e textos de status

Objetivo:

- deixar a interface mais limpa
- evitar aparência de protótipo gerado automaticamente
- manter o tom executivo do dashboard

### Tooltips

Aplicar tooltips com ícone de informação em:

- KPIs da `Visão Geral`
- indicadores financeiros
- score e dimensões do `IPRF`
- filtros de empresa e ano
- tabelas e destaques de `BP`, `DRE` e `DFC`

Objetivo:

- explicar regras de cálculo
- registrar premissas contábeis
- dar suporte à apresentação sem depender de cola externa

### Dados atualizados até 2025

O projeto já foi atualizado com dados até `2025`.

Implicação prática:

- não tratar mais `2025` como backlog de implementação
- assumir `2025` como base já disponível e validada
- preservar compatibilidade do dashboard com essa atualização já concluída

### Dashboard agnóstico por CNPJ

Remover dependências rígidas da `COSAN S.A.` onde isso impedir a seleção de outras empresas.

Regra desejada:

- `COSAN S.A.` pode continuar como empresa padrão inicial
- o dashboard deve funcionar para qualquer empresa selecionável

Isso inclui:

- filtros
- consultas
- benchmark
- comparação setorial
- páginas do `IPRF`

### Ortografia e acentuação

Revisar todos os textos visíveis ao usuário:

- nomes de abas
- títulos
- descrições
- textos auxiliares
- labels
- cabeçalhos de tabela
- mensagens de erro ou alerta

Objetivo:

- remover erros de ortografia
- corrigir acentuação
- padronizar terminologia

## 5. Requisitos funcionais para a entrega final

O dashboard final deve atender, no mínimo, aos seguintes requisitos funcionais:

1. Abrir para qualquer empresa selecionável da base.
2. Permitir que `COSAN S.A.` permaneça como empresa default inicial.
3. Permitir filtros de empresa e ano.
4. Exibir comparações por:
   - mediana da base completa
   - mediana do setor da empresa selecionada
5. Manter a navegação entre:
   - `Visão Geral`
   - `BP`
   - `DRE`
   - `DFC`
   - `Indicadores`
   - `IPRF`
6. Garantir que o `IPRF` compare a empresa selecionada com o setor correspondente.
7. Preservar o funcionamento já validado com dados até `2025`.

## 6. Requisitos não funcionais

O dashboard final também deve atender aos seguintes requisitos não funcionais:

- apresentação visual mais limpa
- menos ruído decorativo
- textos com ortografia correta
- tooltips bem posicionadas e úteis
- manutenção da coerência já validada entre dados de `2025`, camada `gold` e visualização
- interface estável para demonstração ao vivo
- experiência de navegação clara para banca e convidados

## 7. Storytelling esperado pelo professor

O professor sugeriu a seguinte lógica para a apresentação final:

1. Como o dashboard foi construído e como ele funciona.
2. Contexto do setor e da empresa escolhida.
3. Análise da série histórica da empresa, com base nos indicadores.

Essa ordem não deve ser tratada apenas como roteiro de fala. Ela também deve orientar a organização do dashboard, sua navegação e a forma como os dados são apresentados.

O dashboard final deve facilitar esse fluxo narrativo.

## 8. Instruções explícitas para o Codex

Ao trabalhar neste projeto, o Codex deve:

1. Revisar o dashboard atual.
2. Identificar gaps entre o estado atual e os requisitos desta etapa.
3. Propor um backlog técnico priorizado.
4. Implementar ajustes com foco em entrega final, e não em exploração aberta.
5. Preservar a compatibilidade já existente com dados até `2025`.
6. Priorizar clareza visual, agnosticidade por `CNPJ`, explicabilidade e consistência analítica.

Ao produzir respostas, análises ou alterações, o Codex deve assumir que este arquivo é o briefing principal da reta final do dashboard.

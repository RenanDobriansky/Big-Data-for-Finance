# Premissas Setor Agricultura Acucar Alcool e Cana

## Cabecalho

| Campo | Valor |
|---|---|
| Setor | Agricultura (Acucar, Alcool e Cana) |
| Squad | GABRIELA ANTASZCZYSZYN, MILENA JULIANE FERRAZ DE ARAUJO RODRIGUES, RENAN DOBRIANSKY DA SILVA, VICTOR HUGO MORAIS CARAFFINI |
| Data | 2026-05-21 |
| Base de dados | `layer_02_silver.n1_dfp_cia_aberta_bp`, `layer_02_silver.n1_dfp_cia_aberta_dre`, `layer_02_silver.n1_dfp_cia_aberta_dfc` |
| Escopo | Mapeamento inicial das variaveis necessarias para calcular os indicadores classicos do material `indicadores_financeiros_1.html` |
| Status | Rascunho estrutural aderente ao formato do HTML; ainda depende de validacao setorial direta na `silver` |

## Notas Gerais Obrigatorias

### N1. Caixa para indicadores: usar BP ou DFC?

| Indicador | Conta correta | Conta incorreta | Motivo |
|---|---|---|---|
| Liquidez Imediata | `1.01.01` (BP) | `6.05.02` (DFC) | O ratio e definido sobre o balanco patrimonial |
| Divida Liquida | `6.05.02` (DFC) | `1.01.01` (BP) | A DFC incorpora equivalentes de caixa e efeitos de `CPC 03` e `CPC 31` |
| Ativo Circulante Financeiro Fleuriet | `1.01.01 + 1.01.02` | `6.05.02` isolado | O modelo Fleuriet parte do balanco e nao do fluxo |

### N2. Estoques ausentes

Cobertura no setor: `A validar na silver do setor`.

Regra:
- Usar `COALESCE(estoques, 0)` apenas em `Liquidez Seca`.
- Usar `N/A` para `Giro de Estoques`, `PMRE`, `Ciclo Economico` e `Ciclo Financeiro` quando nao houver estoque reportado.
- Registrar nominalmente as empresas sem estoque na etapa de validacao setorial.

### N3. LPA: usar leaves originais da familia 3.99

Regra:
- Usar somente contas leaf da familia `3.99.*`.
- Nao usar pais reconstruidos de `3.99` como valor final de LPA.
- Estrategia provisoria do contrato: priorizar `Diluido ON` quando existir; fallback para `Basico ON`; se a empresa nao reportar a classe ON, usar a leaf mais aderente e documentar a excecao.
- Validar na `silver` do setor quantas variantes reais existem em `3.99.*`.

### N4. ST_CONTA_FIXA: como interpretar

Regra:
- `S`: conta padronizada da taxonomia CVM; preferencia maxima no contrato.
- `N`: conta livre da companhia; usar com cautela e sempre com validacao por `DS_CONTA_REPORTADA`.
- `A validar`: familia candidata ainda nao confirmada no setor.
- Variaveis derivadas ficam com `N/A`, porque nao nascem de uma unica conta bruta da CVM.

## Fichas de Variaveis

### V01. Ativo Total

| Campo | Valor |
|---|---|
| CD_CONTA | 1 |
| DS_CONTA | ATIVO TOTAL |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado; se ocorrer, tratar como anomalia critica |
| Impacto quando ausente | Invalida PCT_AT ROA e Imobilizacao do Ativo Total |
| Validacao no setor piloto | A validar contra empresa piloto do setor |
| Usado em | PCT_AT; ROA; Imobilizacao do Ativo Total |
| Atencao | Conta raiz do BP; evitar somar filhos manualmente quando o pai existir consistente |

### V02. Ativo Circulante

| Campo | Valor |
|---|---|
| CD_CONTA | 1.01 |
| DS_CONTA | ATIVO CIRCULANTE |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado; se ocorrer, tratar como anomalia critica |
| Impacto quando ausente | Invalida Liquidez Corrente Liquidez Seca Giro AC PMRAC CGL e NCG |
| Validacao no setor piloto | A validar |
| Usado em | Liquidez Corrente; Liquidez Seca; Giro AC; PMRAC; CGL; NCG |
| Atencao | Base central do modelo Fleuriet e dos indicadores de capital de giro |

### V03. Ativo Nao Circulante

| Campo | Valor |
|---|---|
| CD_CONTA | 1.02 |
| DS_CONTA | ATIVO NAO CIRCULANTE |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado |
| Impacto quando ausente | Afeta reconciliacoes do BP e suporte analitico do contrato |
| Validacao no setor piloto | A validar |
| Usado em | Apoio analitico e reconciliacoes |
| Atencao | Nao entra isoladamente nos 30 indicadores, mas ajuda a fechar o contrato do BP |

### V04. Realizavel a Longo Prazo

| Campo | Valor |
|---|---|
| CD_CONTA | 1.02.01 |
| DS_CONTA | ATIVO REALIZAVEL A LONGO PRAZO |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Possivel em empresas com estrutura mais simples; listar se ocorrer |
| Impacto quando ausente | Reduz a capacidade de calcular Liquidez Geral de forma completa |
| Validacao no setor piloto | A validar |
| Usado em | Liquidez Geral |
| Atencao | Se a conta existir apenas em filhos, aceitar familia 1.02.01.* desde que o pai esteja coerente |

### V05. Imobilizado

| Campo | Valor |
|---|---|
| CD_CONTA | 1.02.03 \| 1.02.03.* |
| DS_CONTA | IMOBILIZADO |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Pouco provavel no setor; se ocorrer, registrar como anomalia |
| Impacto quando ausente | Invalida Imobilizacao do CP e Imobilizacao do AT |
| Validacao no setor piloto | A validar |
| Usado em | Imobilizacao do CP; Imobilizacao do AT |
| Atencao | O setor tende a ser intensivo em ativo fixo; comparar cobertura e materialidade |

### V06. Estoques

| Campo | Valor |
|---|---|
| CD_CONTA | 1.01.04 \| 1.01.04.* |
| DS_CONTA | ESTOQUES |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Sim; usar 0 apenas para Liquidez Seca |
| Empresas sem a variavel | A levantar na etapa de validacao setorial |
| Impacto quando ausente | Liquidez Seca vira Liquidez Corrente; Giro de Estoques PMRE Ciclo Economico e Ciclo Financeiro ficam N_A |
| Validacao no setor piloto | A validar |
| Usado em | Liquidez Seca; Giro de Estoques; PMRE; Ciclo Economico; Ciclo Financeiro; NCG |
| Atencao | Variavel critica para o setor; se cobertura for baixa, isso vira nota geral e lista de anomalias |

### V07. Contas a Receber

| Campo | Valor |
|---|---|
| CD_CONTA | 1.01.03 \| 1.01.03.* \| 1.02.01.* com DS_CONTA aderente a clientes contas a receber duplicatas |
| DS_CONTA | CONTAS A RECEBER |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S/N a validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao; se ausente, deixar N_A para indicadores de prazo |
| Empresas sem a variavel | A levantar na etapa de validacao setorial |
| Impacto quando ausente | Invalida Giro de Contas a Receber PMRV Ciclo Economico e Ciclo Financeiro |
| Validacao no setor piloto | A validar |
| Usado em | Giro de Contas a Receber; PMRV; Ciclo Economico; Ciclo Financeiro |
| Atencao | Para os indicadores, a interpretacao-alvo e Clientes CP mais LP quando aplicavel |

### V08. Fornecedores

| Campo | Valor |
|---|---|
| CD_CONTA | 2.01.02 \| 2.01.02.* |
| DS_CONTA | FORNECEDORES |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao; se ausente, usar N_A para giro e prazo de pagamento |
| Empresas sem a variavel | A levantar na etapa de validacao setorial |
| Impacto quando ausente | Invalida Giro de Contas a Pagar PMPC e Ciclo Financeiro |
| Validacao no setor piloto | A validar |
| Usado em | Giro de Contas a Pagar; PMPC; Ciclo Financeiro |
| Atencao | Confirmar se a empresa usa FORNECEDORES puro ou filhos especificos |

### V09. Passivo Circulante

| Campo | Valor |
|---|---|
| CD_CONTA | 2.01 |
| DS_CONTA | PASSIVO CIRCULANTE |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado |
| Impacto quando ausente | Invalida Liquidez Corrente Liquidez Geral Liquidez Seca CGL NCG e Composicao do Endividamento |
| Validacao no setor piloto | A validar |
| Usado em | Liquidez Corrente; Liquidez Geral; Liquidez Seca; CGL; NCG; Composicao do Endividamento |
| Atencao | Base tambem para separar operacional versus financeiro em Fleuriet |

### V10. Passivo Nao Circulante

| Campo | Valor |
|---|---|
| CD_CONTA | 2.02 |
| DS_CONTA | PASSIVO NAO CIRCULANTE |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Possivel em estruturas muito simples; listar se ocorrer |
| Impacto quando ausente | Afeta Liquidez Geral PCT_CP PCT_AT Garantia CP_CT e Composicao do Endividamento |
| Validacao no setor piloto | A validar |
| Usado em | Liquidez Geral; PCT_CP; PCT_AT; Garantia CP_CT; Composicao do Endividamento |
| Atencao | No contrato, este campo funciona como ELP |

### V11. Patrimonio Liquido

| Campo | Valor |
|---|---|
| CD_CONTA | 2.03 |
| DS_CONTA | PATRIMONIO LIQUIDO ou PATRIMONIO LIQUIDO CONSOLIDADO |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado |
| Impacto quando ausente | Invalida PCT_CP Garantia CP_CT Imobilizacao CP ROE e Capital Investido |
| Validacao no setor piloto | A validar |
| Usado em | PCT_CP; Garantia CP_CT; Imobilizacao CP; ROE; Capital Investido; ROI |
| Atencao | PL negativo deve ser tratado como anomalia nominal no entregavel final |

### V12. Emprestimos e Financiamentos CP

| Campo | Valor |
|---|---|
| CD_CONTA | 2.01.04 \| 2.01.04.* |
| DS_CONTA | EMPRESTIMOS E FINANCIAMENTOS |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S/N a validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Sim; usar 0 em derivacoes de divida quando nao houver saldo reportado |
| Empresas sem a variavel | A levantar na etapa de validacao setorial |
| Impacto quando ausente | Afeta Divida Bruta Divida Liquida Saldo de Tesouraria e NCG por premissa de Fleuriet |
| Validacao no setor piloto | A validar |
| Usado em | Divida Bruta; Divida Liquida; Saldo de Tesouraria; Capital Investido |
| Atencao | Confirmar no setor se existem reclassificacoes financeiras fora da familia 2.01.04 |

### V13. Emprestimos e Financiamentos LP

| Campo | Valor |
|---|---|
| CD_CONTA | 2.02.01 \| 2.02.01.* |
| DS_CONTA | EMPRESTIMOS E FINANCIAMENTOS |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S/N a validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Sim; usar 0 em derivacoes de divida quando nao houver saldo reportado |
| Empresas sem a variavel | A levantar na etapa de validacao setorial |
| Impacto quando ausente | Afeta Divida Bruta Divida Liquida e Capital Investido |
| Validacao no setor piloto | A validar |
| Usado em | Divida Bruta; Divida Liquida; Capital Investido |
| Atencao | Validar se o setor tem concentracao de divida em curto prazo ou longo prazo |

### V14. Caixa e Equivalentes BP

| Campo | Valor |
|---|---|
| CD_CONTA | 1.01.01 |
| DS_CONTA | CAIXA E EQUIVALENTES DE CAIXA |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Sim; usar 0 apenas em derivacoes de Fleuriet quando necessario |
| Empresas sem a variavel | A levantar na etapa de validacao setorial |
| Impacto quando ausente | Invalida Liquidez Imediata e parte do Ativo Circulante Financeiro |
| Validacao no setor piloto | A validar |
| Usado em | Liquidez Imediata; Ativo Circulante Financeiro; Saldo de Tesouraria |
| Atencao | Nao usar esta conta sozinha para Divida Liquida quando a DFC mostrar equivalentes adicionais |

### V15. Aplicacoes Financeiras

| Campo | Valor |
|---|---|
| CD_CONTA | 1.01.02 \| 1.01.02.01* \| 1.01.02.01.02* \| 1.01.02.01.03* |
| DS_CONTA | APLICACOES FINANCEIRAS |
| Tabela Silver | n1_dfp_cia_aberta_bp |
| ST_CONTA_FIXA | S/N a validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Sim; usar 0 em Fleuriet e reconciliacao CPC03 |
| Empresas sem a variavel | A levantar na etapa de validacao setorial |
| Impacto quando ausente | Pode subestimar Ativo Circulante Financeiro e conciliacao com 6.05.02 |
| Validacao no setor piloto | A validar |
| Usado em | Ativo Circulante Financeiro; Saldo de Tesouraria; suporte para Divida Liquida |
| Atencao | Familia critica para identificar equivalentes de caixa menores que 90 dias |

### V16. Receita Liquida de Vendas

| Campo | Valor |
|---|---|
| CD_CONTA | 3.01 \| 3.01.* |
| DS_CONTA | RECEITA LIQUIDA DE VENDAS |
| Tabela Silver | n1_dfp_cia_aberta_dre |
| ST_CONTA_FIXA | S/N a validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado em DRE operacional |
| Impacto quando ausente | Invalida Margens Giro de Contas a Receber Giro AC PMRV e PMRAC |
| Validacao no setor piloto | A validar |
| Usado em | Margem Bruta; Margem Operacional; Margem Liquida; Giro de Contas a Receber; Giro AC; PMRV; PMRAC |
| Atencao | Validar sinais e estrutura da silver, mas a familia 3.01 ja esta coerente com os testes da DRE |

### V17. CPV CMV COGS

| Campo | Valor |
|---|---|
| CD_CONTA | 3.02 \| 3.02.* |
| DS_CONTA | CPV CMV COGS |
| Tabela Silver | n1_dfp_cia_aberta_dre |
| ST_CONTA_FIXA | S/N a validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Possivel apenas em operacoes atipicas; listar se ocorrer |
| Impacto quando ausente | Invalida Giro de Estoques Giro de Contas a Pagar PMRE e PMPC |
| Validacao no setor piloto | A validar |
| Usado em | Giro de Estoques; Giro de Contas a Pagar; PMRE; PMPC |
| Atencao | O contrato aceita a familia 3.02 porque a silver ja testa 3.03 = 3.01 + 3.02 |

### V18. Lucro Bruto

| Campo | Valor |
|---|---|
| CD_CONTA | 3.03 |
| DS_CONTA | LUCRO BRUTO ou equivalente da silver |
| Tabela Silver | n1_dfp_cia_aberta_dre |
| ST_CONTA_FIXA | S/N a validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado quando a waterfall da DRE esta integra |
| Impacto quando ausente | Invalida Margem Bruta |
| Validacao no setor piloto | A validar |
| Usado em | Margem Bruta |
| Atencao | A silver ja possui teste matematico para 3.03 |

### V19. EBIT Resultado Operacional

| Campo | Valor |
|---|---|
| CD_CONTA | 3.05 |
| DS_CONTA | RESULTADO OPERACIONAL ou equivalente da silver |
| Tabela Silver | n1_dfp_cia_aberta_dre |
| ST_CONTA_FIXA | S/N a validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado quando a waterfall da DRE esta integra |
| Impacto quando ausente | Invalida Margem Operacional e EBITDA |
| Validacao no setor piloto | A validar |
| Usado em | Margem Operacional; EBITDA |
| Atencao | A silver ja possui teste matematico para 3.05 = 3.03 + 3.04 |

### V20. Lucro Liquido do Exercicio

| Campo | Valor |
|---|---|
| CD_CONTA | 3.11 \| 3.11.* \| 3 |
| DS_CONTA | LUCRO LIQUIDO DO EXERCICIO |
| Tabela Silver | n1_dfp_cia_aberta_dre |
| ST_CONTA_FIXA | S/N a validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado em DRE valida |
| Impacto quando ausente | Invalida Margem Liquida ROA ROE ROI e o numerador do LPA |
| Validacao no setor piloto | A validar |
| Usado em | Margem Liquida; ROA; ROE; ROI; LPA |
| Atencao | Preferir leaf consolidada ou 3.11; usar 3 apenas como fallback analitico de ultima instancia |

### V21. LPA Basico ON ou Diluido ON

| Campo | Valor |
|---|---|
| CD_CONTA | 3.99.* somente leaves |
| DS_CONTA | LUCRO POR ACAO familia 3.99 |
| Tabela Silver | n1_dfp_cia_aberta_dre |
| ST_CONTA_FIXA | A validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | A levantar na etapa de validacao setorial |
| Impacto quando ausente | Invalida LPA e comparabilidade por acao |
| Validacao no setor piloto | A validar |
| Usado em | LPA |
| Atencao | Nunca usar pais reconstruidos; estrategia provisoria: Diluido ON e fallback Basico ON |

### V22. Depreciacao e Amortizacao

| Campo | Valor |
|---|---|
| CD_CONTA | 6.01.02* com DS_CONTA ILIKE depreciacao amortizacao |
| DS_CONTA | DEPRECIACAO E AMORTIZACAO ou ajuste operacional equivalente |
| Tabela Silver | n1_dfp_cia_aberta_dfc |
| ST_CONTA_FIXA | A validar |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Sim; usar 0 apenas na derivacao de EBITDA quando nao houver linha explicita |
| Empresas sem a variavel | A levantar na etapa de validacao setorial |
| Impacto quando ausente | Impede fechamento do EBITDA por via direta |
| Validacao no setor piloto | A validar |
| Usado em | EBITDA |
| Atencao | A familia exata costuma aparecer dentro dos ajustes da DFC operacional e precisa de inventario real do setor |

### V23. Caixa Liquido das Atividades Operacionais

| Campo | Valor |
|---|---|
| CD_CONTA | 6.01 |
| DS_CONTA | CAIXA LIQUIDO ATIVIDADES OPERACIONAIS |
| Tabela Silver | n1_dfp_cia_aberta_dfc |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado em DFC valida |
| Impacto quando ausente | Reduz a leitura do Grupo 7 e da capacidade de caixa operacional |
| Validacao no setor piloto | A validar |
| Usado em | Analise de Recursos Financeiros e apoio analitico |
| Atencao | Nao substitui 6.05.02 para Divida Liquida |

### V24. Saldo Final de Caixa DFC

| Campo | Valor |
|---|---|
| CD_CONTA | 6.05.02 |
| DS_CONTA | SALDO FINAL DE CAIXA E EQUIVALENTES |
| Tabela Silver | n1_dfp_cia_aberta_dfc |
| ST_CONTA_FIXA | S |
| Cobertura no setor | A validar na silver do setor |
| COALESCE? | Nao |
| Empresas sem a variavel | Nao esperado em DFC valida |
| Impacto quando ausente | Invalida Divida Liquida na premissa atual |
| Validacao no setor piloto | A validar |
| Usado em | Divida Liquida |
| Atencao | Seguir N1: esta e a conta correta para caixa economico da Divida Liquida |

### V25. EBITDA

| Campo | Valor |
|---|---|
| CD_CONTA | V19 + V22 |
| DS_CONTA | DERIVADA |
| Tabela Silver | DERIVADA |
| ST_CONTA_FIXA | N/A |
| Cobertura no setor | Depende de V19 e V22 |
| COALESCE? | N/A |
| Empresas sem a variavel | A levantar pela ausencia de V22 quando ocorrer |
| Impacto quando ausente | Reduz comparabilidade de caixa operacional ajustado |
| Validacao no setor piloto | A validar apos fechamento de V22 |
| Usado em | Analise complementar e indicadores auxiliares |
| Atencao | Nao e indicador final do HTML, mas faz parte das variaveis calculadas do dicionario |

### V26. Ativo Circulante Financeiro Fleuriet

| Campo | Valor |
|---|---|
| CD_CONTA | V14 + V15 |
| DS_CONTA | DERIVADA |
| Tabela Silver | DERIVADA |
| ST_CONTA_FIXA | N/A |
| Cobertura no setor | Depende de V14 e V15 |
| COALESCE? | N/A |
| Empresas sem a variavel | Derivada; dependera das contas base |
| Impacto quando ausente | Invalida Saldo de Tesouraria |
| Validacao no setor piloto | A validar |
| Usado em | Saldo de Tesouraria |
| Atencao | Premissa inicial do contrato para Fleuriet: 1.01.01 + 1.01.02 |

### V27. Divida Bruta

| Campo | Valor |
|---|---|
| CD_CONTA | V12 + V13 |
| DS_CONTA | DERIVADA |
| Tabela Silver | DERIVADA |
| ST_CONTA_FIXA | N/A |
| Cobertura no setor | Depende de V12 e V13 |
| COALESCE? | N/A |
| Empresas sem a variavel | Derivada; dependera das contas base |
| Impacto quando ausente | Invalida Divida Liquida e Capital Investido |
| Validacao no setor piloto | A validar |
| Usado em | Divida Liquida; Capital Investido |
| Atencao | Confirmar se o setor exige incluir outros passivos financeiros alem de emprestimos e financiamentos |

### V28. Divida Liquida

| Campo | Valor |
|---|---|
| CD_CONTA | V27 - V24 |
| DS_CONTA | DERIVADA |
| Tabela Silver | DERIVADA |
| ST_CONTA_FIXA | N/A |
| Cobertura no setor | Depende de V24 V27 e da aderencia a N1 |
| COALESCE? | N/A |
| Empresas sem a variavel | Derivada; dependera das contas base |
| Impacto quando ausente | Invalida Capital Investido na premissa atual |
| Validacao no setor piloto | A validar |
| Usado em | Capital Investido |
| Atencao | Seguir a DFC e nao o BP para a parcela de caixa economico |

### V29. Capital Investido

| Campo | Valor |
|---|---|
| CD_CONTA | V11 + V28 |
| DS_CONTA | DERIVADA |
| Tabela Silver | DERIVADA |
| ST_CONTA_FIXA | N/A |
| Cobertura no setor | Depende de V11 e V28 |
| COALESCE? | N/A |
| Empresas sem a variavel | Derivada; dependera das contas base |
| Impacto quando ausente | Invalida ROI |
| Validacao no setor piloto | A validar |
| Usado em | ROI |
| Atencao | Premissa inicial do contrato: PL + Divida Liquida; pode ser refinada na etapa seguinte |

## Mapa Rapido Indicador para Variaveis

| Indicador | Formula | Variaveis necessarias |
|---|---|---|
| Liquidez Geral | `(AC + RLP) / (PC + ELP)` | `V02`, `V04`, `V09`, `V10` |
| Liquidez Corrente | `AC / PC` | `V02`, `V09` |
| Liquidez Seca | `(AC - Estoques) / PC` | `V02`, `V06`, `V09` |
| Liquidez Imediata | `Disponibilidades / PC` | `V14`, `V09` |
| PCT/CP | `(PC + ELP) / PL` | `V09`, `V10`, `V11` |
| PCT/AT | `(PC + ELP) / AT` | `V09`, `V10`, `V01` |
| Garantia CP/CT | `PL / (PC + ELP)` | `V11`, `V09`, `V10` |
| Composicao de Endividamento | `PC / (PC + ELP)` | `V09`, `V10` |
| Imobilizacao do CP | `Imobilizado / PL` | `V05`, `V11` |
| Imobilizacao do AT | `Imobilizado / AT` | `V05`, `V01` |
| Margem Bruta | `Lucro Bruto / Receita Liquida` | `V18`, `V16` |
| Margem Operacional | `EBIT / Receita Liquida` | `V19`, `V16` |
| Margem Liquida | `Lucro Liquido / Receita Liquida` | `V20`, `V16` |
| LPA | `Lucro Liquido / Numero de acoes` | `V21` com suporte de conciliacao de `V20` |
| ROA | `Lucro Liquido / Ativo Total` | `V20`, `V01` |
| ROE | `Lucro Liquido / PL` | `V20`, `V11` |
| ROI | `Lucro Liquido / Capital Investido` | `V20`, `V29` |
| Giro dos Estoques | `CPV / Estoques` | `V17`, `V06` |
| Giro de Contas a Receber | `Receita Liquida / Contas a Receber` | `V16`, `V07` |
| Giro de Contas a Pagar | `CPV / Fornecedores` | `V17`, `V08` |
| Giro do Ativo Circulante | `Receita Liquida / AC` | `V16`, `V02` |
| PMRE | `(Estoques * 360) / CPV` | `V06`, `V17` |
| PMRV | `(Contas a Receber * 360) / Receita Liquida` | `V07`, `V16` |
| PMPC | `(Fornecedores * 360) / CPV` | `V08`, `V17` |
| PMRAC | `(AC * 360) / Receita Liquida` | `V02`, `V16` |
| Ciclo Economico | `PMRE + PMRV` | `V06`, `V07`, `V16`, `V17` |
| Ciclo Financeiro | `PMRE + PMRV - PMPC` | `V06`, `V07`, `V08`, `V16`, `V17` |
| CGL CCL | `AC - PC` | `V02`, `V09` |
| NCG | `(AC - Caixa - Aplicacoes) - (PC - Emprestimos CP)` | `V02`, `V14`, `V15`, `V09`, `V12` |
| Saldo de Tesouraria | `Ativo Circulante Financeiro - Passivo Circulante Financeiro` | `V26`, `V12` |

## Empresas-anomalia identificadas

Nenhuma empresa foi listada ainda nesta versao.

Pendencias para preencher esta secao:
- empresas sem estoque
- empresas com variantes problematicas em `3.99.*`
- empresas com `PL` negativo
- empresas com divergencias relevantes entre `1.01.01` e `6.05.02`

## Checklist de aderencia deste rascunho

- Todas as variaveis do bloco do Excel foram convertidas em fichas `V01` a `V29`.
- As notas `N1` a `N4` foram explicitadas.
- O `Mapa Rapido` cobre os 7 grupos de indicadores.
- Ainda falta a etapa de validacao real na `silver` do setor para preencher cobertura, empresas-anomalia e validacao contra empresa piloto.

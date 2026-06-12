"""Shared constants for the executive Cosan dashboard."""

COSAN_CNPJ = "50.746.577/0001-15"
COSAN_NAME = "COSAN S.A."
COSAN_SETOR = "Agricultura (Açúcar, Álcool e Cana)"

PRIORITY_INDICATORS = [
    {
        "group": "Liquidez",
        "code": "LIQ_SECA_AJUSTADA",
        "label": "Liquidez Seca Ajustada",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "group": "Liquidez",
        "code": "LIQ_CORRENTE",
        "label": "Liquidez Corrente",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "group": "Liquidez",
        "code": "LIQ_IMEDIATA",
        "label": "Liquidez Imediata",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "group": "Endividamento",
        "code": "ENDIV_TOTAL",
        "label": "Endividamento Total",
        "direction": "lower_better",
        "format": "pct",
    },
    {
        "group": "Endividamento",
        "code": "COMPOSICAO_ENDIV",
        "label": "Composição do Endividamento",
        "direction": "lower_better",
        "format": "pct",
    },
    {
        "group": "Endividamento",
        "code": "GARANTIA_CP_CT",
        "label": "Garantia Capital Próprio / Capital de Terceiros",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "group": "Margens",
        "code": "MARGEM_BRUTA",
        "label": "Margem Bruta",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "group": "Margens",
        "code": "MARGEM_OPERACIONAL",
        "label": "Margem Operacional",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "group": "Margens",
        "code": "MARGEM_LIQUIDA",
        "label": "Margem Líquida",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "group": "Rentabilidade",
        "code": "ROA",
        "label": "ROA",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "group": "Rentabilidade",
        "code": "ROE",
        "label": "ROE",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "group": "Rentabilidade",
        "code": "ROI",
        "label": "ROI",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "group": "Atividade",
        "code": "GIRO_ESTOQUES_AJUSTADO",
        "label": "Giro de Estoques Ajustado",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "group": "Atividade",
        "code": "PMRE_AJUSTADO",
        "label": "PMRE Ajustado",
        "direction": "lower_better",
        "format": "days",
    },
    {
        "group": "Atividade",
        "code": "PMRV",
        "label": "PMRV",
        "direction": "lower_better",
        "format": "days",
    },
    {
        "group": "Atividade",
        "code": "PMPC",
        "label": "PMPC",
        "direction": "higher_better",
        "format": "days",
    },
    {
        "group": "Ciclos",
        "code": "CICLO_ECONOMICO",
        "label": "Ciclo Econômico",
        "direction": "lower_better",
        "format": "days",
    },
    {
        "group": "Ciclos",
        "code": "CICLO_FINANCEIRO",
        "label": "Ciclo Financeiro",
        "direction": "lower_better",
        "format": "days",
    },
    {
        "group": "Recursos Financeiros",
        "code": "NCG",
        "label": "Necessidade de Capital de Giro",
        "direction": "lower_better",
        "format": "currency",
    },
    {
        "group": "Recursos Financeiros",
        "code": "ST",
        "label": "Saldo de Tesouraria",
        "direction": "higher_better",
        "format": "currency",
    },
    {
        "group": "Recursos Financeiros",
        "code": "CGL",
        "label": "Capital de Giro Líquido",
        "direction": "higher_better",
        "format": "currency",
    },
]

PRIORITY_INDICATOR_CODES = [item["code"] for item in PRIORITY_INDICATORS]
INDICATOR_META = {item["code"]: item for item in PRIORITY_INDICATORS}

CLASSIC_INDICATOR_REFERENCE = {
    "LIQ_GERAL": {
        "full_label": "Liquidez Geral",
        "format": "ratio",
        "formula": "(Ativo Circulante + Realizável a Longo Prazo) / (Passivo Circulante + Passivo Não Circulante)",
        "objective": "Mostra a capacidade de pagamento no curto e no longo prazo para cada R$ 1,00 de dívida total.",
        "analysis": "Quanto maior, melhor. Em geral, valores acima de 1,0 indicam cobertura satisfatória das obrigações totais.",
    },
    "LIQ_CORRENTE": {
        "full_label": "Liquidez Corrente",
        "format": "ratio",
        "formula": "Ativo Circulante / Passivo Circulante",
        "objective": "Mostra a capacidade de pagamento no curto prazo com base apenas nos ativos e passivos circulantes.",
        "analysis": "Quanto maior, melhor. Como referência didática, valores acima de 1,5 costumam indicar posição mais confortável.",
    },
    "LIQ_SECA_AJUSTADA": {
        "full_label": "Liquidez Seca Ajustada",
        "format": "ratio",
        "formula": "(Ativo Circulante - Estoques - Ativos Biológicos, quando aplicável) / Passivo Circulante",
        "objective": "Mede a capacidade de pagar obrigações de curto prazo sem depender da realização dos estoques e, no setor agrícola, também ajustando ativos biológicos circulantes quando existirem.",
        "analysis": "Quanto maior, melhor. O ajuste evita superestimar a liquidez operacional de empresas com capital empatado em estoques ou ativos biológicos.",
    },
    "LIQ_IMEDIATA": {
        "full_label": "Liquidez Imediata",
        "format": "ratio",
        "formula": "Disponibilidades / Passivo Circulante",
        "objective": "Mostra a capacidade de pagamento imediata usando caixa, equivalentes de caixa e aplicações financeiras.",
        "analysis": "Quanto maior, melhor. É um indicador mais conservador porque considera apenas recursos imediatamente disponíveis.",
    },
    "ENDIV_CP": {
        "full_label": "Participação do Capital de Terceiros em Relação ao Capital Próprio",
        "format": "pct",
        "formula": "(Passivo Circulante + Passivo Não Circulante) / Patrimônio Líquido",
        "objective": "Indica quanto a empresa tomou de recursos de terceiros em relação ao capital próprio.",
        "analysis": "Quanto maior, maior a dependência de capital de terceiros e, portanto, maior a alavancagem financeira.",
    },
    "ENDIV_TOTAL": {
        "full_label": "Participação do Capital de Terceiros em Relação ao Ativo Total",
        "format": "pct",
        "formula": "(Passivo Circulante + Passivo Não Circulante) / Ativo Total",
        "objective": "Mede a proporção do ativo total financiada por capital de terceiros.",
        "analysis": "Quanto maior, maior o endividamento da estrutura de capital. A leitura ideal depende do setor, mas níveis menores indicam maior independência financeira.",
    },
    "GARANTIA_CP_CT": {
        "full_label": "Garantia de Capital Próprio ao Capital de Terceiros",
        "format": "ratio",
        "formula": "Patrimônio Líquido / (Passivo Circulante + Passivo Não Circulante)",
        "objective": "Mostra quanto de capital próprio existe para garantir cada R$ 1,00 de capital de terceiros.",
        "analysis": "Quanto maior, melhor. Valores mais altos indicam maior segurança para credores e menor pressão de endividamento.",
    },
    "COMPOSICAO_ENDIV": {
        "full_label": "Composição do Endividamento",
        "format": "pct",
        "formula": "Passivo Circulante / (Passivo Circulante + Passivo Não Circulante)",
        "objective": "Indica qual parcela do endividamento total vence no curto prazo.",
        "analysis": "Quanto menor, melhor. Valores muito próximos de 1 mostram concentração da dívida no curto prazo.",
    },
    "IMOB_PL": {
        "full_label": "Imobilização de Capital Próprio",
        "format": "pct",
        "formula": "Ativo Imobilizado / Patrimônio Líquido",
        "objective": "Mostra quanto do patrimônio líquido está aplicado em ativos imobilizados.",
        "analysis": "Quanto menor, melhor. Como referência didática, valores abaixo de 1 tendem a indicar maior folga para financiar o giro.",
    },
    "IMOB_AT": {
        "full_label": "Imobilização do Ativo Total",
        "format": "pct",
        "formula": "Ativo Imobilizado / Ativo Total",
        "objective": "Indica a participação percentual do ativo imobilizado dentro do ativo total.",
        "analysis": "A interpretação depende do setor. Estruturas intensivas em capital aceitam percentuais maiores, mas níveis muito altos podem reduzir flexibilidade financeira.",
    },
    "MARGEM_BRUTA": {
        "full_label": "Margem Bruta",
        "format": "pct",
        "formula": "Lucro Bruto / Receita Líquida de Venda",
        "objective": "Mede quanto sobra das vendas após o pagamento dos custos diretos dos bens ou serviços vendidos.",
        "analysis": "Quanto maior, melhor. Margens mais altas indicam melhor capacidade de precificação ou controle de custos diretos.",
    },
    "MARGEM_OPERACIONAL": {
        "full_label": "Margem Operacional",
        "format": "pct",
        "formula": "Lucro Operacional / Receita Líquida de Venda",
        "objective": "Mede a parcela da receita líquida que permanece após custos e despesas operacionais.",
        "analysis": "Quanto maior, melhor. O indicador mostra a eficiência da operação antes do efeito completo do resultado financeiro e dos impostos.",
    },
    "MARGEM_LIQUIDA": {
        "full_label": "Margem Líquida",
        "format": "pct",
        "formula": "Lucro Líquido do Exercício / Receita Líquida de Venda",
        "objective": "Mede quanto da receita líquida se transforma em lucro final depois de custos, despesas, juros e impostos.",
        "analysis": "Quanto maior, melhor. Margens líquidas consistentes sugerem melhor conversão de vendas em resultado final.",
    },
    "LPA": {
        "full_label": "Lucro Líquido por Ação (LPA)",
        "format": "currency",
        "formula": "Lucro Líquido do Exercício / Número de Ações Emitidas",
        "objective": "Representa o lucro atribuível a cada ação da empresa.",
        "analysis": "Quanto maior, melhor para o acionista. É um indicador útil para comparação temporal e de mercado quando calculado sobre bases consistentes.",
    },
    "ROA": {
        "full_label": "Retorno sobre o Ativo Total (ROA)",
        "format": "pct",
        "formula": "Lucro Líquido / Ativo Total",
        "objective": "Mede a eficácia da empresa em gerar lucro a partir do conjunto de ativos disponíveis.",
        "analysis": "Quanto maior, melhor. Mostra a eficiência econômica da base de ativos.",
    },
    "ROE": {
        "full_label": "Retorno sobre o Patrimônio Líquido (ROE)",
        "format": "pct",
        "formula": "Lucro Líquido / Patrimônio Líquido",
        "objective": "Mede o retorno obtido pelos acionistas sobre o capital próprio investido.",
        "analysis": "Quanto maior, melhor. É uma medida central de rentabilidade do ponto de vista do investidor.",
    },
    "ROI": {
        "full_label": "Retorno sobre o Investimento (ROI)",
        "format": "pct",
        "formula": "Lucro Líquido / (Passivo Oneroso + Patrimônio Líquido)",
        "objective": "Mede a geração de lucro sobre o capital total investido no negócio.",
        "analysis": "Quanto maior, melhor. Ajuda a avaliar se os recursos captados e próprios estão gerando retorno adequado.",
    },
    "GIRO_ESTOQUES_AJUSTADO": {
        "full_label": "Giro dos Estoques Ajustado",
        "format": "ratio",
        "formula": "ABS(CPV) / (Estoques + Ativos Biológicos, quando aplicável)",
        "objective": "Indica quantas vezes o estoque operacional se renova no período, incluindo ativos biológicos quando a estrutura da empresa exigir esse ajuste.",
        "analysis": "Quanto maior, melhor. Giros mais altos sugerem menor capital parado em estoque ao longo do exercício.",
    },
    "GIRO_CLIENTES": {
        "full_label": "Giro do Contas a Receber",
        "format": "ratio",
        "formula": "Receita Líquida de Venda / Clientes (Curto + Longo Prazo)",
        "objective": "Indica quantas vezes a carteira de clientes se renova no período.",
        "analysis": "Quanto maior, melhor. Giros maiores indicam recebimento mais rápido das vendas.",
    },
    "GIRO_FORNECEDORES": {
        "full_label": "Giro do Contas a Pagar",
        "format": "ratio",
        "formula": "ABS(CPV) / Fornecedores",
        "objective": "Indica quantas vezes a empresa paga suas compras ou fornecedores no período.",
        "analysis": "A interpretação exige contexto. Giro menor costuma significar prazo maior para pagamento, o que pode aliviar o caixa.",
    },
    "GIRO_AC": {
        "full_label": "Giro do Ativo Circulante",
        "format": "ratio",
        "formula": "Receita Líquida de Venda / Ativo Circulante",
        "objective": "Mostra quantas vezes os ativos de curto prazo são convertidos em vendas no período.",
        "analysis": "Quanto maior, melhor. Indica maior eficiência no uso do ativo circulante.",
    },
    "PMRE_AJUSTADO": {
        "full_label": "Prazo Médio de Renovação dos Estoques (PMRE) Ajustado",
        "format": "days",
        "formula": "((Estoques + Ativos Biológicos, quando aplicável) x 360) / ABS(CPV)",
        "objective": "Mostra quantos dias, em média, o estoque operacional leva para se renovar, com ajuste setorial quando houver ativos biológicos relevantes.",
        "analysis": "Quanto menor, melhor. Prazos menores indicam maior velocidade de conversão do estoque em vendas.",
    },
    "PMRV": {
        "full_label": "Prazo Médio de Recebimento das Vendas (PMRV)",
        "format": "days",
        "formula": "(Duplicatas a Receber x 360) / Receita Líquida de Venda",
        "objective": "Mostra em quantos dias, em média, a empresa recebe pelas vendas realizadas.",
        "analysis": "Quanto menor, melhor. Prazos maiores pressionam o capital de giro.",
    },
    "PMPC": {
        "full_label": "Prazo Médio de Pagamento das Compras (PMPC)",
        "format": "days",
        "formula": "(Fornecedores x 360) / ABS(CPV)",
        "objective": "Mostra em quantos dias, em média, a empresa paga seus fornecedores.",
        "analysis": "Quanto maior, melhor para o caixa, desde que o prazo seja sustentável e não sinalize deterioração do relacionamento com fornecedores.",
    },
    "PMRAC": {
        "full_label": "Prazo Médio de Renovação do Ativo Circulante (PMRAC)",
        "format": "days",
        "formula": "(Ativo Circulante x 360) / Receita Líquida de Venda",
        "objective": "Mostra em quantos dias, em média, o ativo circulante se converte em receita de vendas.",
        "analysis": "Quanto menor, melhor. Prazos menores indicam maior agilidade operacional.",
    },
    "CICLO_ECONOMICO": {
        "full_label": "Ciclo Econômico",
        "format": "days",
        "formula": "PMRE + PMRV",
        "objective": "Mostra o tempo entre a compra ou formação do estoque e o recebimento da venda.",
        "analysis": "Quanto menor, melhor. Ciclos mais curtos reduzem a necessidade de capital preso na operação.",
    },
    "CICLO_FINANCEIRO": {
        "full_label": "Ciclo Financeiro",
        "format": "days",
        "formula": "PMRE + PMRV - PMPC",
        "objective": "Mostra por quantos dias a empresa precisa financiar sua operação antes de receber pelas vendas.",
        "analysis": "Quanto menor, melhor. Ciclo negativo indica que a operação tende a se autofinanciar.",
    },
    "CGL": {
        "full_label": "Capital de Giro Líquido (CGL)",
        "format": "currency",
        "formula": "Ativo Circulante - Passivo Circulante",
        "objective": "Mede a folga financeira de curto prazo após a cobertura das obrigações circulantes.",
        "analysis": "Quanto maior, melhor. Valores positivos indicam maior conforto para sustentar a operação corrente.",
    },
    "NCG": {
        "full_label": "Necessidade de Capital de Giro (NCG)",
        "format": "currency",
        "formula": "Ativo Circulante Operacional - Passivo Circulante Operacional",
        "objective": "Mede o volume mínimo de recursos que a operação exige para continuar funcionando.",
        "analysis": "Valores menores reduzem a pressão sobre o caixa. Níveis muito altos sugerem maior capital empatado na operação.",
    },
    "ST": {
        "full_label": "Saldo de Tesouraria (ST)",
        "format": "currency",
        "formula": "Ativo Circulante Financeiro - Passivo Circulante Financeiro",
        "objective": "Mostra a posição financeira de tesouraria disponível no curto prazo.",
        "analysis": "Quanto maior, melhor. Saldos negativos recorrentes podem sinalizar efeito tesoura e deterioração financeira.",
    },
}

CLASSIC_INDICATOR_LABELS = {
    code: metadata["full_label"] for code, metadata in CLASSIC_INDICATOR_REFERENCE.items()
}

CLASSIC_INDICATOR_FORMATS = {
    code: metadata["format"] for code, metadata in CLASSIC_INDICATOR_REFERENCE.items()
}

CLASSIC_INDICATOR_TOOLTIPS = {
    code: (
        f"Objetivo: {metadata['objective']}\n"
        f"Cálculo: {metadata['formula']}\n"
        f"Análise: {metadata['analysis']}"
    )
    for code, metadata in CLASSIC_INDICATOR_REFERENCE.items()
}

IPRF_INDICATORS = [
    {
        "dimension": "Liquidez",
        "code": "LIQ_CORRENTE",
        "note_code": "NOTA_LIQ_CORRENTE",
        "label": "Liquidez Corrente",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "dimension": "Liquidez",
        "code": "LIQ_SECA_AJUSTADA",
        "note_code": "NOTA_LIQ_SECA",
        "label": "Liquidez Seca Ajustada",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "dimension": "Liquidez",
        "code": "COB_CAIXA_OPERACIONAL",
        "note_code": "NOTA_COB_CAIXA_OPERACIONAL",
        "label": "Cobertura de Caixa Operacional",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "dimension": "Rentabilidade",
        "code": "MARGEM_EBITDA",
        "note_code": "NOTA_MARGEM_EBITDA",
        "label": "Margem EBITDA",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "dimension": "Rentabilidade",
        "code": "MARGEM_LIQUIDA",
        "note_code": "NOTA_MARGEM_LIQUIDA",
        "label": "Margem Líquida",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "dimension": "Rentabilidade",
        "code": "ROA",
        "note_code": "NOTA_ROA",
        "label": "ROA",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "dimension": "Solvência",
        "code": "DL_EBITDA",
        "note_code": "NOTA_DL_EBITDA",
        "label": "Dívida Líquida / EBITDA",
        "direction": "lower_better",
        "format": "ratio",
    },
    {
        "dimension": "Solvência",
        "code": "GRAU_ENDIVIDAMENTO",
        "note_code": "NOTA_GRAU_ENDIVIDAMENTO",
        "label": "Grau de Endividamento",
        "direction": "lower_better",
        "format": "pct",
    },
    {
        "dimension": "Eficiência",
        "code": "CCC",
        "note_code": "NOTA_CCC",
        "label": "Ciclo de Conversão de Caixa",
        "direction": "lower_better",
        "format": "days",
    },
    {
        "dimension": "Eficiência",
        "code": "GIRO_ATIVO_TOTAL",
        "note_code": "NOTA_GIRO_ATIVO_TOTAL",
        "label": "Giro do Ativo Total",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "dimension": "Geração de Caixa",
        "code": "MARGEM_CAIXA_OPERACIONAL",
        "note_code": "NOTA_MARGEM_CAIXA_OPERACIONAL",
        "label": "Margem de Caixa Operacional",
        "direction": "higher_better",
        "format": "pct",
    },
    {
        "dimension": "Geração de Caixa",
        "code": "COBERTURA_DIVIDA_CAIXA",
        "note_code": "NOTA_COBERTURA_DIVIDA_CAIXA",
        "label": "Cobertura de Dívida por Caixa",
        "direction": "higher_better",
        "format": "ratio",
    },
    {
        "dimension": "Geração de Caixa",
        "code": "INTENSIDADE_REINVESTIMENTO",
        "note_code": "NOTA_INTENSIDADE_REINVESTIMENTO",
        "label": "Intensidade de Reinvestimento",
        "direction": "u_shape",
        "format": "pct",
    },
]

IPRF_DIMENSION_SCORES = [
    ("SCORE_LIQUIDEZ", "Liquidez"),
    ("SCORE_RENTABILIDADE", "Rentabilidade"),
    ("SCORE_SOLVENCIA", "Solvência"),
    ("SCORE_EFICIENCIA", "Eficiência"),
    ("SCORE_GERACAO_CAIXA", "Geração de Caixa"),
]

COSAN_COLORS = {
    "bg": "#091929",
    "card": "#112236",
    "card_alt": "#0D2137",
    "line": "#1E3A55",
    "text": "#F6FBFF",
    "muted": "#7DA5BE",
    "lime": "#B5E300",
    "teal": "#00AEBA",
    "amber": "#F59E0B",
    "red": "#EF4444",
    "violet": "#A78BFA",
    "green": "#34D399",
}

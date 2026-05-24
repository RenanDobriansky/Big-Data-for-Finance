-- Recria a mart no mesmo formato da versao anterior, agora para todas as empresas.
-- Ajustes principais:
-- 1. Remove o filtro de setor.
-- 2. Corrige AT_BIOLOGICO para CD_CONTA = '1.01.05'.
-- 3. Usa AT_BIOLOGICO apenas quando existir, sem penalizar empresas de outros setores.
-- 4. Ajusta LIQ_IMEDIATA para considerar Caixa + Aplicacoes Financeiras.
-- 5. Ajusta PMRE e Giro de Estoques para considerar Estoques + Ativos Biologicos quando houver.
-- 6. Completa todos os indicadores formula-definidos em Indicadores/00_racional_indicadores/indicadores_financeiros.md.

DROP TABLE IF EXISTS "layer_03_gold"."mart_indicadores_financeiros";

CREATE TABLE "layer_03_gold"."mart_indicadores_financeiros" AS
WITH deduplicado_bp AS (
    SELECT *
    FROM (
        SELECT
            "CNPJ_CIA",
            "DT_REFER",
            "DENOM_CIA",
            "SETOR_ATIV",
            "CD_CONTA",
            "VL_CONTA_TRATADO",
            "VERSAO",
            ROW_NUMBER() OVER (
                PARTITION BY "CNPJ_CIA", "DT_REFER", "CD_CONTA"
                ORDER BY "VERSAO" DESC
            ) AS rn
        FROM "layer_02_silver"."n1_dfp_cia_aberta_bp"
    ) t
    WHERE rn = 1
),
deduplicado_dre AS (
    SELECT *
    FROM (
        SELECT
            "CNPJ_CIA",
            "DT_REFER",
            "DENOM_CIA",
            "SETOR_ATIV",
            "CD_CONTA",
            "VL_CONTA_TRATADO",
            "VERSAO",
            ROW_NUMBER() OVER (
                PARTITION BY "CNPJ_CIA", "DT_REFER", "CD_CONTA"
                ORDER BY "VERSAO" DESC
            ) AS rn
        FROM "layer_02_silver"."n1_dfp_cia_aberta_dre"
    ) t
    WHERE rn = 1
),
deduplicado_dfc AS (
    SELECT *
    FROM (
        SELECT
            "CNPJ_CIA",
            "DT_REFER",
            "DENOM_CIA",
            "SETOR_ATIV",
            "CD_CONTA",
            "VL_CONTA_TRATADO",
            "VERSAO",
            ROW_NUMBER() OVER (
                PARTITION BY "CNPJ_CIA", "DT_REFER", "CD_CONTA"
                ORDER BY "VERSAO" DESC
            ) AS rn
        FROM "layer_02_silver"."n1_dfp_cia_aberta_dfc"
    ) t
    WHERE rn = 1
),
primeira_ordem AS (
    SELECT
        "CNPJ_CIA",
        "DT_REFER",
        "DENOM_CIA" AS "RAZAO_SOCIAL",
        "SETOR_ATIV" AS "SETOR",
        'MERCADO_ABERTO' AS "TP_MERC",
        MAX(CASE WHEN "CD_CONTA" = '1' THEN "VL_CONTA_TRATADO" END) AS "AT",
        MAX(CASE WHEN "CD_CONTA" = '1.01' THEN "VL_CONTA_TRATADO" END) AS "AC",
        MAX(CASE WHEN "CD_CONTA" = '1.01.01' THEN "VL_CONTA_TRATADO" END) AS "CAIXA_EQUIV",
        MAX(CASE WHEN "CD_CONTA" = '1.01.02' THEN "VL_CONTA_TRATADO" END) AS "APLIC_FIN",
        MAX(CASE WHEN "CD_CONTA" = '1.01.03' THEN "VL_CONTA_TRATADO" END) AS "CLIENTES",
        MAX(CASE WHEN "CD_CONTA" = '1.01.04' THEN "VL_CONTA_TRATADO" END) AS "ESTOQUES",
        MAX(CASE WHEN "CD_CONTA" = '1.01.05' THEN "VL_CONTA_TRATADO" END) AS "AT_BIOLOGICO",
        MAX(CASE WHEN "CD_CONTA" = '1.02.01' THEN "VL_CONTA_TRATADO" END) AS "RLP",
        MAX(CASE WHEN "CD_CONTA" = '1.02.03' THEN "VL_CONTA_TRATADO" END) AS "IMOBILIZADO",
        MAX(CASE WHEN "CD_CONTA" = '2.01' THEN "VL_CONTA_TRATADO" END) AS "PC",
        MAX(CASE WHEN "CD_CONTA" = '2.01.02' THEN "VL_CONTA_TRATADO" END) AS "FORNECEDORES",
        MAX(CASE WHEN "CD_CONTA" = '2.01.04' THEN "VL_CONTA_TRATADO" END) AS "EMP_FIN_CP",
        MAX(CASE WHEN "CD_CONTA" = '2.02' THEN "VL_CONTA_TRATADO" END) AS "PNC",
        MAX(CASE WHEN "CD_CONTA" = '2.02.01' THEN "VL_CONTA_TRATADO" END) AS "EMP_FIN_LP",
        MAX(CASE WHEN "CD_CONTA" = '2.03' THEN "VL_CONTA_TRATADO" END) AS "PL",
        MAX(CASE WHEN "CD_CONTA" = '3.01' THEN "VL_CONTA_TRATADO" END) AS "REC_LIQ",
        MAX(CASE WHEN "CD_CONTA" = '3.02' THEN "VL_CONTA_TRATADO" END) AS "CPV",
        MAX(CASE WHEN "CD_CONTA" = '3.03' THEN "VL_CONTA_TRATADO" END) AS "LUCRO_BRUTO",
        MAX(CASE WHEN "CD_CONTA" = '3.05' THEN "VL_CONTA_TRATADO" END) AS "EBIT",
        MAX(CASE WHEN "CD_CONTA" = '3.11' THEN "VL_CONTA_TRATADO" END) AS "LUCRO_LIQ",
        MAX(CASE WHEN "CD_CONTA" = '3.99.02.01' THEN "VL_CONTA_TRATADO" END) AS "LPA_DILUIDO_ON",
        MAX(CASE WHEN "CD_CONTA" = '3.99.01.01' THEN "VL_CONTA_TRATADO" END) AS "LPA_BASICO_ON",
        MAX(CASE WHEN "CD_CONTA" = '3.99' THEN "VL_CONTA_TRATADO" END) AS "LPA_3_99",
        MAX(CASE WHEN "CD_CONTA" = '6.05.02' THEN "VL_CONTA_TRATADO" END) AS "SALDO_FINAL_CAIXA_DFC"
    FROM (
        SELECT
            "CNPJ_CIA",
            "DT_REFER",
            "DENOM_CIA",
            "SETOR_ATIV",
            "CD_CONTA",
            "VL_CONTA_TRATADO"
        FROM deduplicado_bp

        UNION ALL

        SELECT
            "CNPJ_CIA",
            "DT_REFER",
            "DENOM_CIA",
            "SETOR_ATIV",
            "CD_CONTA",
            "VL_CONTA_TRATADO"
        FROM deduplicado_dre

        UNION ALL

        SELECT
            "CNPJ_CIA",
            "DT_REFER",
            "DENOM_CIA",
            "SETOR_ATIV",
            "CD_CONTA",
            "VL_CONTA_TRATADO"
        FROM deduplicado_dfc
    ) u
    GROUP BY 1, 2, 3, 4, 5
),
segunda_ordem AS (
    SELECT
        *,
        (COALESCE("CAIXA_EQUIV", 0) + COALESCE("APLIC_FIN", 0)) AS "ACF",
        (COALESCE("AC", 0) - (COALESCE("CAIXA_EQUIV", 0) + COALESCE("APLIC_FIN", 0))) AS "ACO",
        COALESCE("EMP_FIN_CP", 0) AS "PCF",
        (COALESCE("PC", 0) - COALESCE("EMP_FIN_CP", 0)) AS "PCO",
        (COALESCE("AC", 0) - COALESCE("PC", 0)) AS "CGL",
        ABS(COALESCE("CPV", 0)) AS "CPV_ABS",
        (COALESCE("ESTOQUES", 0) + COALESCE("AT_BIOLOGICO", 0)) AS "ESTOQUE_OPERACIONAL"
    FROM primeira_ordem
),
mart_final AS (
    SELECT
        "CNPJ_CIA",
        "DT_REFER",
        "RAZAO_SOCIAL",
        "SETOR",
        "TP_MERC",
        "AT",
        "AC",
        "CAIXA_EQUIV",
        "APLIC_FIN",
        "CLIENTES",
        "ESTOQUES",
        "AT_BIOLOGICO",
        "RLP",
        "IMOBILIZADO",
        "PC",
        "FORNECEDORES",
        "EMP_FIN_CP",
        "PNC",
        "EMP_FIN_LP",
        "PL",
        "REC_LIQ",
        "CPV",
        "LUCRO_BRUTO",
        "EBIT",
        "LUCRO_LIQ",
        COALESCE("LPA_DILUIDO_ON", "LPA_BASICO_ON", "LPA_3_99") AS "LPA",
        "SALDO_FINAL_CAIXA_DFC",
        "ACF",
        "ACO",
        "PCF",
        "PCO",
        "CGL",
        "CPV_ABS",
        "ESTOQUE_OPERACIONAL",
        CASE
            WHEN "PC" > 0 THEN "AC" / "PC"
        END AS "LIQ_CORRENTE",
        CASE
            WHEN "PC" > 0 THEN ("AC" - "ESTOQUE_OPERACIONAL") / "PC"
        END AS "LIQ_SECA",
        CASE
            WHEN "PC" > 0 THEN "ACF" / "PC"
        END AS "LIQ_IMEDIATA",
        CASE
            WHEN ("PC" + "PNC") > 0 THEN ("AC" + "RLP") / ("PC" + "PNC")
        END AS "LIQ_GERAL",
        CASE
            WHEN "AT" > 0 THEN ("PC" + "PNC") / "AT"
        END AS "ENDIV_TOTAL",
        CASE
            WHEN "PL" <> 0 THEN ("PC" + "PNC") / "PL"
        END AS "ENDIV_CP",
        CASE
            WHEN ("PC" + "PNC") <> 0 THEN "PL" / ("PC" + "PNC")
        END AS "GARANTIA_CP_CT",
        CASE
            WHEN ("PC" + "PNC") <> 0 THEN "PC" / ("PC" + "PNC")
        END AS "COMPOSICAO_ENDIV",
        CASE
            WHEN "PL" > 0 THEN "IMOBILIZADO" / "PL"
        END AS "IMOB_PL",
        CASE
            WHEN "AT" > 0 THEN "IMOBILIZADO" / "AT"
        END AS "IMOB_AT",
        CASE
            WHEN "REC_LIQ" > 0 THEN "LUCRO_BRUTO" / "REC_LIQ"
        END AS "MARGEM_BRUTA",
        CASE
            WHEN "REC_LIQ" > 0 THEN "EBIT" / "REC_LIQ"
        END AS "MARGEM_OPERACIONAL",
        CASE
            WHEN "REC_LIQ" > 0 THEN "LUCRO_LIQ" / "REC_LIQ"
        END AS "MARGEM_LIQUIDA",
        CASE
            WHEN "AT" > 0 THEN "LUCRO_LIQ" / "AT"
        END AS "ROA",
        CASE
            WHEN "PL" > 0 THEN "LUCRO_LIQ" / "PL"
        END AS "ROE",
        CASE
            WHEN (COALESCE("EMP_FIN_CP", 0) + COALESCE("EMP_FIN_LP", 0) + COALESCE("PL", 0)) <> 0
                THEN "LUCRO_LIQ" / (COALESCE("EMP_FIN_CP", 0) + COALESCE("EMP_FIN_LP", 0) + COALESCE("PL", 0))
        END AS "ROI",
        CASE
            WHEN "ESTOQUE_OPERACIONAL" > 0 THEN "CPV_ABS" / "ESTOQUE_OPERACIONAL"
        END AS "GIRO_ESTOQUES",
        CASE
            WHEN "CLIENTES" > 0 THEN "REC_LIQ" / "CLIENTES"
        END AS "GIRO_CLIENTES",
        CASE
            WHEN "FORNECEDORES" > 0 THEN "CPV_ABS" / "FORNECEDORES"
        END AS "GIRO_FORNECEDORES",
        CASE
            WHEN "AC" > 0 THEN "REC_LIQ" / "AC"
        END AS "GIRO_AC",
        ("ACO" - "PCO") AS "NCG",
        ("ACF" - "PCF") AS "ST",
        CASE
            WHEN "REC_LIQ" > 0 AND "CLIENTES" IS NOT NULL THEN ("CLIENTES" * 360.0) / "REC_LIQ"
        END AS "PMRV",
        CASE
            WHEN "CPV_ABS" > 0
             AND ("ESTOQUES" IS NOT NULL OR "AT_BIOLOGICO" IS NOT NULL)
                THEN ("ESTOQUE_OPERACIONAL" * 360.0) / "CPV_ABS"
        END AS "PMRE",
        CASE
            WHEN "CPV_ABS" > 0 AND "FORNECEDORES" IS NOT NULL THEN ("FORNECEDORES" * 360.0) / "CPV_ABS"
        END AS "PMPC",
        CASE
            WHEN "REC_LIQ" > 0 AND "AC" IS NOT NULL THEN ("AC" * 360.0) / "REC_LIQ"
        END AS "PMRAC"
    FROM segunda_ordem
),
mart_com_ciclos AS (
    SELECT
        *,
        CASE
            WHEN "PMRE" IS NOT NULL AND "PMRV" IS NOT NULL THEN "PMRE" + "PMRV"
        END AS "CICLO_ECONOMICO",
        CASE
            WHEN "PMRE" IS NOT NULL AND "PMRV" IS NOT NULL AND "PMPC" IS NOT NULL
                THEN "PMRE" + "PMRV" - "PMPC"
        END AS "CICLO_FINANCEIRO",
        CASE
            WHEN "ST" < 0
             AND LAG("ST", 1) OVER (PARTITION BY "CNPJ_CIA" ORDER BY "DT_REFER") < 0
             AND LAG("ST", 2) OVER (PARTITION BY "CNPJ_CIA" ORDER BY "DT_REFER") < 0
             AND "ST" < LAG("ST", 1) OVER (PARTITION BY "CNPJ_CIA" ORDER BY "DT_REFER")
             AND LAG("ST", 1) OVER (PARTITION BY "CNPJ_CIA" ORDER BY "DT_REFER")
                 < LAG("ST", 2) OVER (PARTITION BY "CNPJ_CIA" ORDER BY "DT_REFER")
                THEN TRUE
            ELSE FALSE
        END AS "EFEITO_TESOURA"
    FROM mart_final
)
SELECT *
FROM mart_com_ciclos;

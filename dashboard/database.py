import os
from typing import Iterable

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

from constants import (
    COSAN_CNPJ,
    COSAN_NAME,
    COSAN_SETOR,
    IPRF_INDICATORS,
    PRIORITY_INDICATOR_CODES,
)


@st.cache_resource
def get_db_connection():
    """Create one SQLAlchemy engine and reuse it across Streamlit reruns."""
    user = quote_plus(os.getenv("DB_USER", "postgres"))
    password = quote_plus(os.getenv("DB_PASS", os.getenv("DB_PASSWORD", "password")))
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "data_lake")
    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    )


def _safe_read_sql(query: str, params: dict | None = None) -> pd.DataFrame:
    """Run SQL and return an empty DataFrame when the object is missing."""
    engine = get_db_connection()
    try:
        with engine.connect() as conn:
            return pd.read_sql(text(query), conn, params=params or {})
    except Exception as exc:  # pragma: no cover - runtime guard for the live DB
        st.warning(f"Consulta indisponivel no momento: {exc}")
        return pd.DataFrame()


def _quoted_csv(values: Iterable[str]) -> str:
    """Return a SQL-safe quoted CSV for literal IN clauses."""
    escaped = [value.replace("'", "''") for value in values]
    return ", ".join(f"'{value}'" for value in escaped)


# ==============================================================================
# Generic metadata helpers used by the explorer / monitoring pages
# ==============================================================================


@st.cache_data(ttl=900)
def get_list_of_schemas():
    query = """
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name NOT IN ('information_schema', 'pg_catalog')
      AND schema_name NOT LIKE 'pg_toast%'
      AND schema_name NOT LIKE 'pg_temp%'
    ORDER BY schema_name;
    """
    df = _safe_read_sql(query)
    return df["schema_name"].tolist() if not df.empty else []


@st.cache_data(ttl=900)
def get_tables_in_schema(schema: str):
    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = :schema
    ORDER BY table_name;
    """
    df = _safe_read_sql(query, {"schema": schema})
    return df["table_name"].tolist() if not df.empty else []


@st.cache_data(ttl=300)
def load_table_data(table_name: str, schema: str, limit: int = 5000):
    query = f'SELECT * FROM "{schema}"."{table_name}" LIMIT {int(limit)};'
    return _safe_read_sql(query)


@st.cache_data(ttl=900)
def get_available_datasets(dataset_type: str, schema: str = "layer_01_bronze"):
    query = f"""
    SELECT table_name AS tabela_destino
         , NULL::INTEGER AS ano_referencia
    FROM information_schema.tables
    WHERE table_schema = :schema
      AND table_name ILIKE :pattern
    ORDER BY table_name;
    """
    return _safe_read_sql(
        query,
        {
            "schema": schema,
            "pattern": f"%{dataset_type.lower()}%",
        },
    )


@st.cache_data(ttl=900)
def get_lake_metadata(schema: str = "layer_01_bronze"):
    query = """
    SELECT
        t.tablename AS nome_tabela,
        pg_total_relation_size(format('%I.%I', t.schemaname, t.tablename)) / 1024.0 / 1024.0 AS tamanho_mb,
        pg_total_relation_size(format('%I.%I', t.schemaname, t.tablename)) / 1024.0 / 1024.0 / 1024.0 AS tamanho_gb,
        COALESCE(s.n_live_tup, 0) AS qtd_linhas_int
    FROM pg_tables t
    LEFT JOIN pg_stat_user_tables s
      ON s.schemaname = t.schemaname
     AND s.relname = t.tablename
    WHERE t.schemaname = :schema
    ORDER BY tamanho_mb DESC, nome_tabela;
    """
    df = _safe_read_sql(query, {"schema": schema})
    if df.empty:
        return df

    df["linhas_txt"] = df["qtd_linhas_int"].map(lambda value: f"{int(value):,}".replace(",", "."))
    df["total_disco_txt"] = df["tamanho_mb"].map(lambda value: f"{value:.1f} MB")
    return df


# ==============================================================================
# Annual statements
# ==============================================================================


STATEMENT_TABLES = {
    "BP": "n1_dfp_cia_aberta_bp",
    "DRE": "n1_dfp_cia_aberta_dre",
    "DFC": "n1_dfp_cia_aberta_dfc",
}

TOP_LEVEL_CODES = {
    "BP": ["1", "1.01", "1.02", "2", "2.01", "2.02", "2.03"],
    "DRE": ["3.01", "3.03", "3.05", "3.11", "3.99.02.01", "3.99.01.01"],
    "DFC": ["6.01", "6.02", "6.03", "6.05.02"],
}


@st.cache_data(ttl=900)
def get_statement_data(
    statement_type: str,
    cnpj: str = COSAN_CNPJ,
    max_level: int = 3,
):
    table_name = STATEMENT_TABLES[statement_type]
    max_digits = (max_level * 2) - 1
    query = f"""
    WITH deduplicado AS (
        SELECT *
        FROM (
            SELECT
                "CNPJ_CIA",
                "DENOM_CIA",
                "SETOR_ATIV",
                "DT_REFER"::date AS "DT_REFER",
                "DT_FIM_EXERC_ANO"::integer AS "ANO_FISCAL",
                "CD_CONTA",
                "DS_CONTA",
                "VL_CONTA_TRATADO",
                "VERSAO",
                ROW_NUMBER() OVER (
                    PARTITION BY "CNPJ_CIA", "DT_FIM_EXERC_ANO", "CD_CONTA"
                    ORDER BY "VERSAO" DESC, "DT_REFER" DESC
                ) AS rn
            FROM "layer_02_silver"."{table_name}"
            WHERE "CNPJ_CIA" = :cnpj
              AND "DT_FIM_EXERC_ANO" IS NOT NULL
              AND LENGTH(REPLACE("CD_CONTA", '.', '')) <= :max_digits
        ) t
        WHERE rn = 1
    )
    SELECT
        "CNPJ_CIA",
        "DENOM_CIA",
        "SETOR_ATIV",
        "DT_REFER",
        "ANO_FISCAL",
        "CD_CONTA",
        "DS_CONTA",
        "VL_CONTA_TRATADO"
    FROM deduplicado
    ORDER BY "ANO_FISCAL", "CD_CONTA";
    """
    return _safe_read_sql(query, {"cnpj": cnpj, "max_digits": max_digits})


@st.cache_data(ttl=900)
def get_statement_highlights(statement_type: str, cnpj: str = COSAN_CNPJ):
    table_name = STATEMENT_TABLES[statement_type]
    codes = _quoted_csv(TOP_LEVEL_CODES[statement_type])
    query = f"""
    WITH deduplicado AS (
        SELECT *
        FROM (
            SELECT
                "CNPJ_CIA",
                "DT_FIM_EXERC_ANO"::integer AS "ANO_FISCAL",
                "CD_CONTA",
                "DS_CONTA",
                "VL_CONTA_TRATADO",
                "VERSAO",
                "DT_REFER"::date AS "DT_REFER",
                ROW_NUMBER() OVER (
                    PARTITION BY "CNPJ_CIA", "DT_FIM_EXERC_ANO", "CD_CONTA"
                    ORDER BY "VERSAO" DESC, "DT_REFER" DESC
                ) AS rn
            FROM "layer_02_silver"."{table_name}"
            WHERE "CNPJ_CIA" = :cnpj
              AND "DT_FIM_EXERC_ANO" IS NOT NULL
              AND "CD_CONTA" IN ({codes})
        ) t
        WHERE rn = 1
    )
    SELECT
        "ANO_FISCAL",
        "CD_CONTA",
        "DS_CONTA",
        "VL_CONTA_TRATADO"
    FROM deduplicado
    ORDER BY "ANO_FISCAL", "CD_CONTA";
    """
    return _safe_read_sql(query, {"cnpj": cnpj})


# ==============================================================================
# Gold mart / benchmark / IPRF queries
# ==============================================================================


def _read_available_years(cnpj: str | None = None) -> list[int]:
    if cnpj:
        query = """
        SELECT DISTINCT "ANO_FISCAL"
        FROM "layer_03_gold"."mart_indicadores_financeiros"
        WHERE "CNPJ_CIA" = :cnpj
          AND "ANO_FISCAL" IS NOT NULL
        ORDER BY "ANO_FISCAL" DESC;
        """
        df = _safe_read_sql(query, {"cnpj": cnpj})
    else:
        query = """
        SELECT DISTINCT "ANO_FISCAL"
        FROM "layer_03_gold"."mart_indicadores_financeiros"
        WHERE "ANO_FISCAL" IS NOT NULL
        ORDER BY "ANO_FISCAL" DESC;
        """
        df = _safe_read_sql(query)
    return df["ANO_FISCAL"].astype(int).tolist() if not df.empty else []


@st.cache_data(ttl=900)
def get_available_years():
    return _read_available_years()


@st.cache_data(ttl=900)
def get_company_available_years(cnpj: str = COSAN_CNPJ):
    return _read_available_years(cnpj)


@st.cache_data(ttl=900)
def get_companies_for_dashboard():
    query = """
    WITH base AS (
        SELECT
            "CNPJ_CIA",
            MAX("RAZAO_SOCIAL") AS "DENOM_CIA",
            MAX("SETOR") AS "SETOR"
        FROM "layer_03_gold"."mart_indicadores_financeiros"
        WHERE "CNPJ_CIA" IS NOT NULL
        GROUP BY "CNPJ_CIA"
    )
    SELECT
        "CNPJ_CIA",
        "DENOM_CIA",
        "SETOR"
    FROM base
    ORDER BY
        CASE WHEN "CNPJ_CIA" = :default_cnpj THEN 0 ELSE 1 END,
        "DENOM_CIA";
    """
    df = _safe_read_sql(query, {"default_cnpj": COSAN_CNPJ})
    if df.empty:
        return df
    df["LABEL"] = df["DENOM_CIA"] + " | " + df["CNPJ_CIA"]
    return df


@st.cache_data(ttl=900)
def get_company_sector_from_db(cnpj: str = COSAN_CNPJ) -> str:
    query = """
    SELECT "SETOR"
    FROM "layer_03_gold"."mart_indicadores_financeiros"
    WHERE "CNPJ_CIA" = :cnpj
      AND "SETOR" IS NOT NULL
    ORDER BY "ANO_FISCAL" DESC
    LIMIT 1;
    """
    df = _safe_read_sql(query, {"cnpj": cnpj})
    if not df.empty:
        return df.iloc[0]["SETOR"]
    return COSAN_SETOR


@st.cache_data(ttl=300)
def get_overview_history(cnpj: str = COSAN_CNPJ):
    query = """
    SELECT
        m."ANO_FISCAL",
        m."REC_LIQ",
        m."EBITDA",
        m."LUCRO_LIQ",
        m."DIVIDA_LIQUIDA",
        m."CAIXA_OPERACIONAL",
        i."SCORE_IPRF",
        b."MEDIANA_IPRF_SETOR_ANO"
    FROM "layer_03_gold"."mart_indicadores_financeiros" m
    LEFT JOIN "layer_03_gold"."vw_iprf_empresas_anual" i
      ON i."CNPJ_CIA" = m."CNPJ_CIA"
     AND i."ANO_FISCAL" = m."ANO_FISCAL"
    LEFT JOIN "layer_03_gold"."vw_benchmark_iprf_setorial" b
      ON b."CNPJ_CIA" = m."CNPJ_CIA"
     AND b."ANO_FISCAL" = m."ANO_FISCAL"
    WHERE m."CNPJ_CIA" = :cnpj
    ORDER BY m."ANO_FISCAL";
    """
    return _safe_read_sql(query, {"cnpj": cnpj})


@st.cache_data(ttl=300)
def get_overview_snapshot(year: int, cnpj: str = COSAN_CNPJ):
    query = """
    SELECT
        m.*,
        i."SCORE_IPRF",
        i."FAIXA_IPRF",
        b."MEDIANA_IPRF_SETOR_ANO",
        b."RANK_IPRF_SETOR_ANO",
        b."PERCENTIL_IPRF_SETOR_ANO"
    FROM "layer_03_gold"."mart_indicadores_financeiros" m
    LEFT JOIN "layer_03_gold"."vw_iprf_empresas_anual" i
      ON i."CNPJ_CIA" = m."CNPJ_CIA"
     AND i."ANO_FISCAL" = m."ANO_FISCAL"
    LEFT JOIN "layer_03_gold"."vw_benchmark_iprf_setorial" b
      ON b."CNPJ_CIA" = m."CNPJ_CIA"
     AND b."ANO_FISCAL" = m."ANO_FISCAL"
    WHERE m."CNPJ_CIA" = :cnpj
      AND m."ANO_FISCAL" = :year;
    """
    df = _safe_read_sql(query, {"cnpj": cnpj, "year": year})
    return df.iloc[0].to_dict() if not df.empty else {}


@st.cache_data(ttl=300)
def get_indicator_benchmark(year: int, cnpj: str = COSAN_CNPJ):
    query = """
    SELECT
        "CNPJ_CIA",
        "DENOM_CIA",
        "SETOR",
        "ANO_FISCAL",
        "COD_INDICADOR",
        "VL_INDICADOR",
        "MEDIANA_GERAL_ANO",
        "MEDIANA_SETOR_ANO",
        "DELTA_VS_GERAL",
        "DELTA_VS_SETOR"
    FROM "layer_03_gold"."vw_benchmark_indicadores_anual"
    WHERE "CNPJ_CIA" = :cnpj
      AND "ANO_FISCAL" = :year
    ORDER BY "COD_INDICADOR";
    """
    return _safe_read_sql(query, {"cnpj": cnpj, "year": year})


@st.cache_data(ttl=300)
def get_priority_indicator_history(cnpj: str = COSAN_CNPJ):
    codes = _quoted_csv(PRIORITY_INDICATOR_CODES)
    query = f"""
    SELECT
        "CNPJ_CIA",
        "DENOM_CIA",
        "SETOR",
        "ANO_FISCAL",
        "COD_INDICADOR",
        "VL_INDICADOR",
        "MEDIANA_GERAL_ANO",
        "MEDIANA_SETOR_ANO",
        "DELTA_VS_GERAL",
        "DELTA_VS_SETOR"
    FROM "layer_03_gold"."vw_benchmark_indicadores_anual"
    WHERE "CNPJ_CIA" = :cnpj
      AND "COD_INDICADOR" IN ({codes})
    ORDER BY "ANO_FISCAL", "COD_INDICADOR";
    """
    return _safe_read_sql(query, {"cnpj": cnpj})


@st.cache_data(ttl=300)
def get_indicator_detail_table(year: int, cnpj: str = COSAN_CNPJ):
    query = """
    SELECT *
    FROM "layer_03_gold"."vw_benchmark_indicadores_anual"
    WHERE "CNPJ_CIA" = :cnpj
      AND "ANO_FISCAL" = :year
    ORDER BY "COD_INDICADOR";
    """
    return _safe_read_sql(query, {"cnpj": cnpj, "year": year})


@st.cache_data(ttl=300)
def get_sector_indicator_ranking(year: int, indicator_code: str, sector: str | None = None):
    sector = sector or get_company_sector_from_db()
    query = """
    SELECT
        "CNPJ_CIA",
        "DENOM_CIA",
        "VL_INDICADOR"
    FROM "layer_03_gold"."vw_benchmark_indicadores_anual"
    WHERE "ANO_FISCAL" = :year
      AND "SETOR" = :sector
      AND "COD_INDICADOR" = :indicator_code
    ORDER BY "VL_INDICADOR" DESC NULLS LAST;
    """
    return _safe_read_sql(
        query,
        {
            "year": year,
            "sector": sector,
            "indicator_code": indicator_code,
        },
    )


@st.cache_data(ttl=300)
def get_iprf_history(cnpj: str = COSAN_CNPJ):
    query = """
    SELECT *
    FROM "layer_03_gold"."vw_iprf_empresas_anual"
    WHERE "CNPJ_CIA" = :cnpj
    ORDER BY "ANO_FISCAL";
    """
    return _safe_read_sql(query, {"cnpj": cnpj})


@st.cache_data(ttl=300)
def get_iprf_year_detail(year: int, cnpj: str = COSAN_CNPJ):
    query = """
    SELECT *
    FROM "layer_03_gold"."vw_iprf_empresas_anual"
    WHERE "CNPJ_CIA" = :cnpj
      AND "ANO_FISCAL" = :year;
    """
    df = _safe_read_sql(query, {"cnpj": cnpj, "year": year})
    return df.iloc[0].to_dict() if not df.empty else {}


@st.cache_data(ttl=300)
def get_iprf_sector_benchmark(year: int, cnpj: str = COSAN_CNPJ):
    query = """
    SELECT *
    FROM "layer_03_gold"."vw_benchmark_iprf_setorial"
    WHERE "CNPJ_CIA" = :cnpj
      AND "ANO_FISCAL" = :year;
    """
    df = _safe_read_sql(query, {"cnpj": cnpj, "year": year})
    return df.iloc[0].to_dict() if not df.empty else {}


@st.cache_data(ttl=300)
def get_iprf_sector_peers(year: int, sector: str | None = None):
    sector = sector or get_company_sector_from_db()
    query = """
    SELECT
        "CNPJ_CIA",
        "DENOM_CIA",
        "SETOR",
        "ANO_FISCAL",
        "SCORE_IPRF",
        "FAIXA_IPRF",
        "SCORE_LIQUIDEZ",
        "SCORE_RENTABILIDADE",
        "SCORE_SOLVENCIA",
        "SCORE_EFICIENCIA",
        "SCORE_GERACAO_CAIXA"
    FROM "layer_03_gold"."vw_iprf_empresas_anual"
    WHERE "SETOR" = :sector
      AND "ANO_FISCAL" = :year
    ORDER BY "SCORE_IPRF" DESC NULLS LAST, "DENOM_CIA";
    """
    return _safe_read_sql(query, {"sector": sector, "year": year})


def get_iprf_note_columns():
    return [item["note_code"] for item in IPRF_INDICATORS]


def get_iprf_indicator_codes():
    return [item["code"] for item in IPRF_INDICATORS]


def get_cosan_sector_from_db(cnpj: str = COSAN_CNPJ) -> str:
    return get_company_sector_from_db(cnpj)


@st.cache_data(ttl=900)
def get_company_reference(cnpj: str = COSAN_CNPJ):
    companies = get_companies_for_dashboard()
    if not companies.empty:
        match = companies[companies["CNPJ_CIA"] == cnpj]
        if not match.empty:
            row = match.iloc[0]
            return {
                "cnpj": row["CNPJ_CIA"],
                "nome": row["DENOM_CIA"],
                "setor": row["SETOR"] if pd.notna(row["SETOR"]) else COSAN_SETOR,
            }
    return {
        "cnpj": cnpj,
        "nome": COSAN_NAME if cnpj == COSAN_CNPJ else cnpj,
        "setor": get_company_sector_from_db(cnpj),
    }


def get_cosan_reference():
    return get_company_reference(COSAN_CNPJ)

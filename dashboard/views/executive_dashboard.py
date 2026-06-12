import html
import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from constants import (
    CLASSIC_INDICATOR_FORMATS,
    CLASSIC_INDICATOR_LABELS,
    CLASSIC_INDICATOR_TOOLTIPS,
    COSAN_CNPJ,
    COSAN_COLORS,
    IPRF_DIMENSION_SCORES,
    IPRF_INDICATORS,
    INDICATOR_META,
    PRIORITY_INDICATORS,
)
from database import (
    get_available_years,
    get_company_available_years,
    get_companies_for_dashboard,
    get_company_reference,
    get_cosan_reference,
    get_indicator_benchmark,
    get_indicator_detail_table,
    get_iprf_history,
    get_iprf_sector_benchmark,
    get_iprf_sector_peers,
    get_iprf_year_detail,
    get_overview_history,
    get_overview_snapshot,
    get_priority_indicator_history,
    get_sector_indicator_ranking,
    get_statement_data,
    get_statement_highlights,
)


STATEMENT_TITLES = {
    "BP": "Balanço Patrimonial",
    "DRE": "Demonstração do Resultado",
    "DFC": "Demonstração do Fluxo de Caixa",
}

HIGHLIGHT_LABELS = {
    "1": "Ativo Total",
    "1.01": "Ativo Circulante",
    "1.02": "Ativo Não Circulante",
    "2": "Passivo Total",
    "2.01": "Passivo Circulante",
    "2.02": "Passivo Não Circulante",
    "2.03": "Patrimônio Líquido",
    "3.01": "Receita Líquida",
    "3.03": "Lucro Bruto",
    "3.05": "EBIT",
    "3.11": "Lucro Líquido",
    "6.01": "Caixa Operacional",
    "6.02": "Caixa de Investimentos",
    "6.03": "Caixa de Financiamentos",
    "6.05.02": "Saldo Final de Caixa",
}

FILTER_HELP = {
    "ano_fiscal": "Seleciona o exercício anual da DFP usado como base para os KPIs, os comparativos e o IPRF.",
    "nivel_detalhe": "Controla até qual nível da hierarquia de contas da CVM o BP, a DRE e a DFC serão exibidos.",
    "grupo_indicadores": "Agrupa os indicadores prioritários por tema para facilitar a leitura executiva do setor.",
    "ranking_setorial": "Escolhe qual indicador será usado para posicionar a empresa entre os pares do mesmo setor no ano selecionado.",
}

SECTION_HELP = {
    "overview": "Resume a leitura anual da empresa combinando desempenho operacional, resultado e risco financeiro.",
    "BP": "Mostra a fotografia patrimonial no encerramento do exercício, com foco em ativos, passivos e patrimônio líquido.",
    "DRE": "Mostra o desempenho acumulado do exercício, da receita líquida ao lucro líquido.",
    "DFC": "Mostra a geração e o consumo de caixa do exercício nas frentes operacional, investimento e financiamento.",
    "indicadores": "Compara a empresa com a mediana de todas as companhias e com a mediana do seu setor para cada indicador clássico.",
    "iprf": "Apresenta o Índice de Prevenção ao Risco Financeiro, calculado em escala de 0 a 10 e comparado com empresas do mesmo setor.",
}

KPI_HELP = {
    "Receita Líquida": "Receita líquida anual reportada na DRE, usada como base para margens e indicadores de atividade.",
    "EBITDA": "Proxy anual de geração operacional antes de resultado financeiro, tributos, depreciação e amortização.",
    "Lucro Líquido": "Resultado consolidado do exercício após despesas financeiras, impostos e participações.",
    "Score IPRF": "Score final do IPRF em escala de 0 a 10. Quanto maior, melhor a percepção preventiva de risco financeiro.",
    "Classificação IPRF": "Faixa qualitativa do IPRF: Saudável, Moderado, Alerta ou Crítico.",
    "Classificação": "Faixa qualitativa do IPRF conforme o score final do exercício selecionado.",
}

IPRF_SECTION_HELP = {
    "gauge": "O gauge mostra o score final do IPRF e o delta contra a mediana do setor no mesmo ano.",
    "calculo": "Explica como o score final do IPRF é formado a partir das cinco dimensões ponderadas do modelo.",
    "dimensoes": "As cinco dimensões sintetizam liquidez, rentabilidade, solvência, eficiência e geração de caixa.",
    "notas": "Tabela com os 13 indicadores-base do IPRF, seus valores anuais e as notas provisórias de 0 a 10.",
    "pares": "Compara o score IPRF da empresa com os principais pares do mesmo setor no exercício selecionado.",
}

IPRF_INDICATOR_HELP = {
    "LIQ_CORRENTE": "Liquidez de curto prazo baseada em ativo circulante sobre passivo circulante.",
    "LIQ_SECA_AJUSTADA": "Liquidez de curto prazo desconsiderando estoques e considerando ajustes setoriais quando aplicáveis.",
    "COB_CAIXA_OPERACIONAL": "Capacidade de a geração operacional de caixa sustentar compromissos de curto prazo.",
    "MARGEM_EBITDA": "Parcela da receita líquida convertida em EBITDA.",
    "MARGEM_LIQUIDA": "Parcela da receita líquida convertida em lucro líquido.",
    "ROA": "Retorno sobre ativos totais.",
    "DL_EBITDA": "Número de anos de EBITDA necessários para cobrir a dívida líquida; menor tende a ser melhor.",
    "GRAU_ENDIVIDAMENTO": "Peso do endividamento na estrutura de capital da empresa.",
    "CCC": "Tempo total entre desembolso operacional e conversão desse desembolso em caixa.",
    "GIRO_ATIVO_TOTAL": "Eficiência da empresa em gerar receita a partir da base total de ativos.",
    "MARGEM_CAIXA_OPERACIONAL": "Parcela da receita líquida convertida em caixa operacional.",
    "COBERTURA_DIVIDA_CAIXA": "Capacidade do caixa operacional em cobrir a dívida da empresa.",
    "INTENSIDADE_REINVESTIMENTO": "Percentual do caixa operacional destinado a reinvestimento; no IPRF a interpretação usa faixa ótima, não apenas mais ou menos.",
}


def _inject_css(font_scale: float = 1.0):
    st.markdown(
        f"""
        <style>
        :root {{
            --dash-font-scale: {font_scale};
        }}
        .stApp {{
            background: linear-gradient(180deg, {COSAN_COLORS['bg']} 0%, #0f2740 100%);
            color: {COSAN_COLORS['text']};
            font-size: calc(1rem * var(--dash-font-scale));
            overflow: visible !important;
        }}
        [data-testid="stSidebar"] {{
            background: #071320;
            overflow: visible !important;
        }}
        [data-testid="stSidebar"] > div:first-child,
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"],
        [data-testid="stSidebar"] [data-testid="stElementContainer"],
        .block-container,
        [data-testid="stAppViewContainer"],
        [data-testid="stMainBlockContainer"],
        [data-testid="stVerticalBlock"],
        [data-testid="stHorizontalBlock"],
        [data-testid="column"],
        [data-testid="stMarkdownContainer"],
        [data-testid="element-container"] {{
            overflow: visible !important;
        }}
        h1 {{
            font-size: calc(2rem * var(--dash-font-scale)) !important;
        }}
        h2 {{
            font-size: calc(1.6rem * var(--dash-font-scale)) !important;
        }}
        h3 {{
            font-size: calc(1.25rem * var(--dash-font-scale)) !important;
        }}
        p, li, label, [data-testid="stCaptionContainer"], [data-testid="stSidebar"] * {{
            font-size: calc(0.98rem * var(--dash-font-scale));
        }}
        .stTabs [data-baseweb="tab"] {{
            font-size: calc(0.95rem * var(--dash-font-scale));
        }}
        [data-testid="stDataFrame"], [data-testid="stDataFrame"] * {{
            font-size: calc(0.92rem * var(--dash-font-scale));
        }}
        .block-container {{
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }}
        .cosan-hero {{
            background: linear-gradient(135deg, {COSAN_COLORS['card']} 0%, {COSAN_COLORS['card_alt']} 100%);
            border: 1px solid {COSAN_COLORS['line']};
            border-radius: 18px;
            padding: 20px 22px;
            margin-bottom: 1rem;
        }}
        .cosan-kpi {{
            background: {COSAN_COLORS['card']};
            border: 1px solid {COSAN_COLORS['line']};
            border-radius: 16px;
            padding: 16px 18px;
            min-height: 112px;
        }}
        .cosan-kpi-label {{
            color: {COSAN_COLORS['muted']};
            font-size: calc(0.78rem * var(--dash-font-scale));
            letter-spacing: 0.04rem;
            text-transform: uppercase;
        }}
        .cosan-kpi-value {{
            color: {COSAN_COLORS['text']};
            font-size: calc(1.7rem * var(--dash-font-scale));
            font-weight: 700;
            margin-top: 0.4rem;
        }}
        .cosan-kpi-sub {{
            color: {COSAN_COLORS['muted']};
            font-size: calc(0.82rem * var(--dash-font-scale));
            margin-top: 0.45rem;
        }}
        .cosan-section-card {{
            background: {COSAN_COLORS['card']};
            border: 1px solid {COSAN_COLORS['line']};
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 1rem;
        }}
        .cosan-pill {{
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 999px;
            font-size: calc(0.8rem * var(--dash-font-scale));
            font-weight: 700;
            margin-top: 0.6rem;
        }}
        .cosan-note {{
            color: {COSAN_COLORS['muted']};
            font-size: calc(0.9rem * var(--dash-font-scale));
        }}
        .cosan-info-row {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            margin: 0.15rem 0 0.25rem 0;
            overflow: visible !important;
        }}
        .cosan-info-label {{
            color: {COSAN_COLORS['text']};
            font-size: calc(0.95rem * var(--dash-font-scale));
            font-weight: 600;
        }}
        .cosan-tooltip {{
            position: relative;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 18px;
            height: 18px;
            border-radius: 999px;
            border: 1px solid {COSAN_COLORS['line']};
            background: rgba(0, 174, 186, 0.14);
            color: {COSAN_COLORS['teal']};
            font-size: calc(0.72rem * var(--dash-font-scale));
            font-weight: 700;
            cursor: help;
            z-index: 10001;
        }}
        .cosan-tooltip-text {{
            visibility: hidden;
            opacity: 0;
            width: 260px;
            background: #0b1726;
            color: {COSAN_COLORS['text']};
            text-align: left;
            border: 1px solid {COSAN_COLORS['line']};
            border-radius: 10px;
            padding: 10px 12px;
            position: absolute;
            z-index: 10002;
            top: 50%;
            left: calc(100% + 10px);
            right: auto;
            transform: translateY(-50%);
            font-size: calc(0.8rem * var(--dash-font-scale));
            font-weight: 400;
            line-height: 1.35;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
            overflow: visible !important;
        }}
        .cosan-tooltip:hover .cosan-tooltip-text {{
            visibility: visible;
            opacity: 1;
        }}
        @media (max-width: 960px) {{
            .cosan-tooltip-text {{
                top: calc(100% + 10px);
                left: 0;
                transform: none;
                width: min(260px, 78vw);
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _format_currency(value: float | int | None, short: bool = False) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "-"
    abs_value = abs(float(value))
    if short:
        if abs_value >= 1_000_000_000:
            return f"R$ {value / 1_000_000_000:.1f} bi"
        if abs_value >= 1_000_000:
            return f"R$ {value / 1_000_000:.1f} mi"
        if abs_value >= 1_000:
            return f"R$ {value / 1_000:.1f} mil"
    return f"R$ {value:,.0f}".replace(",", ".")


def _format_percent(value: float | int | None) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "-"
    return f"{value * 100:.3f}%"


def _format_ratio(value: float | int | None) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "-"
    return f"{value:.3f}"


def _format_number(value: float | int | None) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "-"
    return f"{value:.3f}"


def _format_days(value: float | int | None) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "-"
    return f"{value:.0f} dias"


def _format_score(value: float | int | None) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "-"
    return f"{value:.1f}"


def format_value(value, value_format: str, short: bool = False) -> str:
    if value_format == "currency":
        return _format_currency(value, short=short)
    if value_format == "pct":
        return _format_percent(value)
    if value_format == "ratio":
        return _format_ratio(value)
    if value_format == "days":
        return _format_days(value)
    if value_format == "score":
        return _format_score(value)
    if value_format == "number":
        return _format_number(value)
    return _format_number(value)


def _cnpj_token(cnpj: str) -> str:
    return "".join(char for char in cnpj if char.isdigit())


def _scaled_px(base_size: int) -> int:
    scale = float(st.session_state.get("dashboard_font_scale", 1.0))
    return max(10, int(round(base_size * scale)))


def _plotly_font(base_size: int = 13) -> dict:
    return {"color": COSAN_COLORS["text"], "size": _scaled_px(base_size)}


def _badge_for_risk(faixa: str | None) -> tuple[str, str]:
    faixa = (faixa or "").upper()
    if "SAUD" in faixa:
        return ("rgba(52, 211, 153, 0.13)", COSAN_COLORS["green"])
    if "MODER" in faixa:
        return ("rgba(245, 158, 11, 0.13)", COSAN_COLORS["amber"])
    if "ALERTA" in faixa:
        return ("rgba(251, 146, 60, 0.13)", "#FB923C")
    return ("rgba(239, 68, 68, 0.13)", COSAN_COLORS["red"])


def _statement_pivot(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    pivot = (
        df.pivot_table(
            index=["CD_CONTA", "DS_CONTA"],
            columns="ANO_FISCAL",
            values="VL_CONTA_TRATADO",
            aggfunc="first",
        )
        .reset_index()
        .sort_values("CD_CONTA")
    )
    pivot.columns = [str(col) if isinstance(col, int) else col for col in pivot.columns]
    return pivot


def _statement_download(df: pd.DataFrame, filename: str):
    if df.empty:
        return
    st.download_button(
        "Baixar CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
    )


def _tooltip_html(help_text: str) -> str:
    tooltip_html = html.escape(help_text).replace("\n", "<br>")
    return (
        '<span class="cosan-tooltip">i'
        f'<span class="cosan-tooltip-text">{tooltip_html}</span>'
        "</span>"
    )


def _indicator_label(code: str) -> str:
    return CLASSIC_INDICATOR_LABELS.get(code, INDICATOR_META.get(code, {}).get("label", code))


def _indicator_format(code: str) -> str:
    return CLASSIC_INDICATOR_FORMATS.get(code, INDICATOR_META.get(code, {}).get("format", "number"))


def _render_info_label(label: str, help_text: str):
    st.markdown(
        f"""
        <div class="cosan-info-row">
            <div class="cosan-info-label">{html.escape(label)}</div>
            {_tooltip_html(help_text)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_kpi_card(label: str, value: str, subtext: str = "", help_text: str | None = None):
    label_html = html.escape(label)
    if help_text:
        label_html = f"{label_html} {_tooltip_html(help_text)}"
    st.markdown(
        f"""
        <div class="cosan-kpi">
            <div class="cosan-kpi-label">{label_html}</div>
            <div class="cosan-kpi-value">{value}</div>
            <div class="cosan-kpi-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Legacy block kept only as fallback reference during final refinements.
# Active dashboard functions are the redefined versions later in this file.
def _legacy_render_overview_unused(tab, selected_year: int):
    history = get_overview_history()
    snapshot = get_overview_snapshot(selected_year)
    benchmark = get_iprf_sector_benchmark(selected_year)
    referencia = get_cosan_reference()

    with tab:
        st.markdown(
            f"""
            <div class="cosan-hero">
                <h2 style="margin:0;">{referencia['nome']}</h2>
                <div class="cosan-note">
                    Painel executivo anual com demonstrativos, benchmark por mediana e IPRF.
                </div>
                <div class="cosan-note" style="margin-top:0.5rem;">
                    CNPJ: {referencia['cnpj']} | Setor: {referencia['setor']} | Ano fiscal selecionado: {selected_year}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            _render_kpi_card(
                "Receita Líquida",
                _format_currency(snapshot.get("REC_LIQ"), short=True),
                f"Ano fiscal {selected_year}",
            )
        with col2:
            _render_kpi_card(
                "EBITDA",
                _format_currency(snapshot.get("EBITDA"), short=True),
                "Proxy anual para análise executiva",
            )
        with col3:
            _render_kpi_card(
                "Lucro Líquido",
                _format_currency(snapshot.get("LUCRO_LIQ"), short=True),
                "Resultado consolidado",
            )
        with col4:
            _render_kpi_card(
                "Score IPRF",
                _format_score(snapshot.get("SCORE_IPRF")),
                f"Faixa: {snapshot.get('FAIXA_IPRF', '-')}",
            )

        chart_col, side_col = st.columns([2.2, 1])
        with chart_col:
            if not history.empty:
                plot_df = history.copy()
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        x=plot_df["ANO_FISCAL"],
                        y=plot_df["REC_LIQ"],
                        name="Receita Líquida",
                        marker_color=COSAN_COLORS["lime"],
                        opacity=0.65,
                        yaxis="y1",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=plot_df["ANO_FISCAL"],
                        y=plot_df["EBITDA"],
                        name="EBITDA",
                        mode="lines+markers",
                        line={"color": COSAN_COLORS["teal"], "width": 3},
                        yaxis="y1",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=plot_df["ANO_FISCAL"],
                        y=plot_df["SCORE_IPRF"],
                        name="IPRF da Cosan",
                        mode="lines+markers",
                        line={"color": COSAN_COLORS["amber"], "width": 2},
                        yaxis="y2",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=plot_df["ANO_FISCAL"],
                        y=plot_df["MEDIANA_IPRF_SETOR_ANO"],
                        name="Mediana IPRF Setor",
                        mode="lines+markers",
                        line={"color": COSAN_COLORS["violet"], "width": 2, "dash": "dash"},
                        yaxis="y2",
                    )
                )
                fig.update_layout(
                    title="Histórico anual: desempenho financeiro e IPRF",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend={"orientation": "h", "y": 1.08},
                    yaxis={"title": "R$"},
                    yaxis2={
                        "title": "Score IPRF",
                        "overlaying": "y",
                        "side": "right",
                        "range": [0, 10],
                    },
                    font=_plotly_font(),
                    title_font_size=_scaled_px(18),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Histórico anual indisponível. Execute as queries da camada gold antes de abrir o dashboard.")

        with side_col:
            bg, color = _badge_for_risk(snapshot.get("FAIXA_IPRF"))
            st.markdown(
                f"""
                <div class="cosan-section-card">
                    <div class="cosan-kpi-label">Classificação IPRF</div>
                    <div class="cosan-kpi-value">{_format_score(snapshot.get("SCORE_IPRF"))}</div>
                    <span class="cosan-pill" style="background:{bg}; color:{color};">
                        {snapshot.get("FAIXA_IPRF", "Sem classificação")}
                    </span>
                    <div class="cosan-note" style="margin-top:0.8rem;">
                        Mediana setorial: {_format_score(benchmark.get("MEDIANA_IPRF_SETOR_ANO"))}
                    </div>
                    <div class="cosan-note">
                        Rank no setor: {benchmark.get("RANK_IPRF_SETOR_ANO", "-")}
                    </div>
                    <div class="cosan-note">
                        Percentil setorial: {benchmark.get("PERCENTIL_IPRF_SETOR_ANO", "-")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _legacy_render_statement_tab_unused(tab, statement_type: str, selected_year: int, max_level: int):
    statement_df = get_statement_data(statement_type, max_level=max_level)
    highlights_df = get_statement_highlights(statement_type)

    with tab:
        st.subheader(STATEMENT_TITLES[statement_type])
        st.caption(f"Tabela anual da {STATEMENT_TITLES[statement_type]} da Cosan, filtrada até o nível {max_level}.")

        if statement_df.empty:
            st.info("Sem dados disponíveis para este demonstrativo.")
            return

        pivot = _statement_pivot(statement_df)
        numeric_cols = [col for col in pivot.columns if col not in ["CD_CONTA", "DS_CONTA"]]
        styled = pivot.copy()
        for col in numeric_cols:
            styled[col] = styled[col].map(lambda value: _format_currency(value))

        table_col, chart_col = st.columns([1.3, 1])
        with table_col:
            st.dataframe(styled, use_container_width=True, hide_index=True, height=560)
            _statement_download(pivot, f"cosan_{statement_type.lower()}_anual.csv")

        with chart_col:
            if not highlights_df.empty:
                chart_df = highlights_df.copy()
                chart_df["LABEL"] = chart_df["CD_CONTA"].map(HIGHLIGHT_LABELS).fillna(chart_df["DS_CONTA"])
                fig = px.line(
                    chart_df,
                    x="ANO_FISCAL",
                    y="VL_CONTA_TRATADO",
                    color="LABEL",
                    markers=True,
                    title=f"Evolução anual - {STATEMENT_TITLES[statement_type]}",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=_plotly_font(),
                    title_font_size=_scaled_px(18),
                    legend_title_text="Conta",
                )
                st.plotly_chart(fig, use_container_width=True)

                selected_cols = chart_df[chart_df["ANO_FISCAL"] == selected_year].copy()
                if not selected_cols.empty:
                    selected_cols["ABS"] = selected_cols["VL_CONTA_TRATADO"].abs()
                    selected_cols = selected_cols.sort_values("ABS", ascending=False).head(6)
                    fig_bar = px.bar(
                        selected_cols,
                        x="LABEL",
                        y="VL_CONTA_TRATADO",
                        color="LABEL",
                        title=f"Composição principal em {selected_year}",
                    )
                    fig_bar.update_layout(
                        showlegend=False,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=_plotly_font(),
                        title_font_size=_scaled_px(18),
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)


def _prepare_indicator_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    meta_df = pd.DataFrame(PRIORITY_INDICATORS)
    merged = meta_df.merge(df, left_on="code", right_on="COD_INDICADOR", how="left")
    return merged


def _legacy_render_indicator_cards_unused(df: pd.DataFrame):
    cols = st.columns(3)
    for idx, row in df.reset_index(drop=True).iterrows():
        col = cols[idx % 3]
        with col:
            st.markdown(
                f"""
                <div class="cosan-kpi">
                    <div class="cosan-kpi-label">{row['label']}</div>
                    <div class="cosan-kpi-value">{format_value(row.get('VL_INDICADOR'), row['format'])}</div>
                    <div class="cosan-kpi-sub">
                        Setor: {format_value(row.get('MEDIANA_SETOR_ANO'), row['format'])} |
                        Geral: {format_value(row.get('MEDIANA_GERAL_ANO'), row['format'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_indicator_group_chart(df: pd.DataFrame, company_name: str):
    if df.empty:
        return
    chart_df = pd.DataFrame(
        {
            "Indicador": df["label"],
            company_name: df["VL_INDICADOR"],
            "Mediana Setor": df["MEDIANA_SETOR_ANO"],
            "Mediana Geral": df["MEDIANA_GERAL_ANO"],
        }
    ).melt(id_vars="Indicador", var_name="Serie", value_name="Valor")
    fig = px.bar(
        chart_df,
        x="Indicador",
        y="Valor",
        color="Serie",
        barmode="group",
        color_discrete_map={
            company_name: COSAN_COLORS["lime"],
            "Mediana Setor": COSAN_COLORS["teal"],
            "Mediana Geral": COSAN_COLORS["violet"],
        },
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=_plotly_font(),
        title_font_size=_scaled_px(18),
        legend={"orientation": "h", "y": 1.1},
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_sector_ranking(year: int, indicator_code: str, selected_cnpj: str, sector: str):
    indicator = INDICATOR_META[indicator_code]
    ranking_df = get_sector_indicator_ranking(year, indicator_code, sector)
    if ranking_df.empty:
        st.info("Ranking setorial indisponível.")
        return

    ascending = indicator["direction"] == "lower_better"
    ranking_df = ranking_df.sort_values("VL_INDICADOR", ascending=ascending).reset_index(drop=True)
    ranking_df["rank"] = ranking_df.index + 1
    ranking_df["cor"] = ranking_df["CNPJ_CIA"].apply(
        lambda value: COSAN_COLORS["amber"] if value == selected_cnpj else COSAN_COLORS["line"]
    )

    fig = px.bar(
        ranking_df.head(15),
        x="VL_INDICADOR",
        y="DENOM_CIA",
        orientation="h",
        color="DENOM_CIA",
        color_discrete_map={name: color for name, color in zip(ranking_df["DENOM_CIA"], ranking_df["cor"])},
        title=f"Ranking setorial - {indicator['label']} ({year})",
    )
    fig.update_layout(
        showlegend=False,
        yaxis={"autorange": "reversed"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=_plotly_font(),
        title_font_size=_scaled_px(18),
    )
    st.plotly_chart(fig, use_container_width=True)


def _legacy_render_indicators_unused(tab, selected_year: int):
    benchmark_df = get_indicator_benchmark(selected_year)
    detail_df = get_indicator_detail_table(selected_year)
    history_df = get_priority_indicator_history()

    with tab:
        st.subheader("Indicadores clássicos e benchmark por mediana")
        st.caption(
            "Comparação anual da Cosan com a mediana de todas as empresas e a mediana do setor Agricultura (Açúcar, Álcool e Cana)."
        )

        if benchmark_df.empty:
            st.info("Benchmark indisponível. Execute as views da camada gold para habilitar esta seção.")
            return

        priority_snapshot = _prepare_indicator_snapshot(benchmark_df)
        selected_group = st.selectbox(
            "Grupo prioritário",
            options=list(dict.fromkeys(item["group"] for item in PRIORITY_INDICATORS)),
        )

        selected_group_df = priority_snapshot[priority_snapshot["group"] == selected_group].copy()
        _render_indicator_cards(selected_group_df)

        chart_col, rank_col = st.columns([1.4, 1])
        with chart_col:
            _render_indicator_group_chart(selected_group_df, empresa_nome)
        with rank_col:
            selected_indicator = st.selectbox(
                "Indicador para ranking setorial",
                options=selected_group_df["code"].tolist(),
                format_func=lambda code: INDICATOR_META[code]["label"],
            )
            _render_sector_ranking(selected_year, selected_indicator)

        st.markdown("#### Histórico dos indicadores prioritários")
        if not history_df.empty:
            history_plot = history_df.merge(
                pd.DataFrame(PRIORITY_INDICATORS),
                left_on="COD_INDICADOR",
                right_on="code",
                how="left",
            )
            history_plot = history_plot[history_plot["group"] == selected_group]
            fig = px.line(
                history_plot,
                x="ANO_FISCAL",
                y="VL_INDICADOR",
                color="label",
                markers=True,
                title=f"Histórico anual - {selected_group}",
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=_plotly_font(),
                title_font_size=_scaled_px(18),
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Tabela detalhada")
        if not detail_df.empty:
            detail_df = detail_df.copy()
            detail_df["Indicador"] = detail_df["COD_INDICADOR"]
            detail_df["Valor Cosan"] = detail_df["VL_INDICADOR"]
            detail_df["Mediana Geral"] = detail_df["MEDIANA_GERAL_ANO"]
            detail_df["Mediana Setor"] = detail_df["MEDIANA_SETOR_ANO"]
            detail_df["Delta Geral"] = detail_df["DELTA_VS_GERAL"]
            detail_df["Delta Setor"] = detail_df["DELTA_VS_SETOR"]
            st.dataframe(
                detail_df[
                    [
                        "Indicador",
                        "Valor Cosan",
                        "Mediana Geral",
                        "Mediana Setor",
                        "Delta Geral",
                        "Delta Setor",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
                height=480,
            )
            _statement_download(detail_df, "cosan_benchmark_indicadores.csv")


def _render_iprf_gauge(score: float | None, sector_median: float | None):
    value = score if score is not None else 0
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            delta={"reference": sector_median or 0, "increasing": {"color": COSAN_COLORS["green"]}},
            gauge={
                "axis": {"range": [0, 10]},
                "bar": {"color": COSAN_COLORS["amber"]},
                "steps": [
                    {"range": [0, 3], "color": "rgba(239, 68, 68, 0.19)"},
                    {"range": [3, 5], "color": "rgba(251, 146, 60, 0.15)"},
                    {"range": [5, 7], "color": "rgba(245, 158, 11, 0.15)"},
                    {"range": [7, 10], "color": "rgba(52, 211, 153, 0.15)"},
                ],
                "threshold": {"line": {"color": COSAN_COLORS["lime"], "width": 4}, "value": sector_median or 0},
            },
            title={"text": "Score IPRF"},
        )
    )
    fig.update_layout(
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        font=_plotly_font(),
        title_font_size=_scaled_px(18),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_iprf_dimensions(detail: dict):
    rows = []
    for score_code, label in IPRF_DIMENSION_SCORES:
        rows.append({"Dimensao": label, "Score": detail.get(score_code)})
    df = pd.DataFrame(rows)
    fig = px.bar(
        df,
        x="Score",
        y="Dimensao",
        orientation="h",
        color="Dimensao",
        color_discrete_sequence=[
            COSAN_COLORS["teal"],
            COSAN_COLORS["violet"],
            COSAN_COLORS["amber"],
            COSAN_COLORS["lime"],
            COSAN_COLORS["green"],
        ],
        range_x=[0, 10],
    )
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=_plotly_font(),
        title_font_size=_scaled_px(18),
        yaxis={"autorange": "reversed"},
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_iprf_score_breakdown(detail: dict):
    weights = [
        ("SCORE_LIQUIDEZ", "Liquidez", 0.25),
        ("SCORE_RENTABILIDADE", "Rentabilidade", 0.25),
        ("SCORE_SOLVENCIA", "Solvencia", 0.20),
        ("SCORE_EFICIENCIA", "Eficiencia", 0.15),
        ("SCORE_GERACAO_CAIXA", "Geracao de Caixa", 0.15),
    ]
    st.markdown(
        """
        <div class="cosan-section-card">
            <div class="cosan-kpi-label">Formula do score final</div>
            <div class="cosan-note" style="margin-top:0.7rem; line-height:1.6;">
                <strong>IPRF = 0,25 x Liquidez + 0,25 x Rentabilidade + 0,20 x Solvencia + 0,15 x Eficiencia + 0,15 x Geracao de Caixa</strong>
            </div>
            <div class="cosan-note" style="margin-top:0.7rem;">
                Cada dimensao recebe uma nota de 0 a 10 a partir dos 13 indicadores-base. O score final e a soma ponderada dessas cinco dimensoes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(weights))
    contribution_rows = []
    weighted_total = 0.0
    has_any_score = False

    for idx, (score_code, label, weight) in enumerate(weights):
        score_value = detail.get(score_code)
        contribution = None if score_value is None else score_value * weight
        if contribution is not None:
            weighted_total += contribution
            has_any_score = True

        contribution_rows.append(
            {
                "Dimensao": label,
                "Peso": f"{weight:.0%}",
                "Score": format_value(score_value, "score"),
                "Contribuicao": "-" if contribution is None else f"{contribution:.3f}",
            }
        )

        with cols[idx]:
            _render_kpi_card(
                label,
                format_value(score_value, "score"),
                f"Peso: {weight:.0%} | Contribuicao: {'-' if contribution is None else f'{contribution:.3f}'}",
            )

    table_col, total_col = st.columns([1.4, 1])
    with table_col:
        st.dataframe(pd.DataFrame(contribution_rows), use_container_width=True, hide_index=True)
    with total_col:
        _render_kpi_card(
            "Score final pela formula",
            "-" if not has_any_score else f"{weighted_total:.3f}",
            "Soma ponderada das cinco dimensoes.",
            "Ajuda a conferir como o score final do IPRF foi composto no ano selecionado.",
        )


def _legacy_render_iprf_indicator_table_unused(detail: dict):
    rows = []
    for item in IPRF_INDICATORS:
        rows.append(
            {
                "Dimensao": item["dimension"],
                "Indicador": item["label"],
                "Valor Base": format_value(detail.get(item["code"]), item["format"]),
                "Nota 0-10": format_value(detail.get(item["note_code"]), "score"),
            }
        )
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True, height=460)


def _render_iprf_peers(peers_df: pd.DataFrame, selected_cnpj: str):
    if peers_df.empty:
        st.info("Comparativo setorial do IPRF indisponível.")
        return

    peers_df = peers_df.copy()
    peers_df["Cor"] = peers_df["CNPJ_CIA"].apply(
        lambda value: COSAN_COLORS["amber"] if value == selected_cnpj else COSAN_COLORS["line"]
    )
    fig = px.bar(
        peers_df.head(20),
        x="SCORE_IPRF",
        y="DENOM_CIA",
        orientation="h",
        color="DENOM_CIA",
        color_discrete_map={name: color for name, color in zip(peers_df["DENOM_CIA"], peers_df["Cor"])},
        title="Comparativo setorial do IPRF",
    )
    fig.update_layout(
        showlegend=False,
        yaxis={"autorange": "reversed"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=_plotly_font(),
        title_font_size=_scaled_px(18),
    )
    st.plotly_chart(fig, use_container_width=True)


def _legacy_render_iprf_unused(tab, selected_year: int):
    history_df = get_iprf_history()
    detail = get_iprf_year_detail(selected_year)
    benchmark = get_iprf_sector_benchmark(selected_year)
    peers_df = get_iprf_sector_peers(selected_year)

    with tab:
        st.subheader("Índice de Prevenção ao Risco Financeiro")
        st.caption(
            "Score anual da Cosan comparado apenas com empresas do mesmo setor. As notas de 0 a 10 estão em configuração provisória até a definição final das faixas."
        )

        if not detail:
            st.info("IPRF indisponível. Execute a view anual do IPRF na camada gold.")
            return

        top_col, side_col = st.columns([1.3, 1])
        with top_col:
            _render_iprf_gauge(detail.get("SCORE_IPRF"), benchmark.get("MEDIANA_IPRF_SETOR_ANO"))
        with side_col:
            bg, color = _badge_for_risk(detail.get("FAIXA_IPRF"))
            st.markdown(
                f"""
                <div class="cosan-section-card">
                    <div class="cosan-kpi-label">Classificação</div>
                    <div class="cosan-kpi-value">{format_value(detail.get('SCORE_IPRF'), 'score')}</div>
                    <span class="cosan-pill" style="background:{bg}; color:{color};">
                        {detail.get('FAIXA_IPRF', '-')}
                    </span>
                    <div class="cosan-note" style="margin-top:0.8rem;">
                        Mediana do setor: {format_value(benchmark.get('MEDIANA_IPRF_SETOR_ANO'), 'score')}
                    </div>
                    <div class="cosan-note">
                        Rank setorial: {benchmark.get('RANK_IPRF_SETOR_ANO', '-')}
                    </div>
                    <div class="cosan-note">
                        Percentil setorial: {benchmark.get('PERCENTIL_IPRF_SETOR_ANO', '-')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        dim_col, peers_col = st.columns([1, 1.2])
        with dim_col:
            st.markdown("#### Scores por dimensão")
            _render_iprf_dimensions(detail)
        with peers_col:
            _render_iprf_peers(peers_df)

        history_col, table_col = st.columns([1, 1.1])
        with history_col:
            if not history_df.empty:
                fig = px.line(
                    history_df,
                    x="ANO_FISCAL",
                    y=["SCORE_IPRF", "SCORE_LIQUIDEZ", "SCORE_RENTABILIDADE", "SCORE_SOLVENCIA"],
                    markers=True,
                    title="Histórico do IPRF e dimensões",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=_plotly_font(),
                    title_font_size=_scaled_px(18),
                    yaxis={"range": [0, 10]},
                )
                st.plotly_chart(fig, use_container_width=True)
        with table_col:
            st.markdown("#### Notas dos 13 indicadores")
            _render_iprf_indicator_table(detail)


def _legacy_render_executive_dashboard_unused():
    _inject_css()
    referencia = get_cosan_reference()
    years = get_available_years()

    with st.sidebar:
        st.title("Dashboard Executivo")
        st.caption("Projeto final com DFP anual, benchmark por mediana e IPRF")
        st.markdown("---")
        st.write(f"**Empresa:** {referencia['nome']}")
        st.write(f"**CNPJ:** {referencia['cnpj']}")
        st.write(f"**Setor:** {referencia['setor']}")
        st.markdown("---")

        if years:
            selected_year = st.selectbox("Ano fiscal", options=years, index=0)
        else:
            selected_year = None
        max_level = st.slider("Nível de detalhe dos demonstrativos", 1, 5, 3)

    st.title("Dashboard Final da Cosan com Benchmark e IPRF")
    st.caption(
        "Painel anual da Cosan com demonstrativos, indicadores clássicos e comparativos com a base completa e com o setor agrícola."
    )

    if selected_year is None:
        st.warning("Nenhum ano fiscal foi encontrado na camada gold. Execute as consultas do schema layer_03_gold e recarregue o aplicativo.")
        return

    tabs = st.tabs(["Visão Geral", "BP", "DRE", "DFC", "Indicadores", "IPRF"])
    _render_overview(tabs[0], selected_year)
    _render_statement_tab(tabs[1], "BP", selected_year, max_level)
    _render_statement_tab(tabs[2], "DRE", selected_year, max_level)
    _render_statement_tab(tabs[3], "DFC", selected_year, max_level)
    _render_indicators(tabs[4], selected_year)
    _render_iprf(tabs[5], selected_year)


def _render_overview(tab, selected_year: int, referencia: dict):
    history = get_overview_history(referencia["cnpj"])
    snapshot = get_overview_snapshot(selected_year, referencia["cnpj"])
    benchmark = get_iprf_sector_benchmark(selected_year, referencia["cnpj"])
    empresa_nome = referencia["nome"]

    with tab:
        st.markdown(
            f"""
            <div class="cosan-hero">
                <h2 style="margin:0;">{empresa_nome}</h2>
                <div class="cosan-note">
                    Painel executivo anual com demonstrativos, benchmark por mediana e IPRF.
                </div>
                <div class="cosan-note" style="margin-top:0.5rem;">
                    CNPJ: {referencia['cnpj']} | Setor: {referencia['setor']} | Ano fiscal selecionado: {selected_year}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            _render_kpi_card(
                "Receita Líquida",
                _format_currency(snapshot.get("REC_LIQ"), short=True),
                f"Ano fiscal {selected_year}",
                KPI_HELP["Receita Líquida"],
            )
        with col2:
            _render_kpi_card(
                "EBITDA",
                _format_currency(snapshot.get("EBITDA"), short=True),
                "Proxy anual para análise executiva",
                KPI_HELP["EBITDA"],
            )
        with col3:
            _render_kpi_card(
                "Lucro Líquido",
                _format_currency(snapshot.get("LUCRO_LIQ"), short=True),
                "Resultado consolidado",
                KPI_HELP["Lucro Líquido"],
            )
        with col4:
            _render_kpi_card(
                "Score IPRF",
                _format_score(snapshot.get("SCORE_IPRF")),
                f"Faixa: {snapshot.get('FAIXA_IPRF', '-')}",
                KPI_HELP["Score IPRF"],
            )

        chart_col, side_col = st.columns([2.2, 1])
        with chart_col:
            _render_info_label("Leitura do painel anual", SECTION_HELP["overview"])
            if not history.empty:
                plot_df = history.copy()
                fig = go.Figure()
                fig.add_trace(
                    go.Bar(
                        x=plot_df["ANO_FISCAL"],
                        y=plot_df["REC_LIQ"],
                        name="Receita Líquida",
                        marker_color=COSAN_COLORS["lime"],
                        opacity=0.65,
                        yaxis="y1",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=plot_df["ANO_FISCAL"],
                        y=plot_df["EBITDA"],
                        name="EBITDA",
                        mode="lines+markers",
                        line={"color": COSAN_COLORS["teal"], "width": 3},
                        yaxis="y1",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=plot_df["ANO_FISCAL"],
                        y=plot_df["SCORE_IPRF"],
                        name=f"IPRF de {empresa_nome}",
                        mode="lines+markers",
                        line={"color": COSAN_COLORS["amber"], "width": 2},
                        yaxis="y2",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=plot_df["ANO_FISCAL"],
                        y=plot_df["MEDIANA_IPRF_SETOR_ANO"],
                        name="Mediana IPRF do setor",
                        mode="lines+markers",
                        line={"color": COSAN_COLORS["violet"], "width": 2, "dash": "dash"},
                        yaxis="y2",
                    )
                )
                fig.update_layout(
                    title="Histórico anual: desempenho financeiro e IPRF",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend={"orientation": "h", "y": 1.08},
                    yaxis={"title": "R$"},
                    yaxis2={
                        "title": "Score IPRF",
                        "overlaying": "y",
                        "side": "right",
                        "range": [0, 10],
                    },
                    font={"color": COSAN_COLORS["text"]},
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Histórico anual indisponível. Execute as queries da camada gold antes de abrir o dashboard.")

        with side_col:
            bg, color = _badge_for_risk(snapshot.get("FAIXA_IPRF"))
            st.markdown(
                f"""
                <div class="cosan-section-card">
                    <div class="cosan-kpi-label">Classificação IPRF {_tooltip_html(KPI_HELP["Classificação IPRF"])}</div>
                    <div class="cosan-kpi-value">{_format_score(snapshot.get("SCORE_IPRF"))}</div>
                    <span class="cosan-pill" style="background:{bg}; color:{color};">
                        {snapshot.get("FAIXA_IPRF", "Sem classificação")}
                    </span>
                    <div class="cosan-note" style="margin-top:0.8rem;">
                        Mediana setorial: {_format_score(benchmark.get("MEDIANA_IPRF_SETOR_ANO"))}
                    </div>
                    <div class="cosan-note">
                        Rank no setor: {benchmark.get("RANK_IPRF_SETOR_ANO", "-")}
                    </div>
                    <div class="cosan-note">
                        Percentil setorial: {benchmark.get("PERCENTIL_IPRF_SETOR_ANO", "-")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_statement_tab(tab, statement_type: str, selected_year: int, max_level: int, referencia: dict):
    statement_titles = {
        "BP": "Balanço Patrimonial",
        "DRE": "Demonstração do Resultado",
        "DFC": "Demonstração do Fluxo de Caixa",
    }
    statement_df = get_statement_data(statement_type, cnpj=referencia["cnpj"], max_level=max_level)
    highlights_df = get_statement_highlights(statement_type, cnpj=referencia["cnpj"])
    empresa_nome = referencia["nome"]

    with tab:
        _render_info_label(statement_titles[statement_type], SECTION_HELP[statement_type])
        st.caption(f"Tabela anual de {statement_titles[statement_type]} de {empresa_nome}, filtrada até o nível {max_level}.")

        if statement_df.empty:
            st.info("Sem dados disponíveis para este demonstrativo.")
            return

        pivot = _statement_pivot(statement_df)
        numeric_cols = [col for col in pivot.columns if col not in ["CD_CONTA", "DS_CONTA"]]
        styled = pivot.copy()
        for col in numeric_cols:
            styled[col] = styled[col].map(lambda value: _format_currency(value))

        table_col, chart_col = st.columns([1.3, 1])
        with table_col:
            _render_info_label(
                "Tabela anual",
                "Exibe as contas consolidadas por ano fiscal, respeitando o nível de detalhamento escolhido no filtro lateral.",
            )
            st.dataframe(styled, use_container_width=True, hide_index=True, height=560)
            _statement_download(pivot, f"{_cnpj_token(referencia['cnpj'])}_{statement_type.lower()}_anual.csv")

        with chart_col:
            if not highlights_df.empty:
                _render_info_label(
                    "Destaques do demonstrativo",
                    "Os gráficos destacam as contas mais relevantes para leitura executiva da evolução e da composição anual.",
                )
                chart_df = highlights_df.copy()
                chart_df["LABEL"] = chart_df["CD_CONTA"].map(HIGHLIGHT_LABELS).fillna(chart_df["DS_CONTA"])
                fig = px.line(
                    chart_df,
                    x="ANO_FISCAL",
                    y="VL_CONTA_TRATADO",
                    color="LABEL",
                    markers=True,
                    title=f"Evolução anual - {statement_titles[statement_type]}",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={"color": COSAN_COLORS["text"]},
                    legend_title_text="Conta",
                )
                st.plotly_chart(fig, use_container_width=True)

                selected_cols = chart_df[chart_df["ANO_FISCAL"] == selected_year].copy()
                if not selected_cols.empty:
                    selected_cols["ABS"] = selected_cols["VL_CONTA_TRATADO"].abs()
                    selected_cols = selected_cols.sort_values("ABS", ascending=False).head(6)
                    fig_bar = px.bar(
                        selected_cols,
                        x="LABEL",
                        y="VL_CONTA_TRATADO",
                        color="LABEL",
                        title=f"Composição principal em {selected_year}",
                    )
                    fig_bar.update_layout(
                        showlegend=False,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={"color": COSAN_COLORS["text"]},
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)


def _render_indicator_cards(df: pd.DataFrame):
    cols = st.columns(3)
    for idx, row in df.reset_index(drop=True).iterrows():
        col = cols[idx % 3]
        with col:
            help_text = CLASSIC_INDICATOR_TOOLTIPS.get(
                row["code"],
                "Objetivo: indicador prioritário do painel executivo.\nCálculo: consulte a documentação da camada gold.\nAnálise: compare com a mediana geral e setorial.",
            )
            st.markdown(
                f"""
                <div class="cosan-kpi">
                    <div class="cosan-kpi-label">{html.escape(row['label'])} {_tooltip_html(help_text)}</div>
                    <div class="cosan-kpi-value">{format_value(row.get('VL_INDICADOR'), row['format'])}</div>
                    <div class="cosan-kpi-sub">
                        Setor: {format_value(row.get('MEDIANA_SETOR_ANO'), row['format'])} |
                        Geral: {format_value(row.get('MEDIANA_GERAL_ANO'), row['format'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_indicators(tab, selected_year: int, referencia: dict):
    benchmark_df = get_indicator_benchmark(selected_year, referencia["cnpj"])
    detail_df = get_indicator_detail_table(selected_year, referencia["cnpj"])
    history_df = get_priority_indicator_history(referencia["cnpj"])
    empresa_nome = referencia["nome"]
    setor_nome = referencia["setor"]

    with tab:
        _render_info_label("Indicadores clássicos e benchmark por mediana", SECTION_HELP["indicadores"])
        st.caption(
            f"Comparação anual de {empresa_nome} com a mediana de todas as empresas e a mediana do setor {setor_nome}."
        )

        if benchmark_df.empty:
            st.info("Benchmark indisponível. Execute as views da camada gold para habilitar esta seção.")
            return

        priority_snapshot = _prepare_indicator_snapshot(benchmark_df)
        _render_info_label("Grupo prioritário", FILTER_HELP["grupo_indicadores"])
        selected_group = st.selectbox(
            "Grupo prioritário",
            options=list(dict.fromkeys(item["group"] for item in PRIORITY_INDICATORS)),
            label_visibility="collapsed",
        )

        selected_group_df = priority_snapshot[priority_snapshot["group"] == selected_group].copy()
        if selected_group_df.empty:
            st.info(f"Não há indicadores calculados para {empresa_nome} no grupo {selected_group} em {selected_year}.")
            return
        _render_indicator_cards(selected_group_df)

        chart_col, rank_col = st.columns([1.4, 1])
        with chart_col:
            _render_indicator_group_chart(selected_group_df, empresa_nome)
        with rank_col:
            _render_info_label("Indicador para ranking setorial", FILTER_HELP["ranking_setorial"])
            selected_indicator = st.selectbox(
                "Indicador para ranking setorial",
                options=selected_group_df["code"].tolist(),
                format_func=lambda code: INDICATOR_META[code]["label"],
                label_visibility="collapsed",
            )
            _render_sector_ranking(selected_year, selected_indicator, referencia["cnpj"], referencia["setor"])

        _render_info_label(
            "Histórico dos indicadores prioritários",
            "Mostra a evolução anual dos indicadores do grupo selecionado para apoiar a análise de tendência.",
        )
        if not history_df.empty:
            history_plot = history_df.merge(
                pd.DataFrame(PRIORITY_INDICATORS),
                left_on="COD_INDICADOR",
                right_on="code",
                how="left",
            )
            history_plot = history_plot[history_plot["group"] == selected_group]
            fig = px.line(
                history_plot,
                x="ANO_FISCAL",
                y="VL_INDICADOR",
                color="label",
                markers=True,
                title=f"Histórico anual de {empresa_nome} - {selected_group}",
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": COSAN_COLORS["text"]},
            )
            st.plotly_chart(fig, use_container_width=True)

        _render_info_label(
            "Tabela detalhada",
            "Reúne os indicadores calculados na gold, incluindo valor da empresa, medianas anual geral e setorial, além dos deltas comparativos.",
        )
        if not detail_df.empty:
            detail_df = detail_df.copy()
            detail_df["Indicador"] = detail_df["COD_INDICADOR"].map(_indicator_label)
            detail_df["FORMATO_INDICADOR"] = detail_df["COD_INDICADOR"].map(_indicator_format)
            detail_df["Valor Empresa"] = detail_df.apply(
                lambda row: format_value(row["VL_INDICADOR"], row["FORMATO_INDICADOR"]),
                axis=1,
            )
            detail_df["Mediana Geral"] = detail_df.apply(
                lambda row: format_value(row["MEDIANA_GERAL_ANO"], row["FORMATO_INDICADOR"]),
                axis=1,
            )
            detail_df["Mediana Setor"] = detail_df.apply(
                lambda row: format_value(row["MEDIANA_SETOR_ANO"], row["FORMATO_INDICADOR"]),
                axis=1,
            )
            detail_df["Delta Geral"] = detail_df.apply(
                lambda row: format_value(row["DELTA_VS_GERAL"], row["FORMATO_INDICADOR"]),
                axis=1,
            )
            detail_df["Delta Setor"] = detail_df.apply(
                lambda row: format_value(row["DELTA_VS_SETOR"], row["FORMATO_INDICADOR"]),
                axis=1,
            )
            st.dataframe(
                detail_df[
                    [
                        "Indicador",
                        "Valor Empresa",
                        "Mediana Geral",
                        "Mediana Setor",
                        "Delta Geral",
                        "Delta Setor",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
                height=480,
            )
            _statement_download(detail_df, f"{_cnpj_token(referencia['cnpj'])}_benchmark_indicadores.csv")


def _render_iprf_indicator_table(detail: dict):
    rows = []
    for item in IPRF_INDICATORS:
        rows.append(
            {
                "Dimensão": item["dimension"],
                "Indicador": item["label"],
                "Valor Base": format_value(detail.get(item["code"]), item["format"]),
                "Nota 0-10": format_value(detail.get(item["note_code"]), "score"),
                "Contexto": IPRF_INDICATOR_HELP.get(item["code"], ""),
            }
        )
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True, height=460)


def _render_iprf(tab, selected_year: int, referencia: dict):
    history_df = get_iprf_history(referencia["cnpj"])
    detail = get_iprf_year_detail(selected_year, referencia["cnpj"])
    benchmark = get_iprf_sector_benchmark(selected_year, referencia["cnpj"])
    peers_df = get_iprf_sector_peers(selected_year, referencia["setor"])
    empresa_nome = referencia["nome"]

    with tab:
        _render_info_label("Índice de Prevenção ao Risco Financeiro", SECTION_HELP["iprf"])
        st.caption(
            f"Score anual de {empresa_nome} comparado apenas com empresas do mesmo setor. As notas de 0 a 10 estão em configuração provisória até a definição final das faixas."
        )

        if not detail:
            st.info("IPRF indisponível. Execute a view anual do IPRF na camada gold.")
            return

        top_col, side_col = st.columns([1.3, 1])
        with top_col:
            _render_info_label("Gauge do IPRF", IPRF_SECTION_HELP["gauge"])
            _render_iprf_gauge(detail.get("SCORE_IPRF"), benchmark.get("MEDIANA_IPRF_SETOR_ANO"))
        with side_col:
            bg, color = _badge_for_risk(detail.get("FAIXA_IPRF"))
            st.markdown(
                f"""
                <div class="cosan-section-card">
                    <div class="cosan-kpi-label">Classificação {_tooltip_html(KPI_HELP["Classificação"])}</div>
                    <div class="cosan-kpi-value">{format_value(detail.get('SCORE_IPRF'), 'score')}</div>
                    <span class="cosan-pill" style="background:{bg}; color:{color};">
                        {detail.get('FAIXA_IPRF', '-')}
                    </span>
                    <div class="cosan-note" style="margin-top:0.8rem;">
                        Mediana do setor: {format_value(benchmark.get('MEDIANA_IPRF_SETOR_ANO'), 'score')}
                    </div>
                    <div class="cosan-note">
                        Rank setorial: {benchmark.get('RANK_IPRF_SETOR_ANO', '-')}
                    </div>
                    <div class="cosan-note">
                        Percentil setorial: {benchmark.get('PERCENTIL_IPRF_SETOR_ANO', '-')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        dim_col, peers_col = st.columns([1, 1.2])
        with dim_col:
            _render_info_label("Scores por dimensão", IPRF_SECTION_HELP["dimensoes"])
            _render_iprf_dimensions(detail)
        with peers_col:
            _render_info_label("Comparativo setorial do IPRF", IPRF_SECTION_HELP["pares"])
            _render_iprf_peers(peers_df, referencia["cnpj"])

        _render_info_label("Como o score e calculado", IPRF_SECTION_HELP["calculo"])
        _render_iprf_score_breakdown(detail)

        history_col, table_col = st.columns([1, 1.1])
        with history_col:
            if not history_df.empty:
                fig = px.line(
                    history_df,
                    x="ANO_FISCAL",
                    y=["SCORE_IPRF", "SCORE_LIQUIDEZ", "SCORE_RENTABILIDADE", "SCORE_SOLVENCIA"],
                    markers=True,
                    title="Histórico do IPRF e dimensões",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=_plotly_font(),
                    title_font_size=_scaled_px(18),
                    yaxis={"range": [0, 10]},
                )
                st.plotly_chart(fig, use_container_width=True)
        with table_col:
            _render_info_label("Notas dos 13 indicadores", IPRF_SECTION_HELP["notas"])
            _render_iprf_indicator_table(detail)


def render_executive_dashboard():
    empresas_df = get_companies_for_dashboard()
    if empresas_df.empty:
        st.warning("Nenhuma empresa disponível na camada gold. Execute as consultas do schema layer_03_gold e recarregue o aplicativo.")
        return

    company_options = empresas_df["LABEL"].tolist()
    default_index = 0
    default_matches = empresas_df.index[empresas_df["CNPJ_CIA"] == COSAN_CNPJ].tolist()
    if default_matches:
        default_index = int(default_matches[0])

    selected_label = company_options[default_index]

    years = get_available_years()

    with st.sidebar:
        st.title("Dashboard Executivo")
        st.caption("Projeto final com DFP anual, benchmark por mediana e IPRF")
        st.markdown("---")
        _render_info_label("Empresa", "Selecione a companhia que será analisada. A Cosan permanece como padrão inicial.")
        selected_label = st.selectbox(
            "Empresa",
            options=company_options,
            index=default_index,
            label_visibility="collapsed",
        )
        selected_row = empresas_df.loc[empresas_df["LABEL"] == selected_label].iloc[0]
        referencia = get_company_reference(selected_row["CNPJ_CIA"])
        company_years = set(get_company_available_years(referencia["cnpj"]))
        preferred_year = next((year for year in years if year in company_years), years[0]) if years else None
        st.write(f"**Empresa:** {referencia['nome']}")
        st.write(f"**CNPJ:** {referencia['cnpj']}")
        st.write(f"**Setor:** {referencia['setor']}")
        st.markdown("---")

        if years:
            year_options = []
            year_lookup = {}
            for year in years:
                if year in company_years:
                    label = f"{year} | disponível para a empresa"
                else:
                    label = f"{year} | apenas base consolidada"
                year_options.append(label)
                year_lookup[label] = year

            preferred_label = next(
                (
                    label
                    for label in year_options
                    if year_lookup[label] == preferred_year
                ),
                year_options[0],
            )
            year_index = year_options.index(preferred_label)

            _render_info_label("Ano fiscal", FILTER_HELP["ano_fiscal"])
            selected_year_label = st.selectbox(
                "Ano fiscal",
                options=year_options,
                index=year_index,
                label_visibility="collapsed",
            )
            selected_year = year_lookup[selected_year_label]
            anos_empresa = ", ".join(str(year) for year in years if year in company_years)
            anos_base = ", ".join(str(year) for year in years if year not in company_years)
            st.caption(f"Fechamentos anuais disponíveis para a empresa: {anos_empresa or '-'}")
            if anos_base:
                st.caption(f"Anos adicionais presentes apenas na base consolidada: {anos_base}")
        else:
            selected_year = None

        _render_info_label("Nível de detalhe dos demonstrativos", FILTER_HELP["nivel_detalhe"])
        max_level = st.slider("Nível de detalhe dos demonstrativos", 1, 5, 3, label_visibility="collapsed")

        _render_info_label("Tamanho da fonte", "Ajusta a tipografia do dashboard e dos gráficos para facilitar a leitura na apresentação.")
        font_scale = st.slider(
            "Tamanho da fonte",
            min_value=0.85,
            max_value=1.70,
            value=float(st.session_state.get("dashboard_font_scale", 1.0)),
            step=0.05,
            format="%.2fx",
            label_visibility="collapsed",
            key="dashboard_font_scale",
        )

    _inject_css(font_scale)

    st.title(f"Dashboard Final de {referencia['nome']} com Benchmark e IPRF")
    st.caption(
        f"Painel anual de {referencia['nome']} com demonstrativos, indicadores clássicos e comparativos com a base completa e com o setor {referencia['setor']}."
    )
    with st.expander("Como navegar no painel"):
        st.markdown(
            "\n".join(
                [
                    "- `Visão Geral`: comece pelos KPIs e pelo resumo do histórico anual.",
                    "- `Indicadores`: compare a empresa com a mediana geral e a mediana do setor.",
                    "- `IPRF`: finalize a leitura com risco financeiro, ranking e pares setoriais.",
                    "- `BP`, `DRE` e `DFC`: use os demonstrativos como aprofundamento e validação do racional.",
                ]
            )
        )

    if selected_year is None:
        st.warning("Nenhum ano fiscal foi encontrado na camada gold. Execute as consultas do schema layer_03_gold e recarregue o aplicativo.")
        return

    if selected_year not in company_years:
        st.warning(
            f"O ano {selected_year} aparece no filtro porque existe na base consolidada do projeto, mas não há fechamento anual de {referencia['nome']} "
            f"carregado com `ANO_FISCAL = {selected_year}`. Em outras palavras: o dashboard consegue enxergar {selected_year} para o mercado, "
            f"mas não para esta empresa específica. Por isso, comparativos gerais podem existir, enquanto os blocos próprios da empresa podem ficar vazios."
        )

    tabs = st.tabs(["Visão Geral", "BP", "DRE", "DFC", "Indicadores", "IPRF"])
    _render_overview(tabs[0], selected_year, referencia)
    _render_statement_tab(tabs[1], "BP", selected_year, max_level, referencia)
    _render_statement_tab(tabs[2], "DRE", selected_year, max_level, referencia)
    _render_statement_tab(tabs[3], "DFC", selected_year, max_level, referencia)
    _render_indicators(tabs[4], selected_year, referencia)
    _render_iprf(tabs[5], selected_year, referencia)

import os

import streamlit as st
from dotenv import load_dotenv

from config import PAGE_CONFIG
from views.executive_dashboard import render_executive_dashboard


st.set_page_config(**PAGE_CONFIG)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

render_executive_dashboard()

st.markdown("---")
left, right = st.columns([3, 1])
with left:
    st.caption("Desenvolvido para fins didaticos de analise de dados CVM.")
with right:
    st.caption("Projeto final - COSAN + Benchmark + IPRF")

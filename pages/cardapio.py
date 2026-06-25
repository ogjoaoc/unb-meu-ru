import streamlit as st
from components.sidebar import sidebar

st.set_page_config(
    page_title="Sistema de Gestão",
    page_icon="📊",
    layout="wide"
)

sidebar()
import streamlit as st
from components.render_sidebar import render_sidebar

st.set_page_config(
    page_title="Sistema de Geston",
    page_icon="📊",
    layout="wide"
)

render_sidebar()
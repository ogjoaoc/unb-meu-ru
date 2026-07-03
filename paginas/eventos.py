import streamlit as st
from components.sidebar import sidebar

def render_eventos():
    # Carrega a sidebar
    sidebar()
    st.set_page_config(
        page_title="Eventos",
        page_icon=":material/event:", 
        layout="wide"
    )
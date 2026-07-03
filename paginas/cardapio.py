import streamlit as st
from components.sidebar import sidebar

def home():
    # Carrega a sidebar
    sidebar()

    st.set_page_config(
        page_title="Cardápio",
        page_icon="📊",
        layout="wide"
    )

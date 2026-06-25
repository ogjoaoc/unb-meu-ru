import streamlit as st

def sidebar():
    with st.sidebar:
        st.space(355)

        col1, col2 = st.columns([1,3])

        with col1:
            st.image("https://raw.githubusercontent.com/antonio-reis/unb-meu-ru/main/assets/logo.png", width=50)
        with col2:
            st.markdown("## Sistema de Gestão")
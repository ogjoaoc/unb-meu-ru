import streamlit as st

def inicia_sessao():
    if 'usuario' not in st.session_state:
        st.session_state['usuario'] = None
    
    if 'logado' not in st.session_state:
        st.session_state['logado'] = "login"

    if 'pagina' not in st.session_state:
        st.session_state['pagina'] = "home"

    if 'cargo' not in st.session_state:
        st.session_state['cargo'] = None
from components.sidebar import sidebar
from services import autenticacao as auth
import streamlit as st
import pandas as pd

def render_login():
    if st.session_state['cargo'] == None:
        cargo()
    else:
        estudante_login() if st.session_state["cargo"] == "estudante" else funcionario_login()
        

def estudante_login():
    # Carrega a sidebar
    sidebar()

    col1, col2, col3 = st.columns([1.5, 2, 1])
    with col2:

        col1, col2, col3 = st.columns([1, 2, 1]) 
        # Título da página
        col2.markdown("# Login")

        # Texto de solicitação
        col1, col2, col3 = st.columns([0.2, 2.1, 0.9]) 
        col2.markdown("Insira suas credenciais para acessar o sistema.")

        # Campos de entrada para usuário e senha
        col1, col2, col3 = st.columns([.2, 2, 1])
        with col2:
            usuario = st.text_input("Usuário", width=300)
            senha = st.text_input("Senha", type="password", width=300)

        # Botão de login
        col1, col2, col3 = st.columns([1.2, 2, 1])
        with col2:
            if st.button("Entrar"):
                auth.autenticar(usuario, senha)

def funcionario_login():    
    # Carrega a sidebar
    sidebar()

    col1, col2, col3 = st.columns([1.5, 2, 1])
    with col2:

        col1, col2, col3 = st.columns([1, 2, 1]) 
        # Título da página
        col2.markdown("# Login")

        # Texto de solicitação
        col1, col2, col3 = st.columns([0.2, 2.1, 0.9]) 
        col2.markdown("Insira suas credenciais para acessar o sistema.")

        # Campos de entrada para usuário e senha
        col1, col2, col3 = st.columns([.2, 2, 1])
        with col2:
            usuario = st.text_input("Usuário", width=300)
            senha = st.text_input("Senha", type="password", width=300)

        # Botão de login
        col1, col2, col3 = st.columns([1.2, 2, 1])
        with col2:
            if st.button("Entrar"):
                auth.autenticar(usuario, senha)

def cargo():
    sidebar()

    col1, col2, col3 = st.columns([1.7 ,2 ,1])
    with col2:
        st.markdown("### Escolha seu usuário")
        st.space(80)

        col1, col2 = st.columns([.4,1])
        if col1.button("Estudante", width=100):
            st.session_state['cargo'] = "estudante"
            st.rerun()

        if col2.button("Funcionário", width=100):
            st.session_state['cargo'] = "funcionario"
            st.rerun()
        

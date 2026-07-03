from paginas import cardapio, eventos, login
import streamlit as st
import sessoes as ses

ses.inicia_sessao()

if st.session_state['pagina'] == "home":
    cardapio.home()

if st.session_state['pagina'] == "eventos":
    eventos.render_eventos()

if st.session_state['pagina'] == "login":
    login.render_login()
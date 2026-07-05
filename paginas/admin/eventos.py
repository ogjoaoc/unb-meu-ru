import streamlit as st
from datetime import datetime
from components.styles import inject
from database.cardapio_db import listar_eventos

inject()
user_sessao = st.session_state.get('usuario', {})
if not user_sessao:
	st.stop()

st.title("🎉 Eventos")
st.caption("Próximas atividades e eventos do RU")


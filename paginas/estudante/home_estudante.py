import streamlit as st
st.title("painel do aluno")
st.write(f"bem-vindo, {st.session_state['usuario']['nome']}!")

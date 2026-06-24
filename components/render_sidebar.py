import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.navigation([
            st.Page("cardapio.py", title="Cardápio", icon=":material/restaurant_menu:"),
            st.Page("pages/eventos.py", title="Eventos", icon=":material/event:"),
        ])

        st.space("xxlarge")
        st.space("xxlarge")
        st.space("large")
        with st.container(horizontal=True, gap="medium", border=True):
            st.write("👥"),
            st.write("Nome")
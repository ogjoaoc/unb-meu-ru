import streamlit as st

def sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        min-width: 250px;
        max-width: 250px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.space(50)
        
        if st.button("Cardápio", width=200, icon=":material/restaurant_menu:"):
            st.session_state['pagina'] = "home"
            st.rerun()

        if st.button("Eventos", width=200, icon=":material/event:"):
            st.session_state['pagina'] = "eventos"
            st.rerun()

        if st.button("Login", width=200, icon=":material/login:"):
            st.session_state['pagina'] = "login"
            st.rerun()

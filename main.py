import streamlit as st

pages = {
    "home": st.Page(
        "pages/cardapio.py",
        title= "Cardápio",
        icon= ":material/restaurant_menu:",
        default=True
    ),
    "eventos": st.Page(
        "pages/eventos.py",
        title= "Eventos",
        icon= ":material/event:"
    )
}

pg = st.navigation(list(pages.values()))
pg.run()
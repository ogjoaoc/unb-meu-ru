import streamlit as st
from components.render_sidebar import render_sidebar

st.set_page_config(page_title="Eventos", page_icon=":material/event:", layout="wide")
render_sidebar()


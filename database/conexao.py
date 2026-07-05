import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

def get_connection():
    try:
        return psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            database=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            port=st.secrets["postgres"]["port"]
        )
    except Exception as e:
        st.error(f"erro ao conectar ao banco: {e}")
        return None

def run_query(query, params=None, fetch=False):
    CON = get_connection()
    if not CON: 
        return None
    try:
        with CON.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if fetch:
                return cursor.fetchall()
            CON.commit()
            return True
    except Exception as e:
        st.error(f"erro na execução da Query: {e}")
        if CON: 
            CON.rollback()
        return None
    finally:
        if CON: 
            CON.close()
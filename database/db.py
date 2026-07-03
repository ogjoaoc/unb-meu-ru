import psycopg2
from psycopg2.extras import RealDictCursor 
import streamlit as st

def get_connection():
    try:
        CON = psycopg2.connect( 
            host="localhost",
            database="unb_meu_ru",  
            user="postgres",        
            password="trivial", 
            port="5432"
        )
        return CON
    except Exception as e:
        st.error(f"erro ao conectar ao banco de dados: {e}")
        return None
    
def run_query(query, params = None, fetch = False): #
    CON = get_connection()
    if not CON:
        return None
    res = None
    try:
        with CON.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if fetch:
                res = cursor.fetchall()
            CON.commit()  
    except Exception as e:
        if CON:
            CON.rollback()  
        st.error(f"erro na execução da Query: {e}")
    finally:
        if CON:
            CON.close()  
    return res

teste = run_query("SELECT version();", fetch=True)
if teste:
    print("boa!!!!")
    print(f"ver: {teste[0]['version']}")
else:
    print("ruim")
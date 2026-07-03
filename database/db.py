import psycopg2
from psycopg2.extras import RealDictCursor 
import streamlit as st
import random 

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

def add_student(matricula, nome, email, senha, data_nascimento, curso):
    CON = get_connection()
    if not CON:
        return None
    try:
        with CON.cursor() as cursor:
            id_usuario = random.randint(10000, 99999)
            query = """
                INSERT INTO Usuario (ID_Usuario, Nome, Senha, Data_Nascimento, Email) 
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (id_usuario, nome, senha, data_nascimento, email.strip()))
            query = """
                INSERT INTO Estudante (Matricula, Saldo_RU, Curso, ID_Usuario) 
                VALUES (%s, 0.00, %s, %s);
            """
            cursor.execute(query, (int(matricula), curso, id_usuario))
            CON.commit()
            return {"matricula": matricula, "email": email}
    except Exception as e:
        if CON: 
            CON.rollback()
        st.error(f"erro na transação de cadastro: {e}")
        return None
    finally:
        if CON: 
            CON.close()

def cardapio_ativo():
    return None

def listar_eventos():
    return []

def itens_do_cardapio(id_cardapio):
    return []

teste = run_query("SELECT version();", fetch=True)
if teste:
    print("boa!!!!")
    print(f"ver: {teste[0]['version']}")
else:
    print("ruim")


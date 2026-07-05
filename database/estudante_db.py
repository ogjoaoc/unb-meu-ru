import random
from datetime import datetime
import streamlit as st
from database.conexao import get_connection, run_query

def adicionar_estudante(matricula, nome, email, senha, data_nascimento, curso):
    CON = get_connection()
    if not CON: return None
    try:
        with CON.cursor() as cursor:
            id_usuario = random.randint(10000, 99999)
            query = "INSERT INTO Usuario (ID_Usuario, Nome, Senha, Data_Nascimento, Email) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query, (id_usuario, nome, senha, data_nascimento, email.strip()))
            query = "INSERT INTO Estudante (Matricula, Saldo_RU, Curso, ID_Usuario) VALUES (%s, 0.00, %s, %s);"
            cursor.execute(query, (int(matricula), curso, id_usuario))
            CON.commit()
            return {"matricula": matricula, "email": email}
    except Exception as e:
        if CON: CON.rollback()
        st.error(f"Erro na transação de cadastro: {e}")
        return None
    finally:
        if CON: CON.close()

def saldo_atual(matricula):
    query = "SELECT Saldo_RU FROM Estudante WHERE Matricula = %s;"
    res = run_query(query, (matricula,), fetch=True)
    return float(res[0]['saldo_ru']) if res else 0.0

def historico_transacoes(matricula, limite=30):
    query = (
        "SELECT Valor AS valor_transacao, Data_Hora AS data_hora "
        "FROM Transacao WHERE Matricula = %s ORDER BY Data_Hora DESC LIMIT %s;"
    )
    return run_query(query, (matricula, limite), fetch=True) or []

def recarregar_saldo(matricula, valor):
    CON = get_connection()
    if not CON: return False
    try:
        with CON.cursor() as cursor:
            cursor.execute("UPDATE Estudante SET Saldo_RU = Saldo_RU + %s WHERE Matricula = %s;", (valor, matricula))
            id_transacao = random.randint(100000, 999999)
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            q_trans = "INSERT INTO Transacao (ID_Transacao, Valor, Data_Hora, Matricula) VALUES (%s, %s, %s, %s);"
            cursor.execute(q_trans, (id_transacao, valor, agora, matricula))
            CON.commit()
            return True
    except Exception as e:
        if CON: CON.rollback()
        st.error(f"Erro na transação de recarga: {e}")
        return False
    finally:
        if CON: CON.close()
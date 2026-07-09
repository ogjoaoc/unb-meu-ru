import psycopg2
from database.conexao import get_connection, run_query

def listar_eventos():
    query = "SELECT id_evento, data_inicio, data_fim, descricao, foto_capa FROM Evento ORDER BY data_inicio ASC;"
    return run_query(query, fetch=True) or []

def obter_evento(id_evento):
    query = "SELECT id_evento, data_inicio, data_fim, descricao, foto_capa FROM Evento WHERE id_evento = %s LIMIT 1;"
    res = run_query(query, (id_evento,), fetch=True) or []
    return res[0] if res else None

def criar_evento(data_inicio, data_fim, descricao, foto_bytes=None): # <<< REMOVIDO id_evento daqui
    con = get_connection()
    if not con:
        return False
    try:
        with con.cursor() as cursor:
            foto_valor = psycopg2.Binary(foto_bytes) if foto_bytes else None
            cursor.execute(
                "INSERT INTO Evento (data_inicio, data_fim, descricao, foto_capa) VALUES (%s, %s, %s, %s);",
                (data_inicio, data_fim, descricao, foto_valor),
            )
            con.commit()
            return True
    except Exception:
        if con:
            con.rollback()
        return False
    finally:
        if con:
            con.close()

def atualizar_evento(id_evento, data_inicio, data_fim, descricao, foto_bytes=None):
    con = get_connection()
    if not con:
        return False
    try:
        with con.cursor() as cursor:
            if foto_bytes:
                foto_valor = psycopg2.Binary(foto_bytes)
                cursor.execute(
                    "UPDATE Evento SET data_inicio = %s, data_fim = %s, descricao = %s, foto_capa = %s WHERE id_evento = %s;",
                    (data_inicio, data_fim, descricao, foto_valor, id_evento),
                )
            else:
                cursor.execute(
                    "UPDATE Evento SET data_inicio = %s, data_fim = %s, descricao = %s WHERE id_evento = %s;",
                    (data_inicio, data_fim, descricao, id_evento),
                )
            if cursor.rowcount == 0:
                con.rollback()
                return False
            con.commit()
            return True
    except Exception:
        if con:
            con.rollback()
        return False
    finally:
        if con:
            con.close()

def excluir_evento(id_evento):
    con = get_connection()
    if not con:
        return False
    try:
        with con.cursor() as cursor:
            cursor.execute("DELETE FROM Evento WHERE id_evento = %s;", (id_evento,))
            if cursor.rowcount == 0:
                con.rollback()
                return False
            con.commit()
            return True
    except Exception:
        if con:
            con.rollback()
        return False
    finally:
        if con:
            con.close()

def listar_inscritos_evento(id_evento: int):
    query = (
        "SELECT e.Matricula, u.Nome, u.Email, e.Curso, i.Data_Inscricao "
        "FROM Inscricao i "
        "JOIN Estudante e ON i.Matricula = e.Matricula "
        "JOIN Usuario u ON e.ID_Usuario = u.ID_Usuario "
        "WHERE i.ID_Evento = %s "
        "ORDER BY i.Data_Inscricao DESC;"
    )
    return run_query(query, (id_evento,), fetch=True) or []

def inscricoes_do_estudante(matricula):
    query = "SELECT id_evento FROM Inscricao WHERE matricula = %s ORDER BY data_inscricao DESC;"
    res = run_query(query, (matricula,), fetch=True) or []
    return [r["id_evento"] for r in res]

def contagem_inscritos(id_evento):
    query = "SELECT COUNT(*) AS total FROM Inscricao WHERE id_evento = %s;"
    res = run_query(query, (id_evento,), fetch=True)
    return int(res[0]["total"]) if res else 0

def inscrever_estudante(id_evento, matricula):
    con = get_connection()
    if not con:
        return False
    try:
        with con.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM Inscricao WHERE matricula = %s AND id_evento = %s;",
                (matricula, id_evento),
            )
            if cursor.fetchone():
                return False

            cursor.execute(
                "INSERT INTO Inscricao (matricula, id_evento) VALUES (%s, %s);",
                (matricula, id_evento),
            )
            con.commit()
            return True
    except Exception:
        if con:
            con.rollback()
        return False
    finally:
        if con:
            con.close()

def cancelar_inscricao(id_evento, matricula):
    con = get_connection()
    if not con:
        return False
    try:
        with con.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Inscricao WHERE matricula = %s AND id_evento = %s;",
                (matricula, id_evento),
            )
            if cursor.rowcount == 0:
                con.rollback()
                return False
            con.commit()
            return True
    except Exception:
        if con:
            con.rollback()
        return False
    finally:
        if con:
            con.close()
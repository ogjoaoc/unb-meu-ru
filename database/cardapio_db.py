import random
from datetime import datetime
from database.conexao import run_query

def cardapio_ativo():
    hoje = datetime.now().strftime("%Y-%m-%d")
    query = "SELECT ID_Cardapio, Data_inicio, Data_fim, Status FROM Cardapio WHERE %s BETWEEN Data_inicio AND Data_fim LIMIT 1;"
    res = run_query(query, (hoje,), fetch=True)
    return res[0] if res else None

def itens_do_cardapio(id_cardapio):
    query = """
        SELECT ic.Nome, ic.Categoria, ic.Composicao, ic_card.Periodo, ic_card.Dia_semana 
        FROM Item_Cardapio ic
        JOIN Contem ic_card ON ic.ID_ItemCardapio = ic_card.ID_ItemCardapio
        WHERE ic_card.ID_Cardapio = %s;
    """
    return run_query(query, (id_cardapio,), fetch=True) or []

def media_notas_cardapio(id_cardapio):
    query = "SELECT AVG(Nota) as media, COUNT(*) as total FROM Feedback WHERE ID_Cardapio = %s;"
    res = run_query(query, (id_cardapio,), fetch=True)
    if res and res[0]['total'] > 0:
        return round(float(res[0]['media']), 1), res[0]['total']
    return 0.0, 0

def registrar_feedback(comentario, nota, id_cardapio, matricula):
    query = "INSERT INTO Feedback (ID_Feedback, Descricao, Nota, ID_Cardapio, Matricula) VALUES (%s, %s, %s, %s, %s);"
    id_fb = random.randint(100000, 999999)
    return run_query(query, (id_fb, comentario, nota, id_cardapio, matricula), fetch=False) is not None

# ainda vai ter
def listar_eventos():
    return []
import random
from datetime import datetime

from database.conexao import run_query

def cardapio_ativo():
    hoje = datetime.now().strftime("%Y-%m-%d")
    query = """
        SELECT id_cardapio, data_inicio, data_fim, status 
        FROM Cardapio 
        WHERE %s BETWEEN data_inicio AND data_fim AND status = 'Publicado' 
        LIMIT 1;
    """
    res = run_query(query, (hoje,), fetch=True)
    return res[0] if res else None

def itens_do_cardapio(id_cardapio):
    query = """
        SELECT ic.nome, ic.categoria, cci.periodo, cci.dia_semana, cci.composicao, ic.id_itemcardapio
        FROM ItemCardapio ic
        JOIN Cardapio_Contem_Item cci ON ic.id_itemcardapio = cci.id_itemcardapio
        WHERE cci.id_cardapio = %s;
    """
    return run_query(query, (id_cardapio,), fetch=True) or []

def media_notas_cardapio(id_cardapio):
    query = "SELECT AVG(nota) as media, COUNT(*) as total FROM Feedback WHERE id_cardapio = %s;"
    res = run_query(query, (id_cardapio,), fetch=True)
    if res and res[0]['total'] > 0:
        return round(float(res[0]['media']), 1), res[0]['total']
    return 0.0, 0

def registrar_feedback(comentario, nota, id_cardapio, matricula):
    query = "INSERT INTO Feedback (id_feedback, descricao, nota, id_cardapio, matricula) VALUES (%s, %s, %s, %s, %s);"
    id_fb = random.randint(100000, 999999)
    return run_query(query, (id_fb, comentario, nota, id_cardapio, matricula), fetch=False) is not None

def listar_itens_cardapio():
    query = "SELECT id_itemcardapio, categoria, nome, id_nutricionista FROM ItemCardapio ORDER BY nome;"
    return run_query(query, fetch=True) or []

def listar_categorias():
    query = "SELECT DISTINCT categoria FROM ItemCardapio ORDER BY categoria;"
    res = run_query(query, fetch=True)
    return [r['categoria'] for r in res] if res else []

def listar_cardapios(limite=8):
    query = "SELECT id_cardapio, data_inicio, data_fim, status FROM Cardapio ORDER BY data_inicio DESC LIMIT %s;"
    return run_query(query, (limite,), fetch=True) or []

def cardapio_no_periodo(data_inicio, data_fim):
    query = """
        SELECT id_cardapio
        FROM Cardapio
        WHERE NOT (data_fim < %s OR data_inicio > %s)
        LIMIT 1;
    """
    res = run_query(query, (data_inicio, data_fim), fetch=True)
    return res[0] if res else None

def criar_cardapio(id_cardapio, data_inicio, data_fim, id_funcionario):
    if cardapio_no_periodo(data_inicio, data_fim):
        return False
    query = """
        INSERT INTO Cardapio (id_cardapio, data_inicio, data_fim, status, id_funcionario)
        VALUES (%s, %s, %s, 'Incompleto', %s);
    """
    return run_query(query, (id_cardapio, data_inicio, data_fim, id_funcionario), fetch=False) is not None

def adicionar_item_ao_cardapio(id_cardapio, id_itemcardapio, periodo, dia_semana, composicao):
    query = """
        INSERT INTO Cardapio_Contem_Item (id_cardapio, id_itemcardapio, periodo, dia_semana, composicao)
        VALUES (%s, %s, %s, %s, %s);
    """
    return run_query(query, (id_cardapio, id_itemcardapio, periodo, dia_semana, composicao), fetch=False) is not None

def remover_item_do_cardapio(id_cardapio, id_itemcardapio, periodo, dia_semana, composicao):
    query = """
        DELETE FROM Cardapio_Contem_Item
        WHERE id_cardapio = %s AND id_itemcardapio = %s AND periodo = %s AND dia_semana = %s AND composicao = %s;
    """
    return run_query(query, (id_cardapio, id_itemcardapio, periodo, dia_semana, composicao), fetch=False) is not None

def publicar_cardapio(id_cardapio):
    query = "UPDATE Cardapio SET status = 'Publicado' WHERE id_cardapio = %s;"
    return run_query(query, (id_cardapio,), fetch=False) is not None


def excluir_cardapio(id_cardapio):
    query = "DELETE FROM Cardapio WHERE id_cardapio = %s;"
    return run_query(query, (id_cardapio,), fetch=False) is not None

def adicionar_item_catalogo(id_itemcardapio, categoria, nome, id_nutricionista):
    query = """
        INSERT INTO ItemCardapio (id_itemcardapio, categoria, nome, id_nutricionista)
        VALUES (%s, %s, %s, %s);
    """
    return run_query(query, (id_itemcardapio, categoria, nome, id_nutricionista), fetch=False) is not None

def feedbacks_do_cardapio(id_cardapio):
    query = "SELECT id_feedback, nota, descricao, matricula FROM Feedback WHERE id_cardapio = %s ORDER BY data_feedback DESC;"
    return run_query(query, (id_cardapio,), fetch=True) or []

# usando a view
def relatorio_desempenho_cardapios():
    query = "SELECT * FROM vw_desempenho_cardapio ORDER BY data_inicio DESC;"
    return run_query(query, fetch=True) or []
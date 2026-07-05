from database.conexao import run_query

# def autenticar(usuario, senha):
#     if usuario == "admin" and senha == "admin":
#         return True
#     return False

def run_login(email, senha):
    query = """
    SELECT 
        u.ID_Usuario, u.Nome, u.Email, u.Senha,
        CASE 
            WHEN e.Matricula IS NOT NULL THEN 'estudante'
            WHEN n.ID_Funcionario IS NOT NULL THEN 'nutricionista'
            WHEN g.ID_Funcionario IS NOT NULL THEN 'gerente'
            ELSE 'usuario'
        END as papel,
        e.Matricula as matricula,
        n.ID_Funcionario as id_nutricionista,
        g.ID_Funcionario as id_gerente
    FROM Usuario u
    LEFT JOIN Estudante e ON u.ID_Usuario = e.ID_Usuario
    LEFT JOIN Funcionario f ON u.ID_Usuario = f.ID_Usuario
    LEFT JOIN Nutricionista n ON f.ID_Funcionario = n.ID_Funcionario
    LEFT JOIN Gerente g ON f.ID_Funcionario = g.ID_Funcionario
    WHERE u.Email = %s AND u.Senha = %s;  -- CORRIGIDO AQUI: u.Email em vez de ID
    """
    resultado = run_query(query, (email, senha), fetch=True)
    if resultado:
        return resultado[0] 
    return None

teste = run_login("joao@gmail.com", "unb1")
print(teste)

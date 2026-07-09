CREATE OR REPLACE VIEW vw_desempenho_cardapio AS
SELECT 
    c.id_cardapio,
    c.data_inicio,
    c.data_fim,
    c.status,
    u.nome AS nutricionista_responsavel,
    COUNT(f.id_feedback) AS total_avaliacoes,
    ROUND(COALESCE(AVG(f.nota), 0), 2) AS nota_media
FROM Cardapio c
LEFT JOIN Feedback f ON c.id_cardapio = f.id_cardapio
LEFT JOIN Funcionario func ON c.id_funcionario = func.id_funcionario
LEFT JOIN Usuario u ON func.id_usuario = u.id_usuario
GROUP BY c.id_cardapio, c.data_inicio, c.data_fim, c.status, u.nome;

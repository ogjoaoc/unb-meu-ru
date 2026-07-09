INSERT INTO Usuario (ID_Usuario, Nome, Senha, Data_Nascimento, Email) VALUES
(3001, 'Fernanda Lima', 'unb1', '1990-05-15', 'fernanda@unb.br'),
(3002, 'Paula Souza', 'unb1', '1989-08-22', 'paula@unb.br'),
(3003, 'Bruno Costa', 'unb1', '1991-02-11', 'bruno@unb.br'),
(3004, 'Carla Nunes', 'unb1', '1988-12-03', 'carla@unb.br'),
(3005, 'Diego Almeida', 'unb1', '1992-07-19', 'diego@unb.br'),
(3006, 'Marcos Pereira', 'unb1', '1987-11-03', 'marcos@unb.br'),
(3007, 'Aline Barbosa', 'unb1', '1990-04-14', 'aline@unb.br'),
(3008, 'Rafael Martins', 'unb1', '1986-09-30', 'rafael@unb.br'),
(3009, 'Beatriz Rocha', 'unb1', '1993-01-27', 'beatriz@unb.br'),
(3010, 'Thiago Alves', 'unb1', '1985-06-08', 'thiago@unb.br'),
(3011, 'Joao Silva', 'unb1', '2003-04-20', 'joao@unb.br'),
(3012, 'Maria Oliveira', 'unb1', '2002-05-18', 'maria@unb.br'),
(3013, 'Pedro Santos', 'unb1', '2001-10-07', 'pedro@unb.br'),
(3014, 'Ana Martins', 'unb1', '2004-03-29', 'ana@unb.br'),
(3015, 'Lucas Pereira', 'unb1', '2003-12-12', 'lucas@unb.br')
ON CONFLICT DO NOTHING;

INSERT INTO Funcionario (ID_Funcionario, Salario, ID_Usuario) VALUES
(2001, 8500.00, 3001),
(2002, 8600.00, 3002),
(2003, 8450.00, 3003),
(2004, 8700.00, 3004),
(2005, 8550.00, 3005),
(2011, 9200.00, 3006),
(2012, 9300.00, 3007),
(2013, 9150.00, 3008),
(2014, 9400.00, 3009),
(2015, 9250.00, 3010)
ON CONFLICT DO NOTHING;

INSERT INTO Nutricionista (ID_Funcionario) VALUES
(2001),
(2002),
(2003),
(2004),
(2005)
ON CONFLICT DO NOTHING;

INSERT INTO Gerente (ID_Funcionario) VALUES
(2011),
(2012),
(2013),
(2014),
(2015)
ON CONFLICT DO NOTHING;

INSERT INTO Estudante (Matricula, Saldo_RU, Curso, ID_Usuario) VALUES
(24100001, 35.00, 'Ciencia da Computacao', 3011),
(24100002, 18.50, 'Engenharia de Software', 3012),
(24100003, 42.00, 'Arquitetura', 3013),
(24100004, 12.75, 'Nutrição', 3014),
(24100005, 27.30, 'Direito', 3015)
ON CONFLICT DO NOTHING;

INSERT INTO Evento (ID_Evento, Data_inicio, Data_fim, Descricao) VALUES
(5001, '2026-07-08 10:00:00', '2026-07-09 12:00:00', 'Oficina de aproveitamento integral dos alimentos'),
(5002, '2026-07-10 14:00:00', '2026-07-10 16:00:00', 'Roda de conversa sobre alimentação saudável'),
(5003, '2026-07-12 09:00:00', '2026-07-12 11:00:00', 'Feira cultural do RU'),
(5004, '2026-07-15 13:00:00', '2026-07-15 15:30:00', 'Semana temática da gastronomia brasileira'),
(5005, '2026-07-18 18:00:00', '2026-07-18 20:00:00', 'Apresentação musical no RU')
ON CONFLICT DO NOTHING;

INSERT INTO ItemCardapio (ID_ItemCardapio, Categoria, Nome, ID_Nutricionista) VALUES
(10001, 'Bebida', 'Suco de laranja', 2001),
(10002, 'Bebida', 'Café preto', 2001),
(10003, 'Panificação', 'Pão francês', 2001),
(10004, 'Panificação', 'Pão integral', 2001),
(10005, 'Complemento', 'Manteiga', 2001),
(10006, 'Complemento', 'Queijo coalho', 2001),
(10007, 'Fruta', 'Banana', 2001),
(10008, 'Fruta', 'Maçã', 2001),
(10009, 'Prato Principal', 'Frango grelhado', 2001),
(10010, 'Prato Principal', 'Carne de panela', 2001),
(10011, 'Guarnição', 'Arroz branco', 2001),
(10012, 'Guarnição', 'Feijão carioca', 2001),
(10013, 'Salada', 'Salada verde', 2001),
(10014, 'Salada', 'Salada de tomate', 2001),
(10015, 'Sobremesa', 'Gelatina', 2001),
(10016, 'Sobremesa', 'Melancia', 2001)
ON CONFLICT DO NOTHING;

INSERT INTO Cardapio (ID_Cardapio, Data_Inicio, Data_Fim, Status, ID_Funcionario) VALUES
(4001, '2026-07-07', '2026-07-13', 'Publicado', 2001),
(4002, '2026-07-14', '2026-07-20', 'Incompleto', 2002),
(4003, '2026-07-21', '2026-07-27', 'Completo', 2003),
(4004, '2026-06-30', '2026-07-06', 'Publicado', 2004),
(4005, '2026-07-28', '2026-08-03', 'Incompleto', 2005)
ON CONFLICT DO NOTHING;

INSERT INTO Inscricao (Matricula, ID_Evento) VALUES
(24100001, 5001),
(24100002, 5002),
(24100003, 5003),
(24100004, 5004),
(24100005, 5005)
ON CONFLICT DO NOTHING;

INSERT INTO Cardapio_Contem_Item (ID_Cardapio, ID_ItemCardapio, Periodo, Dia_Semana, Composicao) VALUES
(4001, 10002, 'Cafe', 'Segunda', 'Café preto'),
(4001, 10003, 'Cafe', 'Segunda', 'Pão francês'),
(4001, 10007, 'Cafe', 'Segunda', 'Banana'),
(4001, 10009, 'Almoco', 'Segunda', 'Frango grelhado'),
(4001, 10011, 'Almoco', 'Segunda', 'Arroz branco'),
(4001, 10013, 'Almoco', 'Segunda', 'Salada verde'),
(4001, 10010, 'Jantar', 'Segunda', 'Carne de panela'),
(4001, 10012, 'Jantar', 'Segunda', 'Feijão carioca'),
(4001, 10015, 'Jantar', 'Segunda', 'Gelatina'),

(4001, 10001, 'Cafe', 'Terca', 'Suco de laranja'),
(4001, 10004, 'Cafe', 'Terca', 'Pão integral'),
(4001, 10008, 'Cafe', 'Terca', 'Maçã'),
(4001, 10010, 'Almoco', 'Terca', 'Carne de panela'),
(4001, 10012, 'Almoco', 'Terca', 'Feijão carioca'),
(4001, 10014, 'Almoco', 'Terca', 'Salada de tomate'),
(4001, 10009, 'Jantar', 'Terca', 'Frango grelhado'),
(4001, 10011, 'Jantar', 'Terca', 'Arroz branco'),
(4001, 10016, 'Jantar', 'Terca', 'Melancia'),

(4001, 10002, 'Cafe', 'Quarta', 'Café preto'),
(4001, 10003, 'Cafe', 'Quarta', 'Pão francês'),
(4001, 10007, 'Cafe', 'Quarta', 'Banana'),
(4001, 10009, 'Almoco', 'Quarta', 'Frango grelhado'),
(4001, 10012, 'Almoco', 'Quarta', 'Feijão carioca'),
(4001, 10013, 'Almoco', 'Quarta', 'Salada verde'),
(4001, 10010, 'Jantar', 'Quarta', 'Carne de panela'),
(4001, 10011, 'Jantar', 'Quarta', 'Arroz branco'),
(4001, 10015, 'Jantar', 'Quarta', 'Gelatina'),

(4001, 10001, 'Cafe', 'Quinta', 'Suco de laranja'),
(4001, 10004, 'Cafe', 'Quinta', 'Pão integral'),
(4001, 10008, 'Cafe', 'Quinta', 'Maçã'),
(4001, 10010, 'Almoco', 'Quinta', 'Carne de panela'),
(4001, 10011, 'Almoco', 'Quinta', 'Arroz branco'),
(4001, 10014, 'Almoco', 'Quinta', 'Salada de tomate'),
(4001, 10009, 'Jantar', 'Quinta', 'Frango grelhado'),
(4001, 10012, 'Jantar', 'Quinta', 'Feijão carioca'),
(4001, 10016, 'Jantar', 'Quinta', 'Melancia'),

(4001, 10002, 'Cafe', 'Sexta', 'Café preto'),
(4001, 10003, 'Cafe', 'Sexta', 'Pão francês'),
(4001, 10007, 'Cafe', 'Sexta', 'Banana'),
(4001, 10009, 'Almoco', 'Sexta', 'Frango grelhado'),
(4001, 10011, 'Almoco', 'Sexta', 'Arroz branco'),
(4001, 10013, 'Almoco', 'Sexta', 'Salada verde'),
(4001, 10010, 'Jantar', 'Sexta', 'Carne de panela'),
(4001, 10012, 'Jantar', 'Sexta', 'Feijão carioca'),
(4001, 10015, 'Jantar', 'Sexta', 'Gelatina'),

(4001, 10001, 'Cafe', 'Sabado', 'Suco de laranja'),
(4001, 10004, 'Cafe', 'Sabado', 'Pão integral'),
(4001, 10008, 'Cafe', 'Sabado', 'Maçã'),
(4001, 10010, 'Almoco', 'Sabado', 'Carne de panela'),
(4001, 10012, 'Almoco', 'Sabado', 'Feijão carioca'),
(4001, 10014, 'Almoco', 'Sabado', 'Salada de tomate'),
(4001, 10009, 'Jantar', 'Sabado', 'Frango grelhado'),
(4001, 10011, 'Jantar', 'Sabado', 'Arroz branco'),
(4001, 10016, 'Jantar', 'Sabado', 'Melancia'),

(4001, 10002, 'Cafe', 'Domingo', 'Café preto'),
(4001, 10003, 'Cafe', 'Domingo', 'Pão francês'),
(4001, 10007, 'Cafe', 'Domingo', 'Banana'),
(4001, 10009, 'Almoco', 'Domingo', 'Frango grelhado'),
(4001, 10011, 'Almoco', 'Domingo', 'Arroz branco'),
(4001, 10013, 'Almoco', 'Domingo', 'Salada verde'),
(4001, 10010, 'Jantar', 'Domingo', 'Carne de panela'),
(4001, 10012, 'Jantar', 'Domingo', 'Feijão carioca'),
(4001, 10015, 'Jantar', 'Domingo', 'Gelatina')
ON CONFLICT DO NOTHING;

INSERT INTO Transacao (ID_Transacao, Valor, Data_Hora, Matricula) VALUES
(7001, 25.00, '2026-07-01 08:30:00', 24100001),
(7002, 30.00, '2026-07-02 09:00:00', 24100002),
(7003, 15.00, '2026-07-03 10:15:00', 24100003),
(7004, 40.00, '2026-07-04 11:45:00', 24100004),
(7005, 20.00, '2026-07-05 12:20:00', 24100005)
ON CONFLICT DO NOTHING;

INSERT INTO Preferencias (ID_Usuario, Preferencia) VALUES
(3011, 'Vegetariano'),
(3012, 'Sem lactose'),
(3013, 'Pouco sal'),
(3014, 'Alta proteína'),
(3015, 'Sem glúten')
ON CONFLICT DO NOTHING;

INSERT INTO Certificado (ID_Certificado, Data_Emissao, Creditos, ID_Usuario, ID_Evento) VALUES
(8001, '2026-07-12', 2, 3011, 5001),
(8002, '2026-07-13', 2, 3012, 5002),
(8003, '2026-07-14', 2, 3013, 5003),
(8004, '2026-07-15', 2, 3014, 5004),
(8005, '2026-07-16', 2, 3015, 5005)
ON CONFLICT DO NOTHING;

INSERT INTO Feedback (ID_Feedback, Nota, Descricao, Data_Feedback, Matricula, ID_Cardapio) VALUES
(9001, 5, 'Cardápio variado e bem servido.', '2026-07-09 13:00:00', 24100001, 4001),
(9002, 4, 'Bom equilíbrio entre saladas e prato principal.', '2026-07-09 13:10:00', 24100002, 4002),
(9003, 5, 'Muito bom para o almoço.', '2026-07-09 13:20:00', 24100003, 4003),
(9004, 3, 'Pode melhorar a sobremesa.', '2026-07-09 13:30:00', 24100004, 4004),
(9005, 4, 'Gostei da variedade de bebidas.', '2026-07-09 13:40:00', 24100005, 4005)
ON CONFLICT DO NOTHING;

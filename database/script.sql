CREATE TABLE Usuario (
    ID_Usuario INT PRIMARY KEY,
    Nome VARCHAR(150) NOT NULL,
    Senha VARCHAR(255) NOT NULL, 
    Data_Nascimento DATE NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Evento (
    ID_Evento INT PRIMARY KEY,
    Data_inicio TIMESTAMP NOT NULL,
    Data_fim TIMESTAMP NOT NULL,
    Descricao TEXT NOT NULL,
    CONSTRAINT inicio_fim_evento CHECK (Data_fim >= Data_inicio)
);

CREATE TABLE Estudante (
    Matricula INT PRIMARY KEY,
    Saldo_RU DECIMAL(10, 2) DEFAULT 0.00,
    Curso VARCHAR(100),
    ID_Usuario INT UNIQUE NOT NULL,
    CONSTRAINT fk_estudante_usuario FOREIGN KEY (ID_Usuario) 
    REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE
);

CREATE TABLE Funcionario (
    ID_Funcionario INT PRIMARY KEY,
    Salario DECIMAL(10, 2) NOT NULL,
    ID_Usuario INT UNIQUE NOT NULL,
    CONSTRAINT fk_funcionario_usuario FOREIGN KEY (ID_Usuario) 
    REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE
);

CREATE TABLE Gerente (
    ID_Funcionario INT PRIMARY KEY,
    CONSTRAINT fk_gerente_funcionario FOREIGN KEY (ID_Funcionario) 
    REFERENCES Funcionario(ID_Funcionario) ON DELETE CASCADE
);

CREATE TABLE Nutricionista (
    ID_Funcionario INT PRIMARY KEY,
    CONSTRAINT fk_nutricionista_funcionario FOREIGN KEY (ID_Funcionario) 
    REFERENCES Funcionario(ID_Funcionario) ON DELETE CASCADE
);


CREATE TABLE ItemCardapio (
    ID_ItemCardapio INT PRIMARY KEY,
    Categoria VARCHAR(50) NOT NULL, 
    Nome VARCHAR(100) NOT NULL,
    ID_Nutricionista INT NOT NULL,
    CONSTRAINT fk_item_nutricionista
    FOREIGN KEY (ID_Nutricionista) REFERENCES Nutricionista(ID_Funcionario)
);

CREATE TABLE Cardapio (
    ID_Cardapio INT PRIMARY KEY,
    Data_Inicio DATE NOT NULL,
    Data_Fim DATE NOT NULL,
    Status VARCHAR(20) DEFAULT 'Incompleto',
    ID_Funcionario INT,
    
    CONSTRAINT chk_status_cardapio CHECK (Status IN ('Incompleto', 'Completo', 'Publicado')),
    CONSTRAINT periodo_cardapio CHECK (Data_Fim >= Data_Inicio),
    CONSTRAINT fk_cardapio_editor  
    FOREIGN KEY (ID_Funcionario) REFERENCES Nutricionista(ID_Funcionario)
);


CREATE TABLE Inscricao (
    Matricula INT NOT NULL, 
    ID_Evento INT NOT NULL,
    Data_Inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (Matricula, ID_Evento),

    CONSTRAINT fk_inscricao_estudante
    FOREIGN KEY (Matricula) REFERENCES Estudante(Matricula) ON DELETE CASCADE,
    CONSTRAINT fk_inscricao_evento     
    FOREIGN KEY (ID_Evento) REFERENCES Evento(ID_Evento) ON DELETE CASCADE
);

CREATE TABLE Cardapio_Contem_Item (
    ID_Cardapio INT NOT NULL,
    ID_ItemCardapio INT NOT NULL,
    Periodo VARCHAR(20) NOT NULL,
    Dia_Semana VARCHAR(20) NOT NULL,
    Composicao TEXT NOT NULL,

    PRIMARY KEY (ID_Cardapio, Dia_Semana, Periodo, Composicao),
    CONSTRAINT fk_cardapio_item_cardapio
    FOREIGN KEY (ID_Cardapio) REFERENCES Cardapio(ID_Cardapio) ON DELETE CASCADE,
    CONSTRAINT fk_cardapio_item_item
    FOREIGN KEY (ID_ItemCardapio) REFERENCES ItemCardapio(ID_ItemCardapio) ON DELETE CASCADE
);

CREATE TABLE Transacao (
    ID_Transacao INT PRIMARY KEY,
    Valor DECIMAL(10,2) NOT NULL,
    Data_Hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Matricula INT NOT NULL,

    CONSTRAINT fk_transacao_estudante
    FOREIGN KEY (Matricula) REFERENCES Estudante(Matricula) ON DELETE CASCADE
);

CREATE TABLE Preferencias (
    ID_Usuario INT NOT NULL,
    Preferencia VARCHAR(50) NOT NULL,

    PRIMARY KEY (ID_Usuario, Preferencia),
    CONSTRAINT fk_preferencias_usuario 
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE
);

CREATE TABLE Certificado (
    ID_Certificado INT PRIMARY KEY,
    Data_Emissao DATE NOT NULL,
    Creditos INT NOT NULL,
    ID_Usuario INT NOT NULL,
    ID_Evento INT NOT NULL,

    CONSTRAINT fk_certificado_usuario
    FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE,
    CONSTRAINT fk_certificado_evento
    FOREIGN KEY (ID_Evento) REFERENCES Evento(ID_Evento) ON DELETE CASCADE,
    CONSTRAINT unq_certificado
    UNIQUE (ID_Usuario, ID_Evento)
);

CREATE TABLE Feedback (
    ID_Feedback INT PRIMARY KEY,
    Nota INT NOT NULL,
    Descricao TEXT,
    Data_Feedback TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Matricula INT NOT NULL,
    ID_Cardapio INT NOT NULL,

    CONSTRAINT chk_nota CHECK (Nota BETWEEN 1 AND 5),
    CONSTRAINT fk_feedback_estudante
    FOREIGN KEY (Matricula) REFERENCES Estudante(Matricula) ON DELETE CASCADE,
    CONSTRAINT fk_feedback_cardapio
    FOREIGN KEY (ID_Cardapio) REFERENCES Cardapio(ID_Cardapio) ON DELETE CASCADE,
    CONSTRAINT unq_feedback
    UNIQUE (Matricula, ID_Cardapio)
);

INSERT INTO Usuario (ID_Usuario, Nome, Senha, Data_Nascimento, Email)
VALUES (3001, 'Fernanda Lima', 'unb1', '1990-05-15', 'fernanda@unb.br')
ON CONFLICT DO NOTHING;

INSERT INTO Funcionario (ID_Funcionario, Salario, ID_Usuario)
VALUES (2001, 8500.00, 3001)
ON CONFLICT DO NOTHING;

INSERT INTO Nutricionista (ID_Funcionario)
VALUES (2001)
ON CONFLICT DO NOTHING;

INSERT INTO Usuario (ID_Usuario, Nome, Senha, Data_Nascimento, Email)
VALUES (3002, 'Marcos Pereira', 'unb1', '1987-11-03', 'marcos@unb.br')
ON CONFLICT DO NOTHING;

INSERT INTO Funcionario (ID_Funcionario, Salario, ID_Usuario)
VALUES (2002, 9200.00, 3002)
ON CONFLICT DO NOTHING;

INSERT INTO Gerente (ID_Funcionario)
VALUES (2002)
ON CONFLICT DO NOTHING;

INSERT INTO Usuario (ID_Usuario, Nome, Senha, Data_Nascimento, Email)
VALUES (3003, 'Joao Silva', 'unb1', '2003-04-20', 'joao@unb.br')
ON CONFLICT DO NOTHING;

INSERT INTO Estudante (Matricula, Saldo_RU, Curso, ID_Usuario)
VALUES (24100001, 0.00, 'Ciencia da Computacao', 3003)
ON CONFLICT DO NOTHING;

INSERT INTO ItemCardapio (ID_ItemCardapio, Categoria, Nome, ID_Nutricionista) VALUES
(10001, 'Bebida', 'Suco de laranja', 2001),
(10002, 'Bebida', 'Suco de acerola', 2001),
(10003, 'Bebida', 'Café preto', 2001),
(10004, 'Bebida', 'Chá de ervas', 2001),
(10005, 'Panificação', 'Pão francês', 2001),
(10006, 'Panificação', 'Pão integral', 2001),
(10007, 'Panificação', 'Tapioca simples', 2001),
(10008, 'Complemento', 'Manteiga', 2001),
(10009, 'Complemento', 'Queijo coalho', 2001),
(10010, 'Complemento', 'Ovo mexido', 2001),
(10011, 'Fruta', 'Banana', 2001),
(10012, 'Fruta', 'Maçã', 2001),
(10013, 'Fruta', 'Mamão', 2001),
(10014, 'Prato Principal', 'Frango grelhado', 2001),
(10015, 'Prato Principal', 'Carne de panela', 2001),
(10016, 'Prato Principal', 'Peixe assado', 2001),
(10017, 'Prato Principal', 'Almôndegas ao molho', 2001),
(10018, 'Prato Principal', 'Lasanha de legumes', 2001),
(10019, 'Guarnição', 'Arroz branco', 2001),
(10020, 'Guarnição', 'Arroz integral', 2001),
(10021, 'Guarnição', 'Feijão carioca', 2001),
(10022, 'Guarnição', 'Feijão preto', 2001),
(10023, 'Guarnição', 'Purê de batata', 2001),
(10024, 'Guarnição', 'Farofa de cenoura', 2001),
(10025, 'Salada', 'Salada verde', 2001),
(10026, 'Salada', 'Salada de tomate', 2001),
(10027, 'Salada', 'Salada de beterraba', 2001),
(10028, 'Salada', 'Salada de repolho', 2001),
(10029, 'Sobremesa', 'Gelatina', 2001),
(10030, 'Sobremesa', 'Melancia', 2001),
(10031, 'Sobremesa', 'Doce de banana', 2001),
(10032, 'Sobremesa', 'Mousse de maracujá', 2001)
ON CONFLICT DO NOTHING;

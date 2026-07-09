CREATE TABLE Usuario (
    ID_Usuario SERIAL PRIMARY KEY,
    Nome VARCHAR(150) NOT NULL,
    Senha VARCHAR(255) NOT NULL, 
    Data_Nascimento DATE NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Evento (
    ID_Evento SERIAL PRIMARY KEY,
    Data_inicio TIMESTAMP NOT NULL,
    Data_fim TIMESTAMP NOT NULL,
    Descricao TEXT NOT NULL,
    Foto_capa BYTEA,
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
    FOREIGN KEY (ID_Nutricionista) REFERENCES Nutricionista(ID_Funcionario) -- Mantido sem cascade para evitar que demitir nutricionista apague itens de comida salvos historicamente
);

CREATE TABLE Cardapio (
    ID_Cardapio INT PRIMARY KEY,
    Data_Inicio DATE NOT NULL,
    Data_Fim DATE NOT NULL,
    Status VARCHAR(20) DEFAULT 'Incompleto',
    ID_Funcionario INT,
    Nota_Media DECIMAL(3, 2) DEFAULT 0.00, 
    
    CONSTRAINT chk_status_cardapio CHECK (Status IN ('Incompleto', 'Completo', 'Publicado')),
    CONSTRAINT periodo_cardapio CHECK (Data_Fim >= Data_Inicio),
    CONSTRAINT fk_cardapio_editor  
    FOREIGN KEY (ID_Funcionario) REFERENCES Nutricionista(ID_Funcionario) ON DELETE SET NULL -- Modificado: se o nutricionista for apagado, o cardápio não some, o campo fica nulo.
);

CREATE TABLE Inscricao (
    Matricula INT NOT NULL, 
    ID_Evento INT NOT NULL,
    Data_Inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (Matricula, ID_Evento),
    CONSTRAINT fk_inscricao_estudante FOREIGN KEY (Matricula) REFERENCES Estudante(Matricula) ON DELETE CASCADE,
    CONSTRAINT fk_inscricao_evento FOREIGN KEY (ID_Evento) REFERENCES Evento(ID_Evento) ON DELETE CASCADE
);

CREATE TABLE Cardapio_Contem_Item (
    ID_Cardapio INT NOT NULL,
    ID_ItemCardapio INT NOT NULL,
    Periodo VARCHAR(20) NOT NULL,
    Dia_Semana VARCHAR(20) NOT NULL,
    Composicao TEXT NOT NULL,
    PRIMARY KEY (ID_Cardapio, Dia_Semana, Periodo, Composicao),
    CONSTRAINT fk_cardapio_item_cardapio FOREIGN KEY (ID_Cardapio) REFERENCES Cardapio(ID_Cardapio) ON DELETE CASCADE,
    CONSTRAINT fk_cardapio_item_item FOREIGN KEY (ID_ItemCardapio) REFERENCES ItemCardapio(ID_ItemCardapio) ON DELETE CASCADE
);

CREATE TABLE Transacao (
    ID_Transacao SERIAL PRIMARY KEY,
    Valor DECIMAL(10,2) NOT NULL,
    Data_Hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Matricula INT NOT NULL,
    CONSTRAINT fk_transacao_estudante FOREIGN KEY (Matricula) REFERENCES Estudante(Matricula) ON DELETE CASCADE
);

CREATE TABLE Preferencias (
    ID_Usuario INT NOT NULL,
    Preferencia VARCHAR(50) NOT NULL,
    PRIMARY KEY (ID_Usuario, Preferencia),
    CONSTRAINT fk_preferencias_usuario FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE
);

CREATE TABLE Certificado (
    ID_Certificado INT PRIMARY KEY,
    Data_Emissao DATE NOT NULL,
    Creditos INT NOT NULL,
    ID_Usuario INT NOT NULL,
    ID_Evento INT NOT NULL,
    CONSTRAINT fk_certificado_usuario FOREIGN KEY (ID_Usuario) REFERENCES Usuario(ID_Usuario) ON DELETE CASCADE,
    CONSTRAINT fk_certificado_evento FOREIGN KEY (ID_Evento) REFERENCES Evento(ID_Evento) ON DELETE CASCADE,
    CONSTRAINT unq_certificado UNIQUE (ID_Usuario, ID_Evento)
);

CREATE TABLE Feedback (
    ID_Feedback SERIAL PRIMARY KEY,
    Nota INT NOT NULL,
    Descricao TEXT,
    Data_Feedback TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Matricula INT NOT NULL,
    ID_Cardapio INT NOT NULL,
    CONSTRAINT chk_nota CHECK (Nota BETWEEN 1 AND 5),
    CONSTRAINT fk_feedback_estudante FOREIGN KEY (Matricula) REFERENCES Estudante(Matricula) ON DELETE CASCADE,
    CONSTRAINT fk_feedback_cardapio FOREIGN KEY (ID_Cardapio) REFERENCES Cardapio(ID_Cardapio) ON DELETE CASCADE,
    CONSTRAINT unq_feedback UNIQUE (Matricula, ID_Cardapio)
);

SELECT setval('usuario_id_usuario_seq', (SELECT MAX(id_usuario) FROM Usuario));
SELECT setval('evento_id_evento_seq', (SELECT MAX(id_evento) FROM Evento));
SELECT setval('transacao_id_transacao_seq', (SELECT MAX(id_transacao) FROM Transacao));
SELECT setval('feedback_id_feedback_seq', (SELECT MAX(id_feedback) FROM Feedback));
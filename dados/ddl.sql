CREATE TABLE IF NOT EXISTS contatos (
	id SERIAL NOT NULL PRIMARY KEY,
	nome VARCHAR(100),
    telefone VARCHAR(20),
    data_nascimento DATE,
    detalhes TEXT
);
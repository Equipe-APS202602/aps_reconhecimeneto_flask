drop database cofre_meio_ambiente;


CREATE DATABASE cofre_meio_ambiente;

USE cofre_meio_ambiente;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha_hash VARCHAR(255),
    cargo ENUM(
        'MINISTRO',
        'DIRETOR',
        'FUNCIONARIO'
    ) NOT NULL,
    face_id INT UNIQUE,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE DATABASE cofre_meio_ambiente;

USE cofre_meio_ambiente;

INSERT INTO usuarios
(nome, email, cargo, face_id)
VALUES
('Ministro do Meio Ambiente',
 'ministro@ambiente.gov.br',
 'MINISTRO',
 1),

('Diretor de Segurança',
 'diretor@ambiente.gov.br',
 'DIRETOR',
 2),

('Funcionário Administrativo',
 'funcionario@ambiente.gov.br',
 'FUNCIONARIO',
 3);
 
 CREATE TABLE registros_cofre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nome_ficticio VARCHAR(100) NOT NULL,
    classificacao VARCHAR(50),
    nivel_acesso ENUM(
        'FUNCIONARIO',
        'DIRETOR',
        'MINISTRO'
    ) NOT NULL,
    descricao TEXT,
    quantidade_simulada INT DEFAULT 0,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO registros_cofre
(codigo, nome_ficticio, classificacao,
 nivel_acesso, descricao, quantidade_simulada)
VALUES
(
 'TOX-001',
 'Substância Alfa',
 'CRÍTICA',
 'MINISTRO',
 'Registro fictício para fins acadêmicos.',
 10
),
(
 'TOX-002',
 'Substância Beta',
 'ALTA',
 'DIRETOR',
 'Registro fictício para fins acadêmicos.',
 20
),
(
 'TOX-003',
 'Substância Gama',
 'CONTROLADA',
 'FUNCIONARIO',
 'Registro fictício para fins acadêmicos.',
 30
);

CREATE TABLE logs_acesso (
    id INT AUTO_INCREMENT PRIMARY KEY,

    usuario_id INT,

    acao VARCHAR(150) NOT NULL,

    recurso VARCHAR(150),

    resultado ENUM(
        'PERMITIDO',
        'NEGADO'
    ) NOT NULL,

    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
);
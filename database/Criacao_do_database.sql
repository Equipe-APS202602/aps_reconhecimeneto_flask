-- ============================================================
-- BANCO DE DADOS - COFRE DO MEIO AMBIENTE
-- ============================================================

DROP DATABASE IF EXISTS cofre_meio_ambiente2;

CREATE DATABASE cofre_meio_ambiente2
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE cofre_meio_ambiente2;


-- ============================================================
-- 1. TABELA DE USUÁRIOS
-- ============================================================

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,

    nome VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    cargo ENUM(
        'FUNCIONARIO',
        'DIRETOR',
        'MINISTRO'
    ) NOT NULL,

    face_id INT UNIQUE,

    senha_hash VARCHAR(255),

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 2. USUÁRIOS
-- ============================================================

INSERT INTO usuarios
(nome, email, cargo, face_id)
VALUES
(
    'Ministro do Meio Ambiente',
    'ministro@ambiente.gov.br',
    'MINISTRO',
    1
),
(
    'Diretor de Segurança',
    'diretor@ambiente.gov.br',
    'DIRETOR',
    2
),
(
    'Funcionário Administrativo',
    'funcionario@ambiente.gov.br',
    'FUNCIONARIO',
    3
);


-- ============================================================
-- 3. SENHAS DOS USUÁRIOS
-- ============================================================

UPDATE usuarios
SET senha_hash =
'scrypt:32768:8:1$MG2d16gGYoWtKHHT$bc24745e8f3731c94a8fd19b377b19a1a54afd5e146b8779d1fd79e07863600d7e0786b00a407b83174da2e8c1b3936927889a85282a67d70fa71f9d7a7cc65c'
WHERE id = 1;


UPDATE usuarios
SET senha_hash =
'scrypt:32768:8:1$l3Pi4xWB73oLCFiD$4d58a449270fdc6925c23c80c00868654461d23bf8c821b62732126f42d524f64fb2ce0c43c7a7c9a67a6cebcf4c089a33051a8f0ae337a5ce9ccb96a4532014'
WHERE id = 2;


UPDATE usuarios
SET senha_hash =
'scrypt:32768:8:1$tjxoHpPwxngUYfCK$3ccb3e05023389b5ef60a32f41589e10225ab50ed1bf41d0e57b6918195ef49f73526a3772cd5e539ce35344faea696c0f7c38b22d202fa89814b2d819576be2'
WHERE id = 3;


-- ============================================================
-- 4. REGISTROS DO COFRE
-- ============================================================

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


-- ============================================================
-- 5. DADOS FICTÍCIOS DO COFRE
-- ============================================================

INSERT INTO registros_cofre
(
    codigo,
    nome_ficticio,
    classificacao,
    nivel_acesso,
    descricao,
    quantidade_simulada
)
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


-- ============================================================
-- 6. LOGS DE ACESSO
-- ============================================================

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

    CONSTRAINT fk_logs_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE SET NULL
);


-- ============================================================
-- 7. VERIFICAÇÃO DOS DADOS
-- ============================================================

SELECT * FROM usuarios;

SELECT * FROM registros_cofre;

SELECT * FROM logs_acesso;


-- ============================================================
-- 8. VERIFICAÇÃO DAS SENHAS
-- ============================================================

SELECT
    id,
    nome,
    email,
    cargo,
    face_id,
    senha_hash
FROM usuarios;
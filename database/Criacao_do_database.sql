```sql
-- =====================================================
-- COFRE DIGITAL - MINISTÉRIO DO MEIO AMBIENTE
-- Banco de dados: cofre_meio_ambiente2
-- =====================================================

DROP DATABASE IF EXISTS cofre_meio_ambiente2;

CREATE DATABASE cofre_meio_ambiente2
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE cofre_meio_ambiente2;

-- =====================================================
-- 1. TABELA DE USUÁRIOS
-- =====================================================

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NULL,

    cargo ENUM(
        'MINISTRO',
        'DIRETOR',
        'FUNCIONARIO'
    ) NOT NULL,

    face_id INT UNIQUE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    cadastrado_por INT NULL,
    foto_perfil VARCHAR(255) NULL,

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuario_cadastrador
        FOREIGN KEY (cadastrado_por)
        REFERENCES usuarios(id)
        ON DELETE SET NULL
);

-- =====================================================
-- 2. USUÁRIOS INICIAIS
-- =====================================================

INSERT INTO usuarios
    (nome, email, cargo, face_id, senha_hash, ativo)
VALUES
(
    'Ministro do Meio Ambiente',
    'ministro@ambiente.gov.br',
    'MINISTRO',
    1,
    'scrypt:32768:8:1$MG2d16gGYoWtKHHT$bc24745e8f3731c94a8fd19b377b19a1a54afd5e146b8779d1fd79e07863600d7e0786b00a407b83174da2e8c1b3936927889a85282a67d70fa71f9d7a7cc65c',
    TRUE
),
(
    'Diretor de Segurança',
    'diretor@ambiente.gov.br',
    'DIRETOR',
    2,
    'scrypt:32768:8:1$l3Pi4xWB73oLCFiD$4d58a449270fdc6925c23c80c00868654461d23bf8c821b62732126f42d524f64fb2ce0c43c7a7c9a67a6cebcf4c089a33051a8f0ae337a5ce9ccb96a4532014',
    TRUE
),
(
    'Funcionário Administrativo',
    'funcionario@ambiente.gov.br',
    'FUNCIONARIO',
    3,
    'scrypt:32768:8:1$tjxoHpPwxngUYfCK$3ccb3e05023389b5ef60a32f41589e10225ab50ed1bf41d0e57b6918195ef49f73526a3772cd5e539ce35344faea696c0f7c38b22d202fa89814b2d819576be2',
    TRUE
);


-- Os usuários iniciais ainda precisam ter suas senhas
-- cadastradas ou atualizadas com hashes válidos.
-- Não armazene senhas em texto puro.


-- ============================================================
-- 2.1. SENHAS DOS USUÁRIOS
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

-- =====================================================
-- 3. TABELA DE REGISTROS DO COFRE
-- =====================================================

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

-- =====================================================
-- 4. REGISTROS FICTÍCIOS
-- =====================================================

INSERT INTO registros_cofre
(codigo, nome_ficticio, classificacao, nivel_acesso,
 descricao, quantidade_simulada)
VALUES
('TOX-001', 'Substância Alfa', 'CRÍTICA', 'MINISTRO',
 'Registro fictício para fins acadêmicos.', 10),

('TOX-002', 'Substância Beta', 'ALTA', 'DIRETOR',
 'Registro fictício para fins acadêmicos.', 20),

('TOX-003', 'Substância Gama', 'CONTROLADA', 'FUNCIONARIO',
 'Registro fictício para fins acadêmicos.', 30),

('TOX-004', 'Névoa de Ônix', 'ALTA', 'DIRETOR',
 'Substância fictícia para testes de controle de acesso.', 12),

('TOX-005', 'Véu Carmesim', 'CRÍTICA', 'MINISTRO',
 'Registro acadêmico fictício de acesso ministerial.', 5),

('TOX-006', 'Cristal Nébula', 'CONTROLADA', 'FUNCIONARIO',
 'Material fictício para demonstrar operações de consulta.', 24),

('TOX-007', 'Orvalho Cinzento', 'BAIXA', 'FUNCIONARIO',
 'Registro inventado para testes de listagem.', 40),

('TOX-008', 'Íris de Mercúrio', 'ALTA', 'DIRETOR',
 'Registro fictício restrito à direção.', 8),

('TOX-009', 'Sombra Azul', 'CONTROLADA', 'FUNCIONARIO',
 'Composto imaginário para fins demonstrativos.', 18),

('TOX-010', 'Âmbar Fantasma', 'CRÍTICA', 'MINISTRO',
 'Registro fictício protegido pelo nível ministerial.', 3),

('TOX-011', 'Lótus de Ferro', 'ALTA', 'DIRETOR',
 'Registro para testes de filtros e classificação.', 9),

('TOX-012', 'Bruma Esmeralda', 'BAIXA', 'FUNCIONARIO',
 'Entrada fictícia de baixa classificação.', 35),

('TOX-013', 'Eco Violeta', 'CONTROLADA', 'FUNCIONARIO',
 'Registro simulado para consultas no cofre digital.', 16),

('TOX-014', 'Prisma Abissal', 'CRÍTICA', 'MINISTRO',
 'Entidade imaginária criada para documentação acadêmica.', 2),

('TOX-015', 'Aurora Obsidiana', 'ALTA', 'DIRETOR',
 'Registro fictício para demonstrar proteção de informações.', 7),

('TOX-016', 'Pólen Lunar', 'BAIXA', 'FUNCIONARIO',
 'Substância inventada para testes de ordenação.', 28),

('TOX-017', 'Chama Silenciosa', 'CONTROLADA', 'DIRETOR',
 'Entrada fictícia para validação de permissões gerenciais.', 11),

('TOX-018', 'Maré de Safira', 'ALTA', 'DIRETOR',
 'Composto fictício classificado como de alta prioridade.', 6),

('TOX-019', 'Fragmento Boreal', 'BAIXA', 'FUNCIONARIO',
 'Registro demonstrativo sem propriedades reais atribuídas.', 32),

('TOX-020', 'Vórtice Dourado', 'CRÍTICA', 'MINISTRO',
 'Registro fictício de acesso ministerial.', 4),

('TOX-021', 'Jardim de Névoa', 'CONTROLADA', 'FUNCIONARIO',
 'Substância inventada para operações de consulta.', 21),

('TOX-022', 'Estrela Oca', 'ALTA', 'DIRETOR',
 'Entrada simulada para testes de acesso da direção.', 10),

('TOX-023', 'Silício Fantasma', 'BAIXA', 'FUNCIONARIO',
 'Nome fictício para verificar a consistência dos registros.', 45),

('TOX-024', 'Rubi Nebuloso', 'CRÍTICA', 'MINISTRO',
 'Registro fictício sujeito ao nível máximo de acesso.', 1),

('TOX-025', 'Orbe de Cristal', 'CONTROLADA', 'DIRETOR',
 'Entrada fictícia para testes de acesso gerencial.', 14),

('TOX-026', 'Vento de Jade', 'BAIXA', 'FUNCIONARIO',
 'Registro demonstrativo para buscas por nome e código.', 26),

('TOX-027', 'Eclipse de Prata', 'ALTA', 'DIRETOR',
 'Substância imaginária para testar filtros e permissões.', 13),

('TOX-028', 'Lago Carmim', 'CONTROLADA', 'FUNCIONARIO',
 'Registro inventado de classificação controlada.', 19),

('TOX-029', 'Horizonte Índigo', 'CRÍTICA', 'MINISTRO',
 'Entrada fictícia reservada ao nível ministerial.', 2),

('TOX-030', 'Núcleo de Gelo', 'BAIXA', 'FUNCIONARIO',
 'Substância imaginária para testes de quantidade.', 38),

('TOX-031', 'Pérola Sombria', 'ALTA', 'DIRETOR',
 'Registro fictício de alta classificação.', 7),

('TOX-032', 'Nebulosa Rubra', 'CONTROLADA', 'FUNCIONARIO',
 'Entrada acadêmica inventada para testes de navegação.', 22),

('TOX-033', 'Arco Celeste', 'CRÍTICA', 'MINISTRO',
 'Registro fictício para demonstrar a proteção de dados.', 3);

-- =====================================================
-- 5. TABELA DE LOGS DE ACESSO
-- =====================================================

CREATE TABLE logs_acesso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL,
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

-- =====================================================
-- 6. TABELA DE SEGUNDA VERIFICAÇÃO
-- =====================================================
-- Opcional: utilize somente se o backend do projeto
-- realmente consultar esta tabela.
-- id_face referencia usuarios.face_id.

CREATE TABLE segunda_verificacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_face INT UNIQUE,
    senha VARCHAR(255) NOT NULL,

    CONSTRAINT fk_segunda_verificacao_face
        FOREIGN KEY (id_face)
        REFERENCES usuarios(face_id)
        ON DELETE CASCADE
);

-- =====================================================
-- 7. CONSULTAS DE CONFERÊNCIA
-- =====================================================

SELECT * FROM usuarios ORDER BY id;
SELECT * FROM registros_cofre ORDER BY id;
SELECT * FROM logs_acesso ORDER BY data_hora DESC;
SELECT * FROM segunda_verificacao;

SELECT
    u.id,
    u.nome,
    u.email,
    u.cargo,
    u.face_id,
    u.ativo,
    u.cadastrado_por,
    cadastrador.nome AS nome_cadastrador,
    u.foto_perfil,
    u.criado_em
FROM usuarios AS u
LEFT JOIN usuarios AS cadastrador
    ON u.cadastrado_por = cadastrador.id
ORDER BY u.id;

SELECT COUNT(*) AS total_usuarios FROM usuarios;
SELECT COUNT(*) AS total_registros FROM registros_cofre;
SELECT COUNT(*) AS total_logs FROM logs_acesso;
```

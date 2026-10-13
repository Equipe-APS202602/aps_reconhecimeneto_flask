# Banco de Dados — Cofre Digital

O script abaixo cria as tabelas e os dados iniciais para uma instalação nova do projeto.

```sql
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

    ativo TINYINT(1) NOT NULL DEFAULT 1,
    foto_perfil VARCHAR(255) NULL,
    cadastrado_por INT NULL,

    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_usuario_cadastrador
        FOREIGN KEY (cadastrado_por)
        REFERENCES usuarios(id)
        ON DELETE SET NULL
);


-- ============================================================
-- 2. USUÁRIOS INICIAIS
-- ============================================================

INSERT INTO usuarios
(nome, email, cargo, face_id, senha_hash, ativo)
VALUES
(
    'Ministro do Meio Ambiente',
    'ministro@ambiente.gov.br',
    'MINISTRO',
    1,
    'scrypt:32768:8:1$MG2d16gGYoWtKHHT$bc24745e8f3731c94a8fd19b377b19a1a54afd5e146b8779d1fd79e07863600d7e0786b00a407b83174da2e8c1b3936927889a85282a67d70fa71f9d7a7cc65c',
    1
),
(
    'Diretor de Segurança',
    'diretor@ambiente.gov.br',
    'DIRETOR',
    2,
    'scrypt:32768:8:1$l3Pi4xWB73oLCFiD$4d58a449270fdc6925c23c80c00868654461d23bf8c821b62732126f42d524f64fb2ce0c43c7a7c9a67a6cebcf4c089a33051a8f0ae337a5ce9ccb96a4532014',
    1
),
(
    'Funcionário Administrativo',
    'funcionario@ambiente.gov.br',
    'FUNCIONARIO',
    3,
    'scrypt:32768:8:1$tjxoHpPwxngUYfCK$3ccb3e05023389b5ef60a32f41589e10225ab50ed1bf41d0e57b6918195ef49f73526a3772cd5e539ce35344faea696c0f7c38b22d202fa89814b2d819576be2',
    1
);


-- ============================================================
-- 3. REGISTROS DO COFRE
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
-- 4. DADOS FICTÍCIOS DO COFRE - 33 REGISTROS
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
    'Registro fictício de classificação crítica, utilizado para demonstrar o acesso restrito a informações sensíveis.',
    10
),
(
    'TOX-002',
    'Substância Beta',
    'ALTA',
    'DIRETOR',
    'Substância imaginária destinada a testes de consulta e controle de permissões da direção.',
    20
),
(
    'TOX-003',
    'Substância Gama',
    'CONTROLADA',
    'FUNCIONARIO',
    'Registro demonstrativo de acesso operacional, criado para testar a listagem de informações autorizadas.',
    30
),
(
    'TOX-004',
    'Névoa de Ônix',
    'ALTA',
    'DIRETOR',
    'Substância inteiramente fictícia, utilizada para simular um registro de alta prioridade no sistema.',
    12
),
(
    'TOX-005',
    'Véu Carmesim',
    'CRÍTICA',
    'MINISTRO',
    'Registro imaginário protegido pelo nível ministerial para demonstrar a restrição de dados críticos.',
    5
),
(
    'TOX-006',
    'Cristal Nébula',
    'CONTROLADA',
    'FUNCIONARIO',
    'Entrada fictícia para testes de cadastro, consulta e apresentação de descrições.',
    24
),
(
    'TOX-007',
    'Orvalho Cinzento',
    'BAIXA',
    'FUNCIONARIO',
    'Registro de demonstração utilizado para validar filtros e ordenação de dados.',
    40
),
(
    'TOX-008',
    'Íris de Mercúrio',
    'ALTA',
    'DIRETOR',
    'Substância inventada para representar informações gerenciais de acesso restrito.',
    8
),
(
    'TOX-009',
    'Sombra Azul',
    'CONTROLADA',
    'FUNCIONARIO',
    'Composto imaginário sem correspondência com uma substância real, destinado a testes acadêmicos.',
    18
),
(
    'TOX-010',
    'Âmbar Fantasma',
    'CRÍTICA',
    'MINISTRO',
    'Registro fictício utilizado para demonstrar a proteção de dados classificados no nível máximo.',
    3
),
(
    'TOX-011',
    'Lótus de Ferro',
    'ALTA',
    'DIRETOR',
    'Entrada simulada para testar a visualização de registros conforme o cargo do usuário.',
    9
),
(
    'TOX-012',
    'Bruma Esmeralda',
    'BAIXA',
    'FUNCIONARIO',
    'Substância inventada para validar a exibição de informações de baixa classificação.',
    35
),
(
    'TOX-013',
    'Eco Violeta',
    'CONTROLADA',
    'FUNCIONARIO',
    'Registro demonstrativo utilizado em testes de pesquisa e navegação pelo cofre.',
    16
),
(
    'TOX-014',
    'Prisma Abissal',
    'CRÍTICA',
    'MINISTRO',
    'Entidade química imaginária criada exclusivamente para fins de documentação e demonstração.',
    2
),
(
    'TOX-015',
    'Aurora Obsidiana',
    'ALTA',
    'DIRETOR',
    'Registro fictício destinado a demonstrar a proteção de informações administrativas.',
    7
),
(
    'TOX-016',
    'Pólen Lunar',
    'BAIXA',
    'FUNCIONARIO',
    'Entrada fictícia para testes de consistência, listagem e consulta de registros.',
    28
),
(
    'TOX-017',
    'Chama Silenciosa',
    'CONTROLADA',
    'DIRETOR',
    'Substância imaginária utilizada para testar permissões gerenciais sobre dados controlados.',
    11
),
(
    'TOX-018',
    'Maré de Safira',
    'ALTA',
    'DIRETOR',
    'Composto inventado classificado como de alta prioridade no cenário acadêmico.',
    6
),
(
    'TOX-019',
    'Fragmento Boreal',
    'BAIXA',
    'FUNCIONARIO',
    'Registro de demonstração sem propriedades químicas reais atribuídas.',
    32
),
(
    'TOX-020',
    'Vórtice Dourado',
    'CRÍTICA',
    'MINISTRO',
    'Entrada fictícia de acesso restrito para simulações de segurança e autorização.',
    4
),
(
    'TOX-021',
    'Jardim de Névoa',
    'CONTROLADA',
    'FUNCIONARIO',
    'Registro imaginário criado para demonstrar consultas básicas e apresentação de dados.',
    21
),
(
    'TOX-022',
    'Estrela Oca',
    'ALTA',
    'DIRETOR',
    'Entrada simulada para verificar a exibição de registros reservados à direção.',
    10
),
(
    'TOX-023',
    'Silício Fantasma',
    'BAIXA',
    'FUNCIONARIO',
    'Substância fictícia criada para verificar a integridade da listagem de registros.',
    45
),
(
    'TOX-024',
    'Rubi Nebuloso',
    'CRÍTICA',
    'MINISTRO',
    'Registro acadêmico imaginário protegido pelo nível de acesso ministerial.',
    1
),
(
    'TOX-025',
    'Orbe de Cristal',
    'CONTROLADA',
    'DIRETOR',
    'Entrada fictícia destinada a testar o acesso gerencial a registros controlados.',
    14
),
(
    'TOX-026',
    'Vento de Jade',
    'BAIXA',
    'FUNCIONARIO',
    'Registro demonstrativo para validar pesquisas por nome e código.',
    26
),
(
    'TOX-027',
    'Eclipse de Prata',
    'ALTA',
    'DIRETOR',
    'Substância inventada para testes de classificação e restrição de acesso.',
    13
),
(
    'TOX-028',
    'Lago Carmim',
    'CONTROLADA',
    'FUNCIONARIO',
    'Entrada fictícia utilizada para demonstrar a apresentação de dados controlados.',
    19
),
(
    'TOX-029',
    'Horizonte Índigo',
    'CRÍTICA',
    'MINISTRO',
    'Registro imaginário reservado ao nível ministerial para testes de autorização.',
    2
),
(
    'TOX-030',
    'Núcleo de Gelo',
    'BAIXA',
    'FUNCIONARIO',
    'Substância inventada para verificar a apresentação de quantidades simuladas.',
    38
),
(
    'TOX-031',
    'Pérola Sombria',
    'ALTA',
    'DIRETOR',
    'Registro fictício de alta classificação utilizado em testes de acesso gerencial.',
    7
),
(
    'TOX-032',
    'Nebulosa Rubra',
    'CONTROLADA',
    'FUNCIONARIO',
    'Entrada acadêmica fictícia para validar a consulta e a navegação dos registros.',
    22
),
(
    'TOX-033',
    'Arco Celeste',
    'CRÍTICA',
    'MINISTRO',
    'Registro imaginário criado para demonstrar a proteção de informações classificadas.',
    3
);


-- ============================================================
-- 5. LOGS DE ACESSO
-- ============================================================

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


-- ============================================================
-- 6. DADOS INICIAIS DE AUDITORIA
-- ============================================================

INSERT INTO logs_acesso
(usuario_id, acao, recurso, resultado)
VALUES
(1, 'INICIALIZACAO', 'COFRE DIGITAL', 'PERMITIDO'),
(2, 'INICIALIZACAO', 'COFRE DIGITAL', 'PERMITIDO'),
(3, 'INICIALIZACAO', 'COFRE DIGITAL', 'PERMITIDO');


-- ============================================================
-- 7. CONSULTAS PARA CONFERIR A CRIAÇÃO
-- ============================================================

SELECT
    id,
    nome,
    email,
    cargo,
    face_id,
    ativo,
    foto_perfil,
    cadastrado_por,
    criado_em
FROM usuarios;

SELECT
    id,
    codigo,
    nome_ficticio,
    classificacao,
    nivel_acesso,
    descricao,
    quantidade_simulada,
    criado_em
FROM registros_cofre
ORDER BY id;

SELECT
    id,
    usuario_id,
    acao,
    recurso,
    resultado,
    data_hora
FROM logs_acesso
ORDER BY id;

SELECT COUNT(*) AS total_usuarios
FROM usuarios;

SELECT COUNT(*) AS total_registros
FROM registros_cofre;

SELECT COUNT(*) AS total_logs
FROM logs_acesso;
```

## Observações importantes

1. **Senhas iniciais:** os hashes mantidos no script usam o formato `scrypt` do Werkzeug. O login precisa utilizar um verificador compatível, como `werkzeug.security.check_password_hash`. Se o seu login usar exclusivamente `bcrypt.checkpw`, será necessário ajustar a validação ou gerar hashes compatíveis.
2. **Reconhecimento facial:** os valores `face_id` são identificadores iniciais. O modelo LBPH precisa ser treinado com imagens cujos rótulos correspondam a esses IDs. Criar os usuários no banco não gera automaticamente o modelo facial.
3. **Fotos de perfil:** a coluna `foto_perfil` começa como `NULL`; cada usuário poderá cadastrar a própria foto pelo formulário implementado.
4. **Cadastro por usuário:** `cadastrado_por` permite associar um usuário ao responsável pelo cadastro. Os três usuários iniciais ficam com esse campo nulo.
5. **Acesso aos registros:** o campo `nivel_acesso` armazena o nível necessário. A rota de consulta precisa aplicar a regra de autorização; a coluna, sozinha, não bloqueia o acesso.
6. **Senhas de demonstração:** os hashes acima foram preservados do script original. Confirme que as credenciais correspondentes são conhecidas pela equipe antes de disponibilizar o sistema.

**Para validar a instalação**, o resultado esperado da consulta de contagem é de 3 usuários, 33 registros fictícios e 3 logs iniciais.

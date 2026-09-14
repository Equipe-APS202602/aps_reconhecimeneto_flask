
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


create table segunde_virific(
id INT AUTO_INCREMENT PRIMARY KEY,
id_face int unique,
senha VARCHAR(255) NOT NULL,
constraint fk_face_id foreign key(id_face)
references usuarios(face_id)
on delete cascade

);
select * from usuarios;
DROP table segunde_virific;

insert into segunde_virific
(id_face,senha)
values
(1,"scrypt:32768:8:1$MG2d16gGYoWtKHHT$bc24745e8f3731c94a8fd19b377b19a1a54afd5e146b8779d1fd79e07863600d7e0786b00a407b83174da2e8c1b3936927889a85282a67d70fa71f9d7a7cc65c")
;

update usuarios 
set senha_hash ="scrypt:32768:8:1$MG2d16gGYoWtKHHT$bc24745e8f3731c94a8fd19b377b19a1a54afd5e146b8779d1fd79e07863600d7e0786b00a407b83174da2e8c1b3936927889a85282a67d70fa71f9d7a7cc65c"
WHERE id = 1;
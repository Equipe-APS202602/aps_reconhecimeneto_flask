🔐 Cofre Digital — Sistema de Autenticação Biométrica Facial

Sistema acadêmico desenvolvido para controlar o acesso a informações sensíveis sobre toxinas de alta periculosidade. A aplicação utiliza reconhecimento facial, controle de permissões por nível de usuário e registro de auditoria para garantir que cada pessoa acesse somente os recursos autorizados.

Projeto desenvolvido para as Atividades Práticas Supervisionadas (APS) do curso de Ciência da Computação.

📌 Sobre o projeto

O Cofre Digital simula um sistema de segurança destinado ao Ministério do Meio Ambiente. Seu objetivo é proteger uma base de dados fictícia que contém informações sobre toxinas capazes de causar graves impactos à saúde e ao meio ambiente.

A autenticação é realizada por meio da captura da imagem do usuário pela câmera. Após o reconhecimento facial, o sistema consulta o cadastro no banco de dados e libera as funcionalidades correspondentes ao cargo identificado.

✨ Funcionalidades

Autenticação por reconhecimento facial;

Captura de imagem pela câmera do dispositivo;

Cadastro e gerenciamento de usuários;

Controle de acesso baseado no cargo do usuário;

Consulta de registros fictícios de toxinas;

Exibição de informações de acordo com o nível de permissão;

Registro de acessos e ações para auditoria;

Painéis personalizados para funcionário, diretor e ministro;

Bloqueio de páginas e operações não autorizadas.

👥 Níveis de acesso

Nível

Perfil

Permissões principais

1

Funcionário

Visualização limitada dos registros

2

Diretor

Visualização completa e alteração de registros

3

Ministro

Controle total, gerenciamento de usuários, exclusões e auditoria

🛠️ Tecnologias utilizadas

Python — linguagem principal;

Flask — desenvolvimento da aplicação web;

OpenCV — captura, detecção e reconhecimento facial;

LBPH — algoritmo de reconhecimento facial;

Haar Cascade — detecção de rostos nas imagens;

MySQL — armazenamento de usuários, registros e logs;

HTML5, CSS3 e JavaScript — interface e acesso à câmera;

Bootstrap — componentes e responsividade da interface.

📁 Estrutura do projeto

aps_reconhecimeneto_flask/
├── app.py
├── config.py
├── requirements.txt
├── auth/
│   ├── facial.py
│   └── permissions.py
├── database/
│   └── connection.py
├── facial/
│   ├── capture.py
│   ├── recognize.py
│   ├── models/
│   │   └── trainer.yml
│   └── trainer/
│       └── train.py
├── models/
│   ├── log.py
│   ├── toxina.py
│   └── usuario.py
├── routes/
│   ├── dashboard.py
│   ├── login.py
│   ├── logs.py
│   ├── toxinas.py
│   └── usuarios.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── camera.js
└── templates/
    ├── dashboard/
    ├── logs/
    ├── registros/
    ├── usuarios/
    ├── acesso_negado.html
    ├── base.html
    └── login.html

🚀 Como executar

Pré-requisitos

Antes de começar, instale:

Python;

MySQL;

Git;

Uma câmera ou webcam.

1. Clone o repositório

git clone https://github.com/Equipe-APS202602/aps_reconhecimeneto_flask.git
cd aps_reconhecimeneto_flask

2. Crie e ative um ambiente virtual

No Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1

No Linux ou macOS:

python3 -m venv venv
source venv/bin/activate

3. Instale as dependências

pip install -r requirements.txt

4. Configure o banco de dados

Crie o banco no MySQL e configure um arquivo .env na raiz do projeto:

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=cofre_meio_ambiente
SECRET_KEY=troque_por_uma_chave_segura

Nunca envie o arquivo .env ao GitHub. Ele deve permanecer listado no .gitignore.

5. Execute a aplicação

python app.py

Depois, abra no navegador:

http://127.0.0.1:5000

🔎 Funcionamento da autenticação

A página de login solicita acesso à câmera;

O sistema captura uma imagem do usuário;

O OpenCV detecta e recorta o rosto;

O modelo LBPH compara a imagem com os dados treinados;

O usuário correspondente é consultado no MySQL;

A sessão é criada com as permissões do cargo identificado;

A tentativa de acesso é registrada para auditoria.

🔒 Segurança e privacidade

Este projeto possui finalidade acadêmica e utiliza dados fictícios. Em um ambiente real, recomenda-se adicionar criptografia, proteção contra falsificação facial (liveness detection), HTTPS, política de senhas, limitação de tentativas e armazenamento seguro dos dados biométricos.

Arquivos com credenciais, imagens faciais e dados biométricos não devem ser publicados no repositório. Verifique o .gitignore antes de cada envio.

🎓 Objetivo acadêmico

O projeto busca integrar técnicas de análise de imagens e reconhecimento facial à implementação de mecanismos de segurança da informação. Por meio de diferentes níveis de permissão, a aplicação demonstra a importância da tecnologia para a proteção de dados sensíveis e para a prevenção de acessos realizados por pessoas não autorizadas.

👩‍💻 Equipe

Projeto desenvolvido pela equipe APS 2026/02, como parte do curso de Ciência da Computação.

⚠️ Aviso

As toxinas, instituições, registros e situações apresentados pelo sistema são fictícios e foram elaborados exclusivamente para demonstração acadêmica.

<p align="center">
  Desenvolvido para fins educacionais 💚
</p>
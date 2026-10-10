# 🔐 Cofre Digital — Sistema de Autenticação Biométrica Facial

Sistema web acadêmico desenvolvido para as Atividades Práticas Supervisionadas (APS) do curso de Ciência da Computação. O **Cofre Digital** simula um ambiente de controle de acesso a registros fictícios de substâncias, utilizando reconhecimento facial, autenticação de usuários, permissões por cargo e registro de atividades.

> **Projeto acadêmico:** desenvolvido pela equipe APS 2026/02 para fins educacionais. As substâncias, os registros e os cenários apresentados são fictícios.

## 📌 Sobre o projeto

O Cofre Digital simula um sistema de segurança institucional no qual diferentes usuários possuem níveis distintos de acesso às informações armazenadas.

A aplicação utiliza Python e Flask no backend, MySQL para persistência dos dados e OpenCV para processamento de imagens faciais. O sistema também disponibiliza painéis específicos por cargo, gerenciamento de usuários, fotos de perfil, consulta de registros e auditoria de atividades.

O objetivo é demonstrar a integração entre visão computacional, desenvolvimento web, banco de dados e segurança da informação.

## ✨ Funcionalidades

* Autenticação por reconhecimento facial.
* Captura de imagens por webcam.
* Cadastro e gerenciamento de usuários.
* Cadastro e atualização de fotos de perfil.
* Controle de acesso baseado no cargo do usuário.
* Consulta de registros fictícios de substâncias.
* Exibição de descrições e classificações dos registros.
* Restrição de informações conforme as permissões.
* Painéis personalizados para funcionário, diretor e ministro.
* Registro de atividades e tentativas de acesso.
* Histórico de auditoria.
* Interface web responsiva com Bootstrap.

## 👥 Níveis de acesso

| Nível | Perfil      | Permissões principais                                                                                                  |
| ----- | ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1     | Funcionário | Consulta de informações autorizadas e acesso operacional limitado.                                                     |
| 2     | Diretor     | Acesso ampliado e gerenciamento de funcionários, conforme as permissões implementadas.                                 |
| 3     | Ministro    | Gerenciamento de usuários e acesso administrativo ampliado, incluindo auditoria, conforme as permissões implementadas. |

As permissões efetivas são definidas no código do projeto, especialmente em `auth/permissions.py` e nas rotas correspondentes.

## 🛠️ Tecnologias utilizadas

* **Python 3.13:** linguagem de programação.
* **Flask:** framework web.
* **MySQL:** banco de dados relacional.
* **OpenCV:** processamento e análise de imagens.
* **LBPH:** algoritmo de reconhecimento facial utilizado no projeto.
* **Haar Cascade:** detector facial.
* **Flask-Login ou sessões Flask:** o mecanismo de autenticação depende da implementação presente no código.
* **bcrypt:** geração de hashes de senhas, quando utilizado pelo fluxo de cadastro.
* **HTML5, CSS3 e JavaScript:** estrutura, estilo e interatividade.
* **Bootstrap 5:** componentes visuais e responsividade.
* **Git e GitHub:** versionamento do código-fonte.

## 📋 Pré-requisitos

Antes de executar a aplicação, instale:

* [Python 3.13](https://www.python.org/downloads/)
* [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
* [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) — opcional, para administrar o banco visualmente.
* [Git](https://git-scm.com/downloads)
* Uma webcam, para utilizar a captura facial.

O acesso à câmera pelo navegador pode exigir `localhost` ou HTTPS. Para desenvolvimento local, utilize `http://127.0.0.1:5000`.

## 🚀 Instalação e execução

### 1. Clone o repositório

Abra o terminal e execute:

```bash
git clone https://github.com/Equipe-APS202602/aps_reconhecimeneto_flask.git
cd aps_reconhecimeneto_flask
```

Confira se você está na pasta que contém o arquivo `app.py`.

### 2. Crie um ambiente virtual

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, você pode executar o Python do ambiente virtual diretamente:

```powershell
.\venv\Scripts\python.exe -m pip install --upgrade pip
```

No Linux ou macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se o projeto utilizar o módulo `cv2.face`, confirme que o pacote OpenCV instalado disponibiliza o reconhecedor LBPH. Esse módulo é normalmente fornecido pelo pacote `opencv-contrib-python`.

Para verificar:

```bash
python -c "import cv2; print(cv2.__version__); print(hasattr(cv2, 'face'))"
```

O segundo resultado deve ser `True` quando o código depende de `cv2.face`.

Se houver conflito entre pacotes OpenCV instalados no mesmo ambiente, remova as variantes conflitantes e instale a versão compatível com o projeto. Evite instalar simultaneamente `opencv-python` e `opencv-contrib-python` no mesmo ambiente virtual.

### 4. Configure o MySQL

Inicie o serviço MySQL e abra o MySQL Workbench ou o cliente de sua preferência.

Crie o banco de dados utilizado pela aplicação. No ambiente atual do projeto, o nome configurado é `cofre_meio_ambiente2`.

```sql
CREATE DATABASE cofre_meio_ambiente2
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Se o código ou os scripts SQL do seu checkout utilizarem outro nome, mantenha o mesmo nome em toda a configuração.

### 5. Configure a conexão com o banco

O projeto utiliza o arquivo `database/config.json` para carregar os dados de conexão por meio de `database/connection.py`.

Crie esse arquivo localmente, dentro da pasta `database/`, com a estrutura esperada pelo código atual:

```json
{
    "-host-": "localhost",
    "-db-": "cofre_meio_ambiente2",
    "-user-": "root",
    "-senha-": "SUA_SENHA_MYSQL",
    "-porta-": "3306"
}
```

Substitua `SUA_SENHA_MYSQL` pela senha da sua instalação do MySQL.

**Importante:**

* O nome das chaves precisa corresponder exatamente ao que `database/connection.py` lê.
* O arquivo contém credenciais privadas e não deve ser enviado ao GitHub.
* Não publique sua senha nem a chave secreta da aplicação.
* Se o projeto possuir um arquivo SQL com as tabelas, execute-o no banco antes de iniciar a aplicação.

### 6. Crie as tabelas do banco de dados

A aplicação precisa das tabelas esperadas pelas rotas e pelos modelos, incluindo as relacionadas a:

* `usuarios`: usuários, cargos, hashes de senha, identificadores faciais e fotos de perfil.
* `registros_cofre`: registros fictícios, classificação, nível de acesso, descrição e quantidade simulada.
* `logs_acesso`: histórico de acessos e ações.

Utilize o script SQL fornecido pelo projeto, se houver, para criar a estrutura completa. Se não existir um script de inicialização, será necessário criar as tabelas de acordo com as consultas e os comandos SQL presentes no código.

Não basta criar o banco vazio: as tabelas e colunas precisam corresponder às utilizadas pelas rotas.

### 7. Prepare os diretórios locais

O projeto utiliza diretórios para armazenar imagens de treinamento, modelos faciais e fotos de perfil.

Verifique a existência das seguintes pastas:

```text
facial/
├── dataset/
├── models/
└── trainer/
    └── train.py

static/
└── uploads/
    └── fotos_perfil/
```

Se necessário, crie as pastas ausentes. A aplicação deve ter permissão para gravar arquivos nos diretórios utilizados para as imagens e os modelos.

As imagens faciais dos usuários e as fotos de perfil são dados privados. Não as publique no repositório.

### 8. Prepare o modelo de reconhecimento facial

O projeto utiliza o algoritmo LBPH e o detector Haar Cascade. O modelo treinado é esperado em:

```text
facial/models/trainer.yml
```

Esse arquivo pode ser gerado pelo treinamento do projeto. Como datasets e modelos treinados podem ser excluídos pelo `.gitignore`, eles talvez não estejam disponíveis após clonar o repositório.

Nesse caso:

1. Inicie a aplicação e cadastre os usuários pelo fluxo implementado.
2. Capture as imagens faciais conforme o procedimento de cadastro do projeto.
3. Confira se as imagens foram salvas no diretório de dataset esperado pelo código.
4. Execute o treinamento utilizando o procedimento ou script previsto no projeto.
5. Confirme que `facial/models/trainer.yml` foi criado antes de testar o reconhecimento.

O caminho do dataset, o formato dos identificadores e o comando exato de treinamento dependem da implementação de `facial/capture.py` e `facial/trainer/train.py`. Não renomeie pastas ou identificadores sem conferir como o código associa cada rosto ao usuário correspondente.

### 9. Inicie a aplicação

Na raiz do projeto, execute:

```bash
python app.py
```

Se você utiliza o Python instalado em `C:\python313`, também pode executar no PowerShell:

```powershell
& "C:\python313\python.exe" app.py
```

Não execute `routes/dashboard.py` diretamente: esse arquivo depende dos módulos e da inicialização definidos na aplicação Flask.

Quando o servidor iniciar, abra no navegador:

http://127.0.0.1:5000

A URL e a porta podem variar conforme a configuração presente em `app.py`.

## 🔎 Como funciona a autenticação facial

O fluxo geral do sistema é:

1. O usuário acessa a página de login.
2. A aplicação solicita acesso à câmera, quando necessário.
3. Uma imagem facial é capturada.
4. O OpenCV detecta e processa a região do rosto.
5. O reconhecedor LBPH compara a imagem com o modelo treinado.
6. A aplicação associa o resultado ao cadastro correspondente no banco de dados.
7. Após a validação, a sessão é configurada com as informações do usuário.
8. O sistema direciona o usuário ao painel correspondente ao seu cargo.
9. As rotas verificam as permissões antes de liberar recursos protegidos.
10. Os acessos e as ações relevantes são registrados para auditoria.

O reconhecimento facial e a autorização são etapas diferentes: identificar um rosto não deve, por si só, conceder acesso a informações protegidas. O sistema também precisa validar o cadastro e as permissões do usuário.

## 🗂️ Estrutura do projeto

A estrutura abaixo representa os principais diretórios e arquivos esperados. A organização exata pode variar conforme a versão do repositório.

```text
aps_reconhecimeneto_flask/
├── app.py
├── config.py
├── requirements.txt
├── auth/
│   ├── facial.py
│   └── permissions.py
├── database/
│   ├── connection.py
│   └── config.json              # Criado localmente; não publicar
├── facial/
│   ├── capture.py
│   ├── recognize.py
│   ├── dataset/                 # Imagens locais; não publicar
│   ├── models/
│   │   └── trainer.yml          # Gerado localmente, se necessário
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
│   ├── js/
│   └── uploads/
│       └── fotos_perfil/        # Fotos privadas dos usuários
└── templates/
    ├── dashboard/
    ├── logs/
    ├── registros/
    ├── usuarios/
    ├── acesso_negado.html
    ├── base.html
    └── login.html
```

## 🧪 Dados de demonstração

Os registros de substâncias utilizados no projeto são fictícios e destinados à demonstração de funcionalidades como:

* Listagem e consulta de registros.
* Exibição de descrições.
* Classificação dos registros.
* Controle de acesso por nível.
* Visualização de informações conforme as permissões.

Para preencher o banco com dados de demonstração, execute os scripts SQL disponibilizados pela equipe ou cadastre os registros pelo sistema, conforme as funcionalidades existentes.

## 🔒 Segurança e privacidade

Este é um projeto acadêmico e não deve ser utilizado para controlar o acesso a substâncias reais ou a informações de alto risco sem uma avaliação de segurança adequada.

Boas práticas para executar e compartilhar o projeto:

* Não publique `database/config.json`, arquivos `.env` ou outras credenciais.
* Não publique imagens faciais, datasets biométricos ou fotos privadas.
* Utilize hashes seguros para armazenar senhas.
* Valide as permissões no backend, não apenas na interface.
* Restrinja o tamanho e o tipo dos arquivos enviados.
* Utilize HTTPS em ambientes de produção.
* Considere mecanismos de detecção de apresentação (*liveness detection*) para reduzir tentativas de falsificação facial.
* Proteja os registros de auditoria contra alterações indevidas.
* Utilize dados fictícios para testes e apresentações.

O LBPH não substitui mecanismos completos de autenticação biométrica, e o projeto não deve ser considerado um sistema de segurança de produção.

## 🛠️ Solução de problemas

### Erro: `ModuleNotFoundError`

Confira se o ambiente virtual está ativado, se as dependências foram instaladas e se a execução está sendo feita a partir da raiz do projeto:

```bash
python app.py
```

### Erro de conexão com o MySQL

Confira se o serviço MySQL está ativo, se o banco existe e se os dados em `database/config.json` correspondem às configurações esperadas por `database/connection.py`.

### Erro: `cv2.face` não existe

Verifique a instalação do OpenCV e confirme se o ambiente utiliza uma versão compatível com o módulo de reconhecimento LBPH.

### Modelo facial não encontrado

Confira se `facial/models/trainer.yml` foi gerado e se o caminho definido no código aponta para esse arquivo.

### A câmera não funciona

Verifique as permissões da câmera no sistema operacional e no navegador. Em desenvolvimento local, acesse a aplicação por `http://127.0.0.1:5000`.

### O usuário é direcionado para o painel errado

Confira o cargo armazenado no banco, o valor colocado na sessão após o login e a seleção do template em `routes/dashboard.py`.

## 🎓 Objetivo acadêmico

O projeto integra conceitos de visão computacional, autenticação, autorização, desenvolvimento web e bancos de dados. Sua finalidade é demonstrar como diferentes componentes de software podem trabalhar juntos para organizar e restringir o acesso a informações de acordo com o perfil de cada usuário.

## 👩‍💻 Equipe

Projeto desenvolvido pela equipe **APS 2026/02**, como parte do curso de **Ciência da Computação**.

## ⚠️ Aviso

As substâncias, instituições, quantidades e situações descritas na aplicação são fictícias e foram criadas exclusivamente para fins educacionais.

---

<p align="center">
  Desenvolvido para fins educacionais.
</p>

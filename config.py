import os
from dotenv import load_dotenv

load_dotenv()


# Configuração do Flask
SECRET_KEY = os.getenv("SECRET_KEY", "aps2026")


# Configuração do banco MySQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "cofre_meio_ambiente")
DB_PORT = int(os.getenv("DB_PORT", "3306"))


# Configuração da aplicação
DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

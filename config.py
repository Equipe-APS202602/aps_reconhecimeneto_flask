import os
from dotenv import load_dotenv
from database.constant import host, database, user, password, port, secret_key
load_dotenv()


# Configuração do banco MySQL
SECRET_KEY = os.getenv("SECRET_KEY", secret_key)
DB_HOST = os.getenv("DB_HOST", host)
DB_USER = os.getenv("DB_USER", user)
DB_PASSWORD = os.getenv("DB_PASSWORD", password)
DB_NAME = os.getenv("DB_NAME", database)
DB_PORT = int(os.getenv("DB_PORT", port))


# Configuração da aplicação
DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"

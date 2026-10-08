import json
import os
import mysql.connector

# =========================================================
# CAMINHO DO CONFIG.JSON
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")


# =========================================================
# CARREGAR CONFIGURAÇÕES
# =========================================================

with open(CONFIG_PATH, "r", encoding="utf-8") as arquivo:
    config = json.load(arquivo)


# =========================================================
# CONEXÃO COM MYSQL
# =========================================================


def get_connection():

    return mysql.connector.connect(
        host=config["-host-"],
        database=config["-db-"],
        user=config["-user-"],
        password=config["-senha-"],
        port=int(config["-porta-"]),
    )


# =========================================================
# TESTAR CONEXÃO
# =========================================================

if __name__ == "__main__":

    try:

        connection = get_connection()

        print("Conexão com o banco de dados estabelecida com sucesso!")

        connection.close()

    except mysql.connector.Error as err:

        print(f"Erro ao conectar ao banco de dados: {err}")

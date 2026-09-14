import os
import mysql.connector
from dotenv import load_dotenv
from database.constant import host, database, user, password, port
load_dotenv()
def get_connection():

        return mysql.connector.connect(
            host=os.getenv("DB_HOST", host),
            user=os.getenv("DB_USER", user),
            password=os.getenv("DB_PASSWORD", password),
            database=os.getenv("DB_NAME", database),
            port=int(os.getenv("DB_PORT", port)),
        )

if __name__ == "__main__":
    # Testar a conexão com o banco de dados
    try:
        connection = get_connection()
        cursor = connection.cursor()
        print("Conexão com o banco de dados estabelecida com sucesso!")
        connection.close()
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
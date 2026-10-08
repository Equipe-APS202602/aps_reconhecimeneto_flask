
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "facial", "dataset")
MODEL_PATH = os.path.join(BASE_DIR, "facial", "models", "trainer.yml")
 
config_path = os.path.join(BASE_DIR, "database", "config.json")
with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
    host = config["-host-"]
    database = config["-db-"]
    user = config["-user-"]
    password = config["-senha-"]
    port = config["-porta-"]
    secret_key = config["-secret_key-"]

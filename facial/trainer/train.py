# facial/trainer/train.py

import cv2
import os
import numpy as np

# =========================================================
# CAMINHOS
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATASET_DIR = os.path.join(BASE_DIR, "facial", "dataset")

MODEL_DIR = os.path.join(BASE_DIR, "facial", "models")

MODEL_PATH = os.path.join(MODEL_DIR, "trainer.yml")
""

# =========================================================
# CLASSIFICADOR DE ROSTO
# =========================================================

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# =========================================================
# RECONHECEDOR
# =========================================================

if not hasattr(cv2, "face"):

    raise Exception("OpenCV contrib não instalado. " "Instale opencv-contrib-python.")


recognizer = cv2.face.LBPHFaceRecognizer_create()


faces = []
ids = []


# =========================================================
# LER DATASET
# =========================================================

if not os.path.exists(DATASET_DIR):

    raise Exception("Pasta dataset não encontrada.")


for pasta in os.listdir(DATASET_DIR):

    caminho_pasta = os.path.join(DATASET_DIR, pasta)

    if not os.path.isdir(caminho_pasta):
        continue

    try:

        usuario_id = int(pasta)

    except ValueError:

        continue

    for arquivo in os.listdir(caminho_pasta):

        caminho_imagem = os.path.join(caminho_pasta, arquivo)

        imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)

        if imagem is None:
            continue

        rostos = detector.detectMultiScale(imagem, scaleFactor=1.2, minNeighbors=5)

        for x, y, w, h in rostos:

            faces.append(imagem[y : y + h, x : x + w])

            ids.append(usuario_id)


# =========================================================
# VERIFICAR DATASET
# =========================================================

if len(faces) == 0:

    raise Exception("Nenhum rosto encontrado no dataset.")


# =========================================================
# TREINAR
# =========================================================

print(f"Treinando com {len(faces)} imagens...")

recognizer.train(faces, np.array(ids))


# =========================================================
# CRIAR PASTA DO MODELO
# =========================================================

os.makedirs(MODEL_DIR, exist_ok=True)


# =========================================================
# SALVAR MODELO
# =========================================================

recognizer.write(MODEL_PATH)


print()
print("===================================")
print("TREINAMENTO CONCLUÍDO")
print("===================================")
print(f"Modelo salvo em:\n{MODEL_PATH}")

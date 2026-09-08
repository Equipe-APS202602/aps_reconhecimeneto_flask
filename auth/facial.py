# auth/facial.py

import base64
import os

import cv2
import numpy as np

# =========================================================
# CAMINHOS
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "facial", "models", "trainer.yml")

# Localiza o classificador Haar Cascade
if hasattr(cv2, "data"):
    CASCADE_PATH = os.path.join(
        cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
    )
else:
    CV2_DIR = os.path.dirname(getattr(cv2, "__file__", ""))

    CASCADE_PATH = os.path.join(CV2_DIR, "data", "haarcascade_frontalface_default.xml")


# =========================================================
# CARREGAR CLASSIFICADOR
# =========================================================

face_detector = cv2.CascadeClassifier(CASCADE_PATH)


# =========================================================
# CARREGAR MODELO LBPH
# =========================================================

recognizer = None

if hasattr(cv2, "face") and os.path.exists(MODEL_PATH):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)


# =========================================================
# CONVERTER BASE64 PARA IMAGEM
# =========================================================


def base64_para_imagem(imagem_base64):
    try:
        # Remove o cabeçalho:
        # data:image/jpeg;base64,...
        if "," in imagem_base64:
            imagem_base64 = imagem_base64.split(",", 1)[1]

        imagem_bytes = base64.b64decode(imagem_base64)

        np_array = np.frombuffer(imagem_bytes, np.uint8)

        imagem = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        return imagem

    except Exception as erro:
        print("Erro ao converter imagem:", erro)
        return None


# =========================================================
# RECONHECER ROSTO
# =========================================================


def reconhecer_rosto(imagem_base64):
    if recognizer is None:
        return {
            "sucesso": False,
            "mensagem": "Modelo facial não encontrado.",
            "usuario_id": None,
            "confianca": None,
        }

    if face_detector.empty():
        return {
            "sucesso": False,
            "mensagem": ("Classificador facial não encontrado: " f"{CASCADE_PATH}"),
            "usuario_id": None,
            "confianca": None,
        }

    imagem = base64_para_imagem(imagem_base64)

    if imagem is None:
        return {
            "sucesso": False,
            "mensagem": "Imagem inválida.",
            "usuario_id": None,
            "confianca": None,
        }

    # Converte para escala de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Detecta rostos
    rostos = face_detector.detectMultiScale(
        cinza, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80)
    )

    if len(rostos) == 0:
        return {
            "sucesso": False,
            "mensagem": "Nenhum rosto detectado.",
            "usuario_id": None,
            "confianca": None,
        }

    # Se houver vários rostos, utiliza o maior
    rosto = max(rostos, key=lambda r: r[2] * r[3])

    x, y, largura, altura = rosto

    rosto_cinza = cinza[y : y + altura, x : x + largura]

    if rosto_cinza.size == 0:
        return {
            "sucesso": False,
            "mensagem": "Não foi possível recortar o rosto.",
            "usuario_id": None,
            "confianca": None,
        }

    # Deve ser o mesmo tamanho usado no treinamento
    rosto_cinza = cv2.resize(rosto_cinza, (200, 200))

    # Predição
    usuario_id, distancia = recognizer.predict(rosto_cinza)

    print(f"Usuário previsto: {usuario_id} | " f"Distância: {distancia:.2f}")

    # Quanto menor a distância, melhor o reconhecimento
    if distancia > 80:
        return {
            "sucesso": False,
            "mensagem": ("Rosto não reconhecido. " f"Distância: {distancia:.2f}"),
            "usuario_id": None,
            "confianca": float(distancia),
        }

    return {
        "sucesso": True,
        "mensagem": "Rosto reconhecido.",
        "usuario_id": int(usuario_id),
        "confianca": float(distancia),
    }

# facial/capture.py

import cv2
import os
import time

# =========================================================
# CONFIGURAÇÕES
# =========================================================

NUMERO_IMAGENS = 30

LARGURA_ROSTO = 200
ALTURA_ROSTO = 200


# =========================================================
# DEFINIR CAMINHO DO PROJETO
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATASET_DIR = os.path.join(BASE_DIR, "facial", "dataset")


# =========================================================
# CLASSIFICADOR DE ROSTO
# =========================================================

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


face_detector = cv2.CascadeClassifier(CASCADE_PATH)


# Verificar se o classificador foi carregado

if face_detector.empty():

    raise Exception("Não foi possível carregar o Haar Cascade.")


# =========================================================
# SOLICITAR ID DO USUÁRIO
# =========================================================

while True:

    face_id = input("Digite o ID facial do usuário: ").strip()

    if face_id.isdigit():

        face_id = int(face_id)

        if face_id > 0:
            break

    print("Digite um ID numérico maior que zero.")


# =========================================================
# CRIAR PASTA DO USUÁRIO
# =========================================================

pasta_usuario = os.path.join(DATASET_DIR, str(face_id))


os.makedirs(pasta_usuario, exist_ok=True)


# =========================================================
# CONTAR IMAGENS EXISTENTES
# =========================================================

imagens_existentes = []

for arquivo in os.listdir(pasta_usuario):

    caminho = os.path.join(pasta_usuario, arquivo)

    if os.path.isfile(caminho):

        extensao = os.path.splitext(arquivo)[1].lower()

        if extensao in [".jpg", ".jpeg", ".png"]:

            imagens_existentes.append(arquivo)


contador = len(imagens_existentes)


print()
print("======================================")
print("     CADASTRO FACIAL")
print("======================================")
print(f"ID facial: {face_id}")
print(f"Imagens já existentes: {contador}")
print(f"Meta: {NUMERO_IMAGENS} imagens")
print()
print("Posicione seu rosto diante da câmera.")
print("Pressione Q para cancelar.")
print("======================================")


# =========================================================
# ABRIR CÂMERA
# =========================================================

camera = cv2.VideoCapture(0)


if not camera.isOpened():

    raise Exception("Não foi possível acessar a câmera.")


# =========================================================
# CAPTURA DAS IMAGENS
# =========================================================

ultima_captura = 0

intervalo = 0.25


try:

    while contador < NUMERO_IMAGENS:

        sucesso, frame = camera.read()

        if not sucesso:

            print("Erro ao capturar imagem da câmera.")

            break

        # =============================================
        # CONVERTER PARA CINZA
        # =============================================

        cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # =============================================
        # DETECTAR ROSTOS
        # =============================================

        rostos = face_detector.detectMultiScale(
            cinza, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80)
        )

        # =============================================
        # SE ENCONTRAR UM ROSTO
        # =============================================

        if len(rostos) > 0:

            # Selecionar o maior rosto
            x, y, w, h = max(rostos, key=lambda rosto: rosto[2] * rosto[3])

            # =========================================
            # DESENHAR RETÂNGULO
            # =========================================

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

            agora = time.time()

            # =========================================
            # CONTROLAR INTERVALO DAS FOTOS
            # =========================================

            if agora - ultima_captura >= intervalo:

                rosto = cinza[y : y + h, x : x + w]

                # =====================================
                # REDIMENSIONAR
                # =====================================

                rosto = cv2.resize(rosto, (LARGURA_ROSTO, ALTURA_ROSTO))

                contador += 1

                nome_arquivo = f"usuario.{face_id}." f"{contador}.jpg"

                caminho_arquivo = os.path.join(pasta_usuario, nome_arquivo)

                # =====================================
                # SALVAR
                # =====================================

                cv2.imwrite(caminho_arquivo, rosto)

                ultima_captura = agora

                print(f"Imagem {contador}/" f"{NUMERO_IMAGENS} salva.")

        # =============================================
        # INFORMAÇÕES NA TELA
        # =============================================

        texto = f"Capturas: " f"{contador}/{NUMERO_IMAGENS}"

        cv2.putText(
            frame, texto, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2
        )

        cv2.putText(
            frame,
            "Q = sair",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        # =============================================
        # MOSTRAR CÂMERA
        # =============================================

        cv2.imshow("Cadastro Facial", frame)

        # =============================================
        # TECLA Q
        # =============================================

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("q"):

            print("Captura cancelada.")

            break


finally:

    # =============================================
    # ENCERRAR CÂMERA
    # =============================================

    camera.release()

    cv2.destroyAllWindows()


# =========================================================
# RESULTADO
# =========================================================

print()
print("======================================")

if contador >= NUMERO_IMAGENS:

    print("CAPTURA CONCLUÍDA COM SUCESSO!")

    print(f"Foram capturadas {contador} imagens.")

else:

    print("CAPTURA ENCERRADA.")

    print(f"Foram capturadas {contador} imagens.")


print(f"Local: {pasta_usuario}")

print("======================================")

import cv2
import os
import time

from facial.trainer.train import treinar_modelo

# CONFIGURAÇÕES
# =========================================================

NUMERO_IMAGENS = 30
LARGURA_ROSTO = 200
ALTURA_ROSTO = 200


# =========================================================
# CLASSIFICADOR DE ROSTO
# =========================================================

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

face_detector = cv2.CascadeClassifier(CASCADE_PATH)

if face_detector.empty():
    raise Exception("Não foi possível carregar o Haar Cascade.")


# =========================================================
# FUNÇÃO DE CAPTURA FACIAL
# =========================================================


def capturar_rosto(face_id):

    # Validar ID
    if not isinstance(face_id, int) or face_id <= 0:
        raise ValueError("O ID facial deve ser um número inteiro maior que zero.")

    # =====================================================
    # CAMINHO DO DATASET
    # =====================================================

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DATASET_DIR = os.path.join(BASE_DIR, "facial", "dataset")

    pasta_usuario = os.path.join(DATASET_DIR, str(face_id))

    os.makedirs(pasta_usuario, exist_ok=True)

    # =====================================================
    # CONTAR IMAGENS EXISTENTES
    # =====================================================

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
    print("       CADASTRO FACIAL")
    print("======================================")
    print(f"ID facial: {face_id}")
    print(f"Imagens já existentes: {contador}")
    print(f"Meta: {NUMERO_IMAGENS} imagens")
    print()
    print("Posicione seu rosto diante da câmera.")
    print("Pressione Q para cancelar.")
    print("======================================")

    # =====================================================
    # ABRIR CÂMERA
    # =====================================================

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise Exception("Não foi possível acessar a câmera.")

    ultima_captura = 0
    intervalo = 1.0

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

                # Desenhar retângulo
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

                agora = time.time()

                # =========================================
                # CONTROLAR INTERVALO
                # =========================================

                if agora - ultima_captura >= intervalo:

                    rosto = cinza[y : y + h, x : x + w]

                    # Redimensionar
                    rosto = cv2.resize(rosto, (LARGURA_ROSTO, ALTURA_ROSTO))

                    contador += 1

                    nome_arquivo = f"usuario.{face_id}.{contador}.jpg"

                    caminho_arquivo = os.path.join(pasta_usuario, nome_arquivo)

                    # Salvar imagem
                    cv2.imwrite(caminho_arquivo, rosto)

                    ultima_captura = agora

                    print(f"Imagem {contador}/" f"{NUMERO_IMAGENS} salva.")

            # =============================================
            # INFORMAÇÕES NA TELA
            # =============================================

            texto = f"Capturas: " f"{contador}/{NUMERO_IMAGENS}"

            cv2.putText(
                frame,
                texto,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
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

            # Mostrar câmera
            cv2.imshow("Cadastro Facial", frame)

            # Tecla Q
            tecla = cv2.waitKey(1) & 0xFF

            if tecla == ord("q"):
                print("Captura cancelada.")
                break

    finally:

        camera.release()
        cv2.destroyAllWindows()

    # =====================================================
    # RESULTADO
    # =====================================================

    print()
    print("======================================")

    if contador >= NUMERO_IMAGENS:

        print("CAPTURA CONCLUÍDA COM SUCESSO!")
        print(f"Foram capturadas {contador} imagens.")

    # =============================================
    # TREINAMENTO AUTOMÁTICO
    # =============================================

    print()
    print("Iniciando treinamento automático...")

    try:

        treinar_modelo()

        print("Modelo atualizado com sucesso.")

        sucesso = True

    except Exception as erro:

        print(
            f"Erro durante o treinamento: {erro}"
        )

        sucesso = False
        
if __name__ == "__main__":
    face_id = input("Digite o ID facial (número inteiro maior que zero): ")

    try:
        face_id = int(face_id)
        capturar_rosto(face_id)
    except ValueError:
        print("ID inválido. Certifique-se de digitar um número inteiro maior que zero.")
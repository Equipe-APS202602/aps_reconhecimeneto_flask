import cv2
import os

# ==========================================
# CAMINHOS
# ==========================================

# Pasta principal do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho do modelo treinado
MODEL_PATH = "C:\\Users\\arian\\ESTUDO PESQUISA OPERACIONAL\\facial\\models\\trainer.yml"

print("📁 Pasta do projeto:", BASE_DIR)
print("🤖 Procurando modelo em:", MODEL_PATH)


# ==========================================
# VERIFICAR MODELO
# ==========================================

if not os.path.exists(MODEL_PATH):
    print("\n❌ Modelo não encontrado!")
    print("Verifique se o arquivo trainer.yml existe em:")
    print(MODEL_PATH)
    exit()


print("✅ Modelo encontrado!")


# ==========================================
# CARREGAR RECONHECEDOR
# ==========================================

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read(MODEL_PATH)


# ==========================================
# CLASSIFICADOR DE ROSTO
# ==========================================

cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

face_cascade = cv2.CascadeClassifier(cascade_path)


# ==========================================
# ABRIR WEBCAM
# ==========================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Não foi possível acessar a câmera.")
    exit()


print("\n✅ Reconhecimento facial iniciado!")
print("Pressione ESC para sair.")


# ==========================================
# RECONHECIMENTO
# ==========================================

while True:

    ret, frame = camera.read()

    if not ret:
        print("❌ Erro ao capturar imagem.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100)
    )

    for x, y, w, h in faces:

        rosto = gray[y : y + h, x : x + w]

        label, confidence = recognizer.predict(rosto)

        # Quanto MENOR o valor, melhor a correspondência
        if confidence < 70:

            nome = "Ariane"

        else:

            nome = "Desconhecido"

        texto = f"{nome} | {confidence:.1f}"

        # Quadrado no rosto
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Texto
        cv2.putText(
            frame, texto, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
        )

    # Mostrar câmera
    cv2.imshow("Reconhecimento Facial", frame)

    # ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break


# ==========================================
# ENCERRAR
# ==========================================

camera.release()
cv2.destroyAllWindows()

print("\n🔴 Reconhecimento encerrado.")

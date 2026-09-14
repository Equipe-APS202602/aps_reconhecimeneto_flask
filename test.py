# import cv2

# # Se não houver erros na linha abaixo, o problema foi resolvido!
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# print("Módulo 'face' importado com sucesso!")

from werkzeug.security import generate_password_hash, check_password_hash
senha = "SuperPoderesa"
senha_hash = generate_password_hash(senha)
print(senha_hash)
senha_verificada = check_password_hash(senha_hash, senha)
print(senha_verificada)  # Deve imprimir True se a senha estiver correta
senha_antiga ="scrypt:32768:8:1$MG2d16gGYoWtKHHT$bc24745e8f3731c94a8fd19b377b19a1a54afd5e146b8779d1fd79e07863600d7e0786b00a407b83174da2e8c1b3936927889a85282a67d70fa71f9d7a7cc65c"
senha_verificada_antiga = check_password_hash(senha_antiga, "SuperPoderesa")
print(senha_verificada_antiga)  # Deve imprimir True se a senha estiver correta
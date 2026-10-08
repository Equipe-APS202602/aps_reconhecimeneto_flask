# facial/trainer/train.py

import os
from collections import defaultdict
from uuid import uuid4

import cv2
import numpy as np

# =========================================================
# CONFIGURAÇÕES
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATASET_DIR = os.path.join(
    BASE_DIR,
    "facial",
    "dataset",
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "facial",
    "models",
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "trainer.yml",
)

TAMANHO_ROSTO = (200, 200)

EXTENSOES_PERMITIDAS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}

MINIMO_RECOMENDADO = 30


# =========================================================
# PREPARAÇÃO DAS IMAGENS
# =========================================================


def preparar_rosto(rosto_cinza):
    """
    Mesma preparação utilizada no auth/facial.py.

    As imagens do dataset devem ser rostos já recortados
    pelo capture.py, sem CLAHE aplicado anteriormente.
    """
    if rosto_cinza is None or rosto_cinza.size == 0:
        raise ValueError("Recorte facial vazio.")

    rosto_cinza = cv2.resize(
        rosto_cinza,
        TAMANHO_ROSTO,
        interpolation=cv2.INTER_AREA,
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )

    return clahe.apply(rosto_cinza)


def ordenar_pastas(nome):
    """Ordena as pastas numéricas por ID."""
    try:
        return 0, int(nome)
    except ValueError:
        return 1, nome.lower()


def ler_imagem(caminho):
    """
    Lê a imagem em cinza.

    Usa fromfile + imdecode para aceitar caminhos
    com acentos no Windows.
    """
    dados = np.fromfile(
        caminho,
        dtype=np.uint8,
    )

    if dados.size == 0:
        return None

    return cv2.imdecode(
        dados,
        cv2.IMREAD_GRAYSCALE,
    )


# =========================================================
# CARREGAR DATASET
# =========================================================


def carregar_dataset():
    faces = []
    ids = []

    imagens_por_usuario = defaultdict(int)
    imagens_ignoradas = []
    pastas_ignoradas = []
    usuarios_sem_imagens = []
    ids_pastas = set()

    pastas = sorted(
        os.listdir(DATASET_DIR),
        key=ordenar_pastas,
    )

    print("======================================")
    print("LEITURA DO DATASET")
    print("======================================")
    print(f"Dataset: {DATASET_DIR}\n")

    for pasta in pastas:
        caminho_pasta = os.path.join(
            DATASET_DIR,
            pasta,
        )

        if not os.path.isdir(caminho_pasta):
            continue

        # A pasta deve representar usuarios.id no banco.
        if not pasta.isascii() or not pasta.isdigit():
            pastas_ignoradas.append(pasta)
            print(f"[AVISO] Pasta ignorada: {pasta!r}. " "Use um ID numérico positivo.")
            continue

        usuario_id = int(pasta)

        if not 1 <= usuario_id <= np.iinfo(np.int32).max:
            pastas_ignoradas.append(pasta)
            print(
                f"[AVISO] Pasta ignorada: {pasta!r}. " "ID fora do intervalo permitido."
            )
            continue

        # Impede pastas como "1" e "01" para o mesmo ID.
        if usuario_id in ids_pastas:
            raise RuntimeError(
                f"Existem duas pastas para o ID {usuario_id}. "
                "Organize as imagens em uma única pasta."
            )

        ids_pastas.add(usuario_id)

        print(f"Lendo usuário ID {usuario_id}...")

        for arquivo in sorted(os.listdir(caminho_pasta)):
            caminho_imagem = os.path.join(
                caminho_pasta,
                arquivo,
            )

            if not os.path.isfile(caminho_imagem):
                continue

            extensao = os.path.splitext(arquivo)[1].lower()

            if extensao not in EXTENSOES_PERMITIDAS:
                continue

            try:
                imagem = ler_imagem(caminho_imagem)

                if imagem is None:
                    raise ValueError("Imagem vazia ou formato inválido.")

                # O capture.py já recortou o rosto.
                # Não fazemos uma segunda detecção facial.
                rosto = preparar_rosto(imagem)

            except (OSError, ValueError, cv2.error) as erro:
                imagens_ignoradas.append(caminho_imagem)

                print(f"  [IGNORADA] {arquivo}: {erro}")
                continue

            faces.append(rosto)
            ids.append(usuario_id)

            # Amostra adicional por espelhamento.
            faces.append(cv2.flip(rosto, 1))
            ids.append(usuario_id)

            imagens_por_usuario[usuario_id] += 1

        quantidade = imagens_por_usuario[usuario_id]

        print(
            f"  {quantidade} imagens válidas; "
            f"{quantidade * 2} amostras de treinamento."
        )

        if quantidade == 0:
            usuarios_sem_imagens.append(usuario_id)

    if not faces:
        raise RuntimeError(
            "Nenhuma imagem válida foi encontrada. "
            "O modelo anterior não será substituído."
        )

    # Evita salvar silenciosamente um modelo que deixou
    # de incluir uma pasta de usuário existente.
    if usuarios_sem_imagens:
        raise RuntimeError(
            "Usuários sem imagens válidas: "
            f"{usuarios_sem_imagens}. "
            "Corrija essas pastas antes de treinar. "
            "O modelo anterior não será substituído."
        )

    return (
        faces,
        np.asarray(ids, dtype=np.int32),
        imagens_por_usuario,
        imagens_ignoradas,
        pastas_ignoradas,
    )


# =========================================================
# SALVAR MODELO
# =========================================================


def salvar_modelo(modelo):
    """
    Grava e verifica um arquivo temporário antes de
    substituir trainer.yml.
    """
    os.makedirs(
        MODEL_DIR,
        exist_ok=True,
    )

    caminho_temporario = os.path.join(
        MODEL_DIR,
        f"trainer.{uuid4().hex}.tmp.yml",
    )

    try:
        modelo.write(caminho_temporario)

        if (
            not os.path.isfile(caminho_temporario)
            or os.path.getsize(caminho_temporario) == 0
        ):
            raise RuntimeError("O arquivo do modelo não foi gravado corretamente.")

        # Confirma que o arquivo salvo pode ser carregado.
        verificacao = cv2.face.LBPHFaceRecognizer_create()
        verificacao.read(caminho_temporario)

        if verificacao.empty():
            raise RuntimeError("O modelo salvo está vazio.")

        labels_esperados = np.asarray(modelo.getLabels()).reshape(-1)

        labels_salvos = np.asarray(verificacao.getLabels()).reshape(-1)

        if not np.array_equal(
            labels_esperados,
            labels_salvos,
        ):
            raise RuntimeError(
                "Os IDs do modelo salvo não correspondem " "aos IDs do treinamento."
            )

        # Substitui o arquivo somente após a verificação.
        os.replace(
            caminho_temporario,
            MODEL_PATH,
        )

    finally:
        if os.path.exists(caminho_temporario):
            os.remove(caminho_temporario)


# =========================================================
# TREINAMENTO
# =========================================================


def main():
    if not hasattr(cv2, "face"):
        raise RuntimeError(
            "O módulo cv2.face não foi encontrado.\n"
            "Instale no mesmo ambiente do projeto:\n"
            "python -m pip install opencv-contrib-python"
        )

    if not os.path.isdir(DATASET_DIR):
        raise FileNotFoundError(f"Pasta do dataset não encontrada:\n{DATASET_DIR}")

    (
        faces,
        ids,
        imagens_por_usuario,
        imagens_ignoradas,
        pastas_ignoradas,
    ) = carregar_dataset()

    usuarios = sorted(int(usuario_id) for usuario_id in np.unique(ids))

    if len(usuarios) == 1:
        print(
            "\n[AVISO] Apenas um usuário no treinamento. "
            "Teste também pessoas não cadastradas para "
            "avaliar a rejeição no reconhecimento."
        )

    for usuario_id in usuarios:
        quantidade = imagens_por_usuario[usuario_id]

        if quantidade < MINIMO_RECOMENDADO:
            print(
                f"[AVISO] Usuário {usuario_id}: "
                f"{quantidade} imagens válidas. "
                f"Recomendação inicial: "
                f"{MINIMO_RECOMENDADO} imagens variadas."
            )

    print("\n======================================")
    print("TREINAMENTO")
    print("======================================")
    print(f"IDs: {usuarios}")
    print(f"Total de usuários: {len(usuarios)}")
    print("Imagens originais válidas: " f"{sum(imagens_por_usuario.values())}")
    print(f"Amostras com espelhamento: {len(faces)}")

    modelo = cv2.face.LBPHFaceRecognizer_create(
        radius=1,
        neighbors=8,
        grid_x=8,
        grid_y=8,
    )

    # Treinamento completo com o dataset atual.
    # Não acumula amostras do trainer.yml anterior.
    modelo.train(
        faces,
        ids,
    )

    salvar_modelo(modelo)

    print("\n======================================")
    print("TREINAMENTO CONCLUÍDO")
    print("======================================")

    for usuario_id in usuarios:
        print(
            f"Usuário {usuario_id}: "
            f"{imagens_por_usuario[usuario_id]} "
            "imagens válidas"
        )

    print(f"\nImagens ignoradas: {len(imagens_ignoradas)}")
    print(f"Pastas ignoradas: {len(pastas_ignoradas)}")
    print(f"Modelo salvo em:\n{MODEL_PATH}")


def treinar_modelo():
    """
    Executa o treinamento do modelo facial.

    Retorna True quando o treinamento é concluído
    com sucesso.
    """

    if not hasattr(cv2, "face"):
        raise RuntimeError(
            "O módulo cv2.face não foi encontrado. " "Instale opencv-contrib-python."
        )

    if not os.path.isdir(DATASET_DIR):
        raise FileNotFoundError(f"Pasta do dataset não encontrada:\n{DATASET_DIR}")

    (
        faces,
        ids,
        imagens_por_usuario,
        imagens_ignoradas,
        pastas_ignoradas,
    ) = carregar_dataset()

    usuarios = sorted(int(usuario_id) for usuario_id in np.unique(ids))

    print("\n======================================")
    print("TREINAMENTO AUTOMÁTICO")
    print("======================================")
    print(f"IDs: {usuarios}")
    print(f"Total de usuários: {len(usuarios)}")
    print("Imagens originais válidas: " f"{sum(imagens_por_usuario.values())}")
    print(f"Amostras com espelhamento: {len(faces)}")

    modelo = cv2.face.LBPHFaceRecognizer_create(
        radius=1,
        neighbors=8,
        grid_x=8,
        grid_y=8,
    )

    modelo.train(faces, ids)

    salvar_modelo(modelo)

    print("\n======================================")
    print("TREINAMENTO CONCLUÍDO")
    print("======================================")

    print(f"Modelo salvo em:")
    print(MODEL_PATH)

    return True


def main():
    treinar_modelo()


if __name__ == "__main__":
    try:
        main()
    except (
        OSError,
        RuntimeError,
        ValueError,
        cv2.error,
    ) as erro:
        print(f"\n[ERRO] Treinamento não concluído:\n{erro}")
        raise SystemExit(1)

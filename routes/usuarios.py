# routes/usuarios.py
from flask import current_app
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)

from auth.permissions import permission_required, login_required

from database.connection import get_connection
import bcrypt

import base64

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.route("/perfil/foto", methods=["POST"])
@login_required
def atualizar_foto():

    usuario_id = session.get("usuario_id")
    arquivo = request.files.get("foto")

    if not arquivo or not arquivo.filename:
        flash("Selecione uma imagem.", "warning")
        return redirect(url_for("usuarios.perfil"))

    extensoes_permitidas = {".jpg", ".jpeg", ".png", ".webp"}
    extensao = os.path.splitext(arquivo.filename)[1].lower()

    if extensao not in extensoes_permitidas:
        flash("Envie uma imagem JPG, PNG ou WEBP.", "warning")
        return redirect(url_for("usuarios.perfil"))

    # Limita o tamanho do arquivo a 3 MB.
    arquivo.stream.seek(0, os.SEEK_END)
    tamanho = arquivo.stream.tell()
    arquivo.stream.seek(0)

    if tamanho > 3 * 1024 * 1024:
        flash("A imagem deve ter no máximo 3 MB.", "warning")
        return redirect(url_for("usuarios.perfil"))

    # Gera um nome único para evitar colisões e nomes perigosos.
    nome_arquivo = f"{usuario_id}_{uuid4().hex}{extensao}"

    pasta = os.path.join(current_app.root_path, "static", "uploads", "fotos_perfil")
    os.makedirs(pasta, exist_ok=True)

    caminho = os.path.join(pasta, nome_arquivo)
    caminho_relativo = f"uploads/fotos_perfil/{nome_arquivo}"

    conexao = get_connection()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT foto_perfil FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()

        if not usuario:
            flash("Usuário não encontrado.", "danger")
            return redirect(url_for("usuarios.perfil"))

        arquivo.save(caminho)

        cursor.execute(
            """
            UPDATE usuarios
            SET foto_perfil = %s
            WHERE id = %s
        """,
            (caminho_relativo, usuario_id),
        )

        conexao.commit()

        # Remove a foto anterior somente após o commit.
        foto_antiga = usuario.get("foto_perfil")
        if foto_antiga:
            caminho_antigo = os.path.abspath(
                os.path.join(current_app.root_path, "static", foto_antiga)
            )
            pasta_fotos = os.path.abspath(pasta)

            if os.path.dirname(caminho_antigo) == pasta_fotos and os.path.isfile(
                caminho_antigo
            ):
                try:
                    os.remove(caminho_antigo)
                except OSError:
                    current_app.logger.warning(
                        "Não foi possível remover a foto antiga."
                    )

        flash("Foto de perfil atualizada com sucesso.", "success")

    except Exception:
        conexao.rollback()

        if os.path.isfile(caminho):
            try:
                os.remove(caminho)
            except OSError:
                pass

        current_app.logger.exception("Erro ao atualizar foto de perfil.")
        flash("Não foi possível atualizar a foto.", "danger")

    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for("usuarios.perfil"))


# =========================================================
# LISTAR USUÁRIOS
# =========================================================


@usuarios_bp.route("/")
@permission_required("GERENCIAR_USUARIOS")
def index():

    conexao = get_connection()
    cursor = conexao.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                u.id,
                u.nome,
                u.email,
                u.cargo,
                u.face_id,
                u.ativo,
                cadastrador.nome AS nome_cadastrador
            FROM usuarios u
            LEFT JOIN usuarios cadastrador
                ON u.cadastrado_por = cadastrador.id
            ORDER BY u.nome
        """)

        usuarios = cursor.fetchall()

        return render_template("usuarios/index.html", usuarios=usuarios)

    finally:
        cursor.close()
        conexao.close()


# # =========================================================
# CRIAR USUÁRIO
# =========================================================


@usuarios_bp.route("/criar", methods=["GET", "POST"])
@permission_required("GERENCIAR_USUARIOS")
def criar():

    # Usuário autenticado que está realizando o cadastro
    usuario_logado_id = session.get("usuario_id")
    cargo_usuario = session.get("usuario_cargo", "").upper()

    # Define quais cargos podem ser cadastrados
    if cargo_usuario == "MINISTRO":
        cargos_disponiveis = ["DIRETOR", "FUNCIONARIO"]
    elif cargo_usuario == "DIRETOR":
        cargos_disponiveis = ["FUNCIONARIO"]
    else:
        cargos_disponiveis = []

    # GET: abre a tela de cadastro
    if request.method == "GET":
        return render_template(
            "usuarios/criar.html", cargos_disponiveis=cargos_disponiveis
        )

    # POST: recebe os dados do formulário
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    cargo = request.form.get("cargo", "").upper()
    senha = request.form.get("senha", "")

    # Validação dos campos
    if not nome or not email or not cargo or not senha:
        flash("Preencha todos os campos obrigatórios.", "warning")
        return redirect(url_for("usuarios.criar"))

    # Validação de permissão
    if cargo not in cargos_disponiveis:
        flash("Você não tem permissão para cadastrar este cargo.", "danger")
        return redirect(url_for("usuarios.criar"))

    if not usuario_logado_id:
        flash("Sessão inválida. Faça login novamente.", "warning")
        return redirect(url_for("login.index"))

    # Gera o hash da senha
    senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    conexao = get_connection()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO usuarios (
                nome,
                email,
                cargo,
                senha_hash,
                cadastrado_por
            )
            VALUES (%s, %s, %s, %s, %s)
        """,
            (nome, email, cargo, senha_hash, usuario_logado_id),
        )

        # ID gerado pelo MySQL
        usuario_id = cursor.lastrowid

        # O face_id será o mesmo ID do usuário
        cursor.execute(
            """
            UPDATE usuarios
            SET face_id = %s
            WHERE id = %s
        """,
            (usuario_id, usuario_id),
        )

        conexao.commit()

        flash("Usuário cadastrado. Agora realize o cadastro facial.", "success")

    except Exception as erro:
        conexao.rollback()
        flash(f"Erro ao cadastrar usuário: {erro}", "danger")
        return redirect(url_for("usuarios.criar"))

    finally:
        cursor.close()
        conexao.close()

    return redirect(url_for("usuarios.cadastrar_rosto", usuario_id=usuario_id))


# =========================================================
# CADASTRAR ROSTO
# =========================================================


@usuarios_bp.route("/<int:usuario_id>/cadastrar-rosto")
@permission_required("GERENCIAR_USUARIOS")
def cadastrar_rosto(usuario_id):

    conexao = get_connection()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT id, nome, email, cargo, face_id
            FROM usuarios
            WHERE id = %s
            """,
            (usuario_id,),
        )

        usuario = cursor.fetchone()

        if not usuario:
            flash("Usuário não encontrado.", "danger")
            return redirect(url_for("usuarios.index"))

        return render_template(
            "usuarios/cadastrar_rosto.html",
            usuario=usuario,
            usuario_id=usuario_id,
            numero_imagens=30,
        )

    finally:
        cursor.close()
        conexao.close()


@usuarios_bp.route("/<int:usuario_id>/cadastrar-rosto/foto", methods=["POST"])
@permission_required("GERENCIAR_USUARIOS")
def receber_foto_rosto(usuario_id):

    dados = request.get_json()

    if not dados or "imagem" not in dados:
        return jsonify({"sucesso": False, "mensagem": "Imagem não enviada."}), 400

    imagem_base64 = dados["imagem"]

    try:
        # Remove o prefixo:
        # data:image/jpeg;base64,...
        if "," in imagem_base64:
            imagem_base64 = imagem_base64.split(",", 1)[1]

        imagem = base64.b64decode(imagem_base64)

        # Caminho raiz do projeto
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        dataset_dir = os.path.join(BASE_DIR, "facial", "dataset", str(usuario_id))

        os.makedirs(dataset_dir, exist_ok=True)

        # Conta as imagens existentes
        imagens = [
            arquivo
            for arquivo in os.listdir(dataset_dir)
            if arquivo.lower().endswith(".jpg")
        ]

        numero = len(imagens) + 1

        caminho = os.path.join(dataset_dir, f"{numero}.jpg")

        with open(caminho, "wb") as arquivo:
            arquivo.write(imagem)

        return jsonify({"sucesso": True, "mensagem": "Imagem salva.", "numero": numero})

    except Exception as erro:

        print("ERRO AO SALVAR ROSTO:", erro)

        return jsonify({"sucesso": False, "mensagem": str(erro)}), 500


@usuarios_bp.route("/<int:usuario_id>/salvar-rosto", methods=["POST"])
@permission_required("GERENCIAR_USUARIOS")
def salvar_rosto(usuario_id):

    dados = request.get_json()

    if not dados or "imagem" not in dados:
        return (
            jsonify({"sucesso": False, "mensagem": "Nenhuma imagem foi enviada."}),
            400,
        )

    try:
        # Verifica se o usuário existe
        conexao = get_connection()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, nome, cargo FROM usuarios WHERE id = %s", (usuario_id,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        if not usuario:
            return (
                jsonify({"sucesso": False, "mensagem": "Usuário não encontrado."}),
                404,
            )

        # -----------------------------------------
        # RECEBE A IMAGEM BASE64
        # -----------------------------------------

        imagem_base64 = dados["imagem"]

        if "," in imagem_base64:
            imagem_base64 = imagem_base64.split(",", 1)[1]

        imagem = base64.b64decode(imagem_base64)

        # -----------------------------------------
        # DATASET
        # -----------------------------------------

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        pasta_usuario = os.path.join(BASE_DIR, "facial", "dataset", str(usuario_id))

        os.makedirs(pasta_usuario, exist_ok=True)

        # -----------------------------------------
        # CONTAR IMAGENS EXISTENTES
        # -----------------------------------------

        imagens = [
            arquivo
            for arquivo in os.listdir(pasta_usuario)
            if arquivo.lower().endswith(".jpg")
        ]

        numero = len(imagens) + 1

        # -----------------------------------------
        # SALVAR IMAGEM
        # -----------------------------------------

        caminho = os.path.join(pasta_usuario, f"{numero}.jpg")

        with open(caminho, "wb") as arquivo:
            arquivo.write(imagem)

        print(f"[FACIAL] Imagem {numero} salva: {caminho}")

        # -----------------------------------------
        # VERIFICAR SE TERMINOU
        # -----------------------------------------

        total = 30

        if numero >= total:

            print("[FACIAL] 30 imagens coletadas.")
            print("[FACIAL] Iniciando treinamento...")

            try:
                from facial.trainer.train import treinar_modelo

                treinar_modelo()

                print("[FACIAL] Treinamento concluído.")

                return jsonify(
                    {
                        "sucesso": True,
                        "quantidade": numero,
                        "concluido": True,
                        "mensagem": "Cadastro facial concluído e modelo treinado.",
                        "redirecionar": url_for("usuarios.index"),
                    }
                )

            except Exception as erro_treinamento:

                print("[FACIAL] ERRO NO TREINAMENTO:", erro_treinamento)

                return (
                    jsonify(
                        {
                            "sucesso": False,
                            "quantidade": numero,
                            "concluido": False,
                            "mensagem": f"As imagens foram salvas, "
                            f"mas ocorreu um erro no treinamento: "
                            f"{erro_treinamento}",
                        }
                    ),
                    500,
                )

        # -----------------------------------------
        # AINDA NÃO TERMINOU
        # -----------------------------------------

        return jsonify(
            {
                "sucesso": True,
                "quantidade": numero,
                "concluido": False,
                "mensagem": f"Imagem {numero} de {total} salva.",
            }
        )

    except Exception as erro:

        print("[FACIAL] ERRO:", erro)

        return (
            jsonify({"sucesso": False, "mensagem": f"Erro ao salvar imagem: {erro}"}),
            500,
        )


@usuarios_bp.route("/perfil")
@login_required
def perfil():

    usuario_id = session.get("usuario_id")

    conexao = get_connection()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                id,
                nome,
                email,
                cargo,
                face_id,
                ativo,
                criado_em,
                foto_perfil
            FROM usuarios
            WHERE id = %s
        """,
            (usuario_id,),
        )

        usuario = cursor.fetchone()

        if not usuario:
            flash("Usuário não encontrado.", "warning")
            return redirect(url_for("dashboard.dashboard"))

        return render_template("usuarios/perfil.html", usuario=usuario)

    finally:
        cursor.close()
        conexao.close()


# =========================================================
# DESATIVAR USUÁRIO
# =========================================================


@usuarios_bp.route("/desativar/<int:id>", methods=["POST"])
@permission_required("GERENCIAR_USUARIOS")
def desativar(id):

    conexao = get_connection()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET ativo = FALSE
        WHERE id = %s
        """,
        (id,),
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Usuário desativado.", "success")

    return redirect(url_for("usuarios.index"))


# =========================================================
# ATIVAR USUÁRIO
# =========================================================


@usuarios_bp.route("/ativar/<int:id>", methods=["POST"])
@permission_required("GERENCIAR_USUARIOS")
def ativar(id):

    conexao = get_connection()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET ativo = TRUE
        WHERE id = %s
        """,
        (id,),
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Usuário ativado.", "success")

    return redirect(url_for("usuarios.index"))

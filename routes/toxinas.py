# routes/toxinas.py

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from auth.permissions import (
    login_required,
    permission_required,
)

from database.connection import get_connection

toxinas_bp = Blueprint("toxinas", __name__, url_prefix="/registros")


# =========================================================
# LISTAR REGISTROS
# =========================================================


@toxinas_bp.route("/")
@login_required
def index():

    conexao = get_connection()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            codigo,
            nome_ficticio,
            classificacao,
            nivel_acesso,
            descricao,
            quantidade_simulada,
            criado_em
        FROM registros_cofre
        ORDER BY id DESC
        """)

    registros = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("registros/index.html", registros=registros)


# =========================================================
# CRIAR REGISTRO
# =========================================================


@toxinas_bp.route("/criar", methods=["POST"])
@permission_required("ALTERAR_REGISTRO")
def criar():

    codigo = request.form.get("codigo")

    nome = request.form.get("nome_ficticio")

    classificacao = request.form.get("classificacao")

    nivel_acesso = request.form.get("nivel_acesso")

    descricao = request.form.get("descricao")

    quantidade = request.form.get("quantidade_simulada", 0)

    if not codigo or not nome:

        flash("Código e nome são obrigatórios.", "warning")

        return redirect(url_for("toxinas.index"))

    conexao = get_connection()

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO registros_cofre
            (
                codigo,
                nome_ficticio,
                classificacao,
                nivel_acesso,
                descricao,
                quantidade_simulada
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (codigo, nome, classificacao, nivel_acesso, descricao, quantidade),
        )

        conexao.commit()

        flash("Registro criado com sucesso.", "success")

    except Exception as erro:

        conexao.rollback()

        flash(f"Erro ao criar registro: {erro}", "danger")

    finally:

        cursor.close()
        conexao.close()

    return redirect(url_for("toxinas.index"))


# =========================================================
# EXCLUIR REGISTRO
# =========================================================


@toxinas_bp.route("/excluir/<int:id>", methods=["POST"])
@permission_required("EXCLUIR_REGISTRO")
def excluir(id):

    conexao = get_connection()

    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM registros_cofre
        WHERE id = %s
        """,
        (id,),
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Registro removido.", "success")

    return redirect(url_for("toxinas.index"))

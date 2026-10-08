from flask import Blueprint, render_template, request, redirect, url_for, flash

from auth.permissions import permission_required

from database.connection import get_connection

cadrasta_bp = Blueprint("cadrasto", __name__)

@cadrasta_bp.route("/cadrasto")

def cadrasto():
    conexao = get_connection()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        insert into usuarios (nome, email, cargo, face_id, ativo) values (%s, %s, %s, %s, %s);
        """,(valor[0], valor[1], valor[2], valor[3], valor[4]))
    conexao.commit()
    cursor.execute("""
            insert into usuarios (nome, email, cargo, face_id, ativo) values (%s, %s, %s, %s, %s);
            """,(valor[0], valor[1], valor[2], valor[3], valor[4]))
    conexao.commit()

    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("cadrasto/index.html", usuarios=usuarios)
# auth/permissions.py

from functools import wraps

from flask import session, redirect, url_for, flash

# =========================================================
# PERMISSÕES DO SISTEMA
# =========================================================

PERMISSOES = {
    "FUNCIONARIO": [
        "VISUALIZAR_LIMITADO",
    ],
    "DIRETOR": [
        "VISUALIZAR_LIMITADO",
        "VISUALIZAR_COMPLETO",
        "ALTERAR_REGISTRO",
    ],
    "MINISTRO": [
        "VISUALIZAR_LIMITADO",
        "VISUALIZAR_COMPLETO",
        "ALTERAR_REGISTRO",
        "GERENCIAR_USUARIOS",
        "EXCLUIR_REGISTRO",
        "VISUALIZAR_LOGS",
    ],
}


# =========================================================
# VERIFICAR PERMISSÃO
# =========================================================


def possui_permissao(cargo, permissao):
    if not cargo or not permissao:
        return False

    cargo = cargo.upper()
    permissao = permissao.upper()

    return permissao in PERMISSOES.get(cargo, [])


# =========================================================
# USUÁRIO PRECISA ESTAR LOGADO
# =========================================================


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Você precisa realizar o login.", "warning")
            return redirect(url_for("login.login"))

        return func(*args, **kwargs)

    return wrapper


# =========================================================
# VERIFICAR UMA PERMISSÃO ESPECÍFICA
# =========================================================


def permission_required(permissao):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("usuario_id"):
                flash("Faça login para continuar.", "warning")
                return redirect(url_for("login.login"))

            cargo = session.get("usuario_cargo", "").upper()

            if not possui_permissao(cargo, permissao):
                flash(
                    "Você não possui permissão para acessar este recurso.",
                    "danger",
                )
                return redirect(url_for("dashboard.dashboard"))

            return func(*args, **kwargs)

        return wrapper

    return decorator

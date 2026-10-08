from flask import Blueprint, render_template, session

from auth.permissions import login_required

dashboard_bp = Blueprint("dashboard", __name__)


# =========================================================
# DASHBOARD PRINCIPAL
# =========================================================


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    cargo = session.get("usuario_cargo", "").upper()

    if cargo == "MINISTRO":
        return render_template("dashboard/ministro.html")

    if cargo == "DIRETOR":
        return render_template("dashboard/diretor.html")

    return render_template("dashboard/funcionario.html")

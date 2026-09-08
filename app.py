from flask import Flask

from routes.login import login_bp
from routes.dashboard import dashboard_bp
from routes.usuarios import usuarios_bp
from routes.toxinas import toxinas_bp
from routes.logs import logs_bp

app = Flask(__name__)


# =========================================================
# CONFIGURAÇÕES
# =========================================================

app.config.from_pyfile("config.py")


# =========================================================
# REGISTRAR BLUEPRINTS
# =========================================================

app.register_blueprint(login_bp)

app.register_blueprint(dashboard_bp)

app.register_blueprint(usuarios_bp)

app.register_blueprint(toxinas_bp)

app.register_blueprint(logs_bp)


# =========================================================
# EXECUTAR
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)

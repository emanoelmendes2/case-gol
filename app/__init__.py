from flask import Flask, render_template, redirect, url_for
from .models import db, Usuario
from .routes import auth_bp, dashboard_bp
from flask_migrate import Migrate
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Inicializa o banco de dados
    db.init_app(app)

    # Inicializa a migração
    migrate = Migrate(app, db)

    # Inicializa o gerenciador de login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Registra as rotas
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app
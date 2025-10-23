# Criação da aplicação Flask e registro das rotas

from flask import Flask
from api_mapa.routes.mapa_routes import mapa_bp

def create_app():
    app = Flask(__name__)

    # Registro do blueprint das rotas de mapa
    app.register_blueprint(mapa_bp, url_prefix="/mapa")

    return app

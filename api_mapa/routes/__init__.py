from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from api_mapa.routes.mapa_routes import mapa_bp

    app.register_blueprint(mapa_bp, url_prefix="/mapa")


    return app

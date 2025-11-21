from flask import Blueprint, make_response
from api_mapa.services.map_service import generate_map_html

mapa_bp = Blueprint("mapa", __name__)


@mapa_bp.route("/", methods=["GET"])
def exibir_mapa():
    mapa_html = generate_map_html()
    response = make_response(mapa_html)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response

from flask import Blueprint, jsonify
from api_mapa.services.pindorama_service import get_artigos, get_eventos
from api_mapa.utils.map_generator import gerar_mapa

mapa_bp = Blueprint("mapa", __name__)

@mapa_bp.route("/", methods=["GET"])
def listar_patrimonios():
    #Retorna o HTML do mapa com artigos e eventos do backend Pindorama.
    artigos = get_artigos()
    eventos = get_eventos()

    if "erro" in artigos or "erro" in eventos:
        return jsonify({"erro": "Falha ao obter dados do backend."}), 500

    mapa_html = gerar_mapa(artigos, eventos)
    return jsonify({"mapa_html": mapa_html})

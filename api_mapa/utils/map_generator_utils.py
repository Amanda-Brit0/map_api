import json
from pathlib import Path
import os

VIEW_DIR = Path(__file__).parent
PROJECT_ROOT = VIEW_DIR.parent.parent
DATA_EXTERNAL_DIR = PROJECT_ROOT / "api_mapa" / "data_external"


def load_geojson(filename: str = "brasil_geo.geojson") -> dict:
    """Carrega dados GeoJSON de um arquivo."""
    file_path = DATA_EXTERNAL_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"GeoJSON não encontrado: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def darken_color(hex_color, factor=0.7):
    """Escurece uma cor HEX por um fator."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def gerar_popup_artigo(artigo):
    """Gera o HTML para o pop-up de um artigo."""
    html = f"""
<h4>{artigo['titulo']}</h4>
<p>{artigo['conteudo'][:200]}...</p>
<p><strong>Local:</strong> {artigo['local']}</p>
"""
    return html


REGIAO_COLORS = {
    "Norte": "#783d19",
    "Nordeste": "#FFB703",
    "Centro-Oeste": "#405A37",
    "Sudeste": "#F77F00",
    "Sul": "#90BE6D",
    "default": "#CCCCCC",
}

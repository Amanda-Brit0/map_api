import folium
import json
from pathlib import Path
from folium import Element

VIEW_DIR = Path(__file__).parent
PROJECT_ROOT = VIEW_DIR.parent.parent
DATA_EXTERNAL_DIR = PROJECT_ROOT / "api_mapa" / "data_external"

REGIAO_COLORS = {
    "Norte": "#783d19",
    "Nordeste": "#FFB703",
    "Centro-Oeste": "#405A37",
    "Sudeste": "#F77F00",
    "Sul": "#90BE6D",
    "default": "#CCCCCC",
}


def load_geojson(filename: str = "brasil_geo.geojson") -> dict:
    file_path = DATA_EXTERNAL_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"GeoJSON não encontrado: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def darken_color(hex_color, factor=0.7):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def gerar_popup_artigo(artigo):
    html = f"""
<h4>{artigo['titulo']}</h4>
<p>{artigo['conteudo'][:200]}...</p>
<p><strong>Local:</strong> {artigo['local']}</p>
"""
    return html


def generate_map_object(initial_coords=None) -> folium.Map: 
    """Função que gera um objeto mapa em representação html do Folium.
        Percorre cada artigo e demonstra ele por pop-up no mapa."""
    geojson_data = load_geojson()
    if initial_coords is None:
        initial_coords = [-14.235, -51.9253]

    brazil_bounds = [[-34.0, -74.0], [5.5, -32.0]]

    m = folium.Map(
        location=initial_coords,
        zoom_start=4,
        tiles="OpenStreetMap",
        min_zoom=4,
        max_zoom=6,
        max_bounds=True,
    )
    m.fit_bounds(brazil_bounds)

    def style_function(feature):
        regiao = feature["properties"].get("regiao", "default")
        fill_color = REGIAO_COLORS.get(regiao, REGIAO_COLORS["default"])
        return {
            "fillColor": fill_color,
            "color": "#000000",
            "weight": 1,
            "fillOpacity": 0.7,
        }

    def highlight_function(feature):
        regiao = feature["properties"].get("regiao", "default")
        fill_color = REGIAO_COLORS.get(regiao, REGIAO_COLORS["default"])
        return {
            "fillColor": darken_color(fill_color),
            "color": "#000000",
            "weight": 2,
            "fillOpacity": 0.9,
        }

    popup_geojson = folium.GeoJsonPopup(
        fields=["name", "regiao"],
        aliases=["<strong>Estado:</strong> ", "<strong>Região:</strong> "],
        localize=True,
        labels=True,
        parse_html=True,
    )

    geo_layer = folium.GeoJson(
        geojson_data,
        name="Estados do Brasil",
        style_function=style_function,
        highlight_function=highlight_function,
        popup=popup_geojson,
    )
    geo_layer.add_to(m)

    artigos = [
        {
            "id": 23,
            "titulo": "O frevo",
            "conteudo": "O frevo surgiu no início do século XX...",
            "local": "Recife - PE",
            "coordenadas": [-8.0476, -34.8770],
        },
        {
            "id": 24,
            "titulo": "Maracatu",
            "conteudo": "O maracatu é uma manifestação musical...",
            "local": "São Paulo - SP",
            "coordenadas": [-23.5505, -46.6333],
        },
    ]

    icon_url = "https://leafletjs.com/examples/custom-icons/leaf-orange.png"
    artigos_layer = folium.FeatureGroup(name="Artigos")
    artigos_layer.add_to(m)

    for artigo in artigos:
        popup = folium.Popup(gerar_popup_artigo(artigo), parse_html=True)
        icon = folium.CustomIcon(icon_url, icon_size=(32, 32), icon_anchor=(16, 32))
        folium.Marker(location=artigo["coordenadas"], popup=popup, icon=icon).add_to(
            artigos_layer
        )

    folium.LayerControl().add_to(m)

    return m.get_root()._repr_html_()
    # para teste, gera o objeto mapa e não html
    # return m


# Para teste de geração
# if __name__ == "__main__":
#     MAP_TEMPLATES_DIR = PROJECT_ROOT / "api_mapa" / "map_templates"
#     MAP_TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

#     output_filename = MAP_TEMPLATES_DIR / "mapa_teste.html"
#     print("Gerando mapa...")

#     try:
#         mapa = generate_map_object()
#         mapa.save(str(output_filename))
#         print(f"Mapa gerado com sucesso: {output_filename}")
#     except FileNotFoundError as e:
#         print(f"Erro: {e}")
#     except Exception as e:
#         print(f"Erro inesperado: {e}")

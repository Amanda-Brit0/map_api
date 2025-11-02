import folium
import json
from pathlib import Path

VIEW_DIR = Path(__file__).parent
PROJECT_ROOT = VIEW_DIR.parent.parent
DATA_EXTERNAL_DIR = PROJECT_ROOT / "api_mapa" / "data_external"

REGIAO_COLORS = {
    "Norte": "#783d19",
    "Nordeste": "#FFB703",
    "Centro-Oeste": "#405a37",
    "Sudeste": "#f77f00",
    "Sul": "#90be6d",
    "default": "#ccc",
}


def load_geojson(filename: str = "brasil_geo.geojson") -> dict:
    file_path = DATA_EXTERNAL_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"GeoJSON não encontrado. Caminho procurado: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_map_object(initial_coords=None) -> folium.Map:
    geojson_data = load_geojson()

    if initial_coords is None:
        initial_coords = [-14.235, -51.9253]

    initial_zoom = 4
    m = folium.Map(
        location=initial_coords,
        zoom_start=initial_zoom,
        tiles="OpenStreetMap",
        min_zoom=4,
        max_zoom=6,
    )

    def style_function(feature):
        regiao = feature["properties"].get("regiao", "default")
        fill_color = REGIAO_COLORS.get(regiao, REGIAO_COLORS["default"])

        return {
            "fillColor": fill_color,
            "color": feature["properties"].get("stroke", "#000"),
            "weight": feature["properties"].get("stroke-width", 1),
            "fillOpacity": feature["properties"].get("fill-opacity", 0.7),
        }

    folium.GeoJson(
        geojson_data, name="Brasil_Pindorama", style_function=style_function
    ).add_to(m)

    url = "https://leafletjs.com/examples/custom-icons/{}".format
    icon_image = url("leaf-red.png")
    shadow_image = url("leaf-shadow.png")

    icon = folium.CustomIcon(
        icon_image,
        icon_size=(38, 95),
        icon_anchor=(22, 94),
        shadow_image=shadow_image,
        shadow_size=(50, 64),
        shadow_anchor=(4, 62),
        popup_anchor=(-3, -76),
    )

    # vai receber as coordenadas da camada de dados, substituir em location
    folium.Marker(
        location=[-14, -51],
        icon=icon,
        popup="teste",
    ).add_to(m)

    # return m <- para teste, gera o objeto mapa e não html como abaixo
    # return m.get_root()._repr_html_()
    return m


if __name__ == "__main__":
    MAP_TEMPLATES_DIR = PROJECT_ROOT / "api_mapa" / "map_templates"

    output_filename = MAP_TEMPLATES_DIR / "mapa_teste.html"
    print("Iniciando teste do mapa")

    try:
        map_object = generate_map_object()

        # salva o HTML do mapa
        map_object.save(str(output_filename))

        print(f"Sucesso! Mapa gerado e salvo em: {output_filename}")
        print("Abra este arquivo no seu navegador para visualizar o mapa.")

    except FileNotFoundError as e:
        print(f"ERRO no carregamento do GeoJSON: {e}")
    except Exception as e:
        print(f"ERRO inesperado durante a geração do mapa: {e}")

    print("--- Teste finalizado ---")

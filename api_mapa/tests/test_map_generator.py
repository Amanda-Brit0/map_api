import pytest
from pathlib import Path

from presentation.mapa_view import load_geojson, generate_map_object, DATA_EXTERNAL_DIR

@pytest.fixture
def geojson_path():
    return DATA_EXTERNAL_DIR / "brasil_geo.geojson"

# Teste carregamento do geojson
def test_load_geojson_sucesso(geojson_path):
    data = load_geojson()
    
    assert isinstance(data, dict)
    assert "features" in data
    assert "type" in data
    assert data["type"] == "FeatureCollection"


@pytest.mark.parametrize("coords", [
    ([-14.235, -51.9253]),  
])

# Teste gerador do mapa com sucesso
def test_generate_map_from_existing_geojson(coords):
    geojson_path = DATA_EXTERNAL_DIR / "brasil_geo.geojson"
    assert geojson_path.exists(), f"GeoJSON não encontrado em {geojson_path}"

    html_output = generate_map_object(initial_coords=coords)

    assert isinstance(html_output, str)
    assert "folium" in html_output.lower()
    assert "<div" in html_output.lower()
    assert "leaflet" in html_output.lower()

    possible_keywords = ["Estado", "Região", "name", "regiao", "feature"]
    assert any(k.lower() in html_output.lower() for k in possible_keywords), \
        "HTML do mapa não contém campos esperados do GeoJSON"

    print("\n✅ Mapa gerado com sucesso a partir do GeoJSON existente.")


# Teste gerador do mapa sem o geojson
def test_generate_map_object_sem_geojson(monkeypatch):
    fake_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Teste", "regiao": "Norte"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[-60, -10], [-50, -10], [-50, 0], [-60, 0], [-60, -10]]],
                },
            }
        ],
    }

    monkeypatch.setattr("presentation.mapa_view.load_geojson", lambda: fake_geojson)
    
    html_output = generate_map_object(initial_coords=[-14.235, -51.9253])
    
    assert isinstance(html_output, str)
    assert "folium" in html_output.lower()
    assert "Teste" in html_output or "Norte" in html_output

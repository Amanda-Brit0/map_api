import folium
from folium.plugins import MarkerCluster
import random

def gerar_mapa(artigos, eventos):
    #Cria um mapa interativo com os locais de artigos e eventos.
    """
    Cria um mapa interativo com os locais de artigos e eventos.
    
    Parâmetros:
        artigos (list): Lista de artigos, cada um com 'titulo' e 'local'.
        eventos (list): Lista de eventos, cada um com 'titulo' e 'local'.
    
    Retorna:
        str: HTML do mapa pronto para ser exibido.
    """
    mapa = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
    cluster = MarkerCluster().add_to(mapa)

    # Artigos
    for artigo in artigos:
        local = artigo.get("local", "Local não informado")
        titulo = artigo.get("titulo", "Sem título")
        lat = random.uniform(-33, 5)
        lon = random.uniform(-74, -34)

        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{titulo}</b><br>{local}<br><a href='#'>Ver artigo</a>",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(cluster)

    # Eventos
    for evento in eventos:
        local = evento.get("local", "Local não informado")
        titulo = evento.get("titulo", "Sem título")
        lat = random.uniform(-33, 5)
        lon = random.uniform(-74, -34)

        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{titulo}</b><br>{local}<br><a href='#'>Ver evento</a>",
            icon=folium.Icon(color="green", icon="star")
        ).add_to(cluster)

    return mapa._repr_html_()

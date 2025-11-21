from api_mapa.presentation.mapa_view import generate_map_object


def generate_map_html():
    """
    Função do serviço que chama o gerador de mapa.
    """

    mapa_html = generate_map_object()

    return mapa_html

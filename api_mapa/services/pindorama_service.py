# api_mapa/services/pindorama_service.py

import requests
from api_mapa.config import API_PINDORAMA_URL

def get_artigos():
    #Retorna a lista de artigos do backend Pindorama.
    #Se houver algum erro na requisição, retorna um dict com chave 'erro'.

    try:
        response = requests.get(f"{API_PINDORAMA_URL}/artigos")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"erro": str(e)}

def get_eventos():

    #Retorna a lista de eventos do backend Pindorama.
    #Se houver algum erro na requisição, retorna um dict com chave 'erro'.

    try:
        response = requests.get(f"{API_PINDORAMA_URL}/eventos")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"erro": str(e)}

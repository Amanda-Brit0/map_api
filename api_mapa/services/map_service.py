# app/services/map_service.py

import json
from api_mapa.data.processed import load_processed_data  # função que você criará em data/ ou utils/

def get_map_data():
    #Retorna os dados prontos do mapa em JSON.
    
    data = load_processed_data()
    # Aqui você poderia processar ou filtrar dados, se necessário
    return json.dumps(data,ensure_ascii=False, indent=2)

def save_map_data_to_file(filename="api_mapa/data/processed/map_data.json"):
    #Salva os dados processados do mapa em um arquivo JSON.
    data_json = get_map_data()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data_json)
# Ponto de entrada da aplicação Flask
from api_mapa import create_app

app = create_app()

if __name__ == "__main__":
    # Roda o servidor Flask(necessário para o Docker)
    app.run(host="0.0.0.0", port=5000, debug=True)

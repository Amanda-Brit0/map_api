# Usa imagem base leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia tudo para o container
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta que o Flask vai usar
EXPOSE 5000

# Comando para rodar o app
CMD ["python", "run.py"]

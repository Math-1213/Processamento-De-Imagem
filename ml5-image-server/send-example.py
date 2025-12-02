import requests
import json

# Caminho da imagem no seu computador
caminho_imagem = r"C:\Users\math1\Downloads\violao1.jpg"

# URL do servidor Node
url = "http://localhost:5000/processarImagem"

# Abrindo a imagem e enviando via POST
with open(caminho_imagem, "rb") as img_file:
    files = {"image": img_file}
    try:
        resposta = requests.post(url, files=files)
        resposta.raise_for_status()  # Levanta exceção se status != 200
        dados = resposta.json()
        
        print("Resposta do servidor:")
        print(json.dumps(dados, indent=2))  # Mostra bonito
    except requests.exceptions.RequestException as e:
        print("Erro ao enviar a imagem:", e)

import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import os

# CONSTANTS
url = "http://localhost:5000/processarImagem"
caminho_segmentado = "segmentado/img.jpg"

# FUNÇÕES AUXILIARES
def suavizacao_grab(caminho_imagem):
    """
    Aplica GrabCut assumindo que o objeto está centralizado.
    
    Args:
        caminho_imagem (str): Caminho do arquivo.
        margem_percent (float): Porcentagem da borda a ser considerada fundo.
                                0.05 significa 5% de margem em cada lado.
    """
    # 1. Carregar a imagem
    imagem_original = cv2.imread(caminho_imagem)
    if imagem_original is None:
        print(f"Erro: Não foi possível carregar a imagem em '{caminho_imagem}'")
        return
    imagem_original_rgb = cv2.cvtColor(imagem_original, cv2.COLOR_BGR2RGB)
    
    # --- Blur na imagem original --- #
    imagem_original = cv2.GaussianBlur(imagem_original, (1, 1), 0)

    # --- Início da Lógica do GrabCut Dinâmico ---
    margem_percent=0.04

    # 2. Definir um retângulo (ROI) DINÂMICO ao redor do centro
    # Obtém as dimensões reais da imagem carregada
    altura_img, largura_img = imagem_original.shape[:2]

    # Calcula o tamanho da margem em pixels
    margem_x = int(largura_img * margem_percent)
    margem_y = int(altura_img * margem_percent)

    # Define o retângulo centralizado.
    x_inicial = margem_x
    y_inicial = margem_y
    largura_rect = largura_img - (2 * margem_x)
    altura_rect = altura_img - (2 * margem_y)

    # O formato é (x_inicial, y_inicial, largura, altura)
    rect = (x_inicial, y_inicial, largura_rect, altura_rect)
    
    # Verificação de segurança: garante que o retângulo é válido
    if largura_rect <= 0 or altura_rect <= 0:
         print("Erro: A imagem é muito pequena ou a margem é muito grande.")
         return

    print(f"Imagem: {largura_img}x{altura_img}. Retângulo Dinâmico gerado: {rect}")

    # 3. Preparar os dados para o GrabCut
    # O algoritmo precisa de uma máscara inicial e de modelos para o fundo/objeto.
    mascara = np.zeros(imagem_original.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64) # Modelo do fundo (background)
    fgdModel = np.zeros((1, 65), np.float64) # Modelo do objeto (foreground)

    # 4. Executar o GrabCut
    # O algoritmo irá refinar a máscara dentro do retângulo que definimos.
    # Aumentei para 10 iterações para garantir melhor convergência em imagens variadas
    cv2.grabCut(imagem_original, mascara, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)

    # 5. Criar a máscara final para aplicação
    # O GrabCut marca o fundo provável/definitivo como 0 e 2, e o objeto como 1 e 3.
    # Nós criamos uma máscara onde tudo que for objeto (1 ou 3) vira branco (1) e o resto preto (0).
    mascara_final = np.where((mascara == 2) | (mascara == 0), 0, 1).astype('uint8')

    # 6. Aplicar a máscara na imagem original
    # Multiplicamos a imagem original pela máscara para manter apenas o objeto.
    # O np.newaxis é para que a máscara (2D) possa ser multiplicada pela imagem (3D).
    resultado_final = imagem_original_rgb * mascara_final[:, :, np.newaxis]

    # 7. Mostrar os resultados
    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    plt.title(f"1. Imagem Original ({largura_img}x{altura_img}) com Retângulo")
    # Desenha o retângulo na imagem para visualização
    img_com_rect = imagem_original_rgb.copy()
    x, y, w, h = rect
    cv2.rectangle(img_com_rect, (x, y), (x + w, y + h), (0, 255, 0), 2)
    plt.imshow(img_com_rect)
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title("2. Máscara Gerada pelo GrabCut")
    plt.imshow(mascara_final, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title("3. Resultado Final da Segmentação")
    plt.imshow(resultado_final)
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    cv2.imwrite(caminho_segmentado, cv2.cvtColor(resultado_final, cv2.COLOR_RGB2BGR))

# Envia para o servidor ml5 para classificação
def get_prediction(caminho_imagem):
    try:
        with open(caminho_imagem, "rb") as img_file:
            files = {
                "image": img_file
            }

            resposta = requests.post(url, files=files)
            resposta.raise_for_status()

            dados = resposta.json()
            print("\nResposta do servidor:")
            print(json.dumps(dados, indent=2))

            plotar_resultado(dados["resultado"])

    except requests.exceptions.RequestException as e:
        print("Erro ao enviar a imagem:", e)

def plotar_resultado(resultado):
    labels = [item["label"] for item in resultado]
    confidences = [item["confidence"] for item in resultado]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(labels, confidences)

    plt.title("Classificação da Imagem (ml5)")
    plt.ylabel("Confiança (%)")
    plt.xlabel("Classe")
    plt.ylim(0, 1)

    # Destacar o maior valor
    maior_idx = confidences.index(max(confidences))
    bars[maior_idx].set_edgecolor("black")
    bars[maior_idx].set_linewidth(2)

    # Mostrar porcentagem com 4 casas decimais
    for bar, conf in zip(bars, confidences):
        porcentagem = conf * 100
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{porcentagem:.4f}%",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.tight_layout()
    plt.show()

# --- Como Usar ---
def main():
    os.makedirs("segmentado", exist_ok=True)
    
    caminho = input("Digite o caminho da imagem: ").strip()

    if not os.path.isfile(caminho):
        print("Erro: caminho inválido.")
        return

    print("\nSegmentando imagem...")
    suavizacao_grab(caminho)

    if caminho_segmentado:
        print("\nEnviando imagem segmentada para o servidor ML5...")
        get_prediction(caminho_segmentado)
    else:
        print("Erro na segmentação.")

if __name__ == "__main__":
    main()





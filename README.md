# Processamento-De-Imagem
Servidor Node.js para processamento de imagens usando aprendizado de máquina. Permite enviar imagens via front-end ou requisições HTTP, processá-las usando modelos de classificação (como MobileNet) e retornar os resultados. Inclui preview de imagens no navegador e endpoints para salvar/processar imagens localmente.

# ML5 Image Server

Servidor Node.js para processamento de imagens com aprendizado de máquina, utilizando ML5.js (MobileNet) ou TensorFlow.js. Permite enviar imagens via front-end ou requisições HTTP, processá-las e salvar tanto a imagem original quanto o resultado do processamento.

---

## **Funcionalidades**

- Recebe imagens via upload ou POST HTTP.
- Salva imagens enviadas na pasta `uploads/`.
- Processa imagens usando modelo MobileNet.
- Retorna resultados do processamento em JSON.
- Preview das imagens e resultados diretamente no navegador.
- Estrutura modular: funções compartilhadas entre front-end e servidor Node.js.

---

## **Tecnologias**

- Node.js
- Express
- Multer (upload de arquivos)
- Cors
- Puppeteer (opcional, para ML5 em Node)
- ML5.js / TensorFlow.js
- p5.js (dependência de ML5)
- Front-end simples em HTML/JS para preview de imagens

---

## **Estrutura do Projeto**
ml5-image-server/
│
├─ uploads/ # Pasta para salvar imagens enviadas e processadas
├─ libs/ # Bibliotecas JS locais (opcional, p5.js e ml5.min.js)
├─ server.js # Servidor Node.js e endpoints
├─ functions.js # Funções para salvar/processar imagens
├─ index.html # Front-end para enviar imagens e ver resultados
├─ scripts.js # Script front-end para preview e classificação
├─ package.json # Dependências do projeto
└─ README.md


---

## **Instalação**

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/ml5-image-server.git
cd ml5-image-server

2. Instale as dependências:

npm install


2. Crie a pasta de uploads:

mkdir uploads

4. Uso

Inicie o servidor:

npm start


O servidor será iniciado em: http://localhost:5000.

Requisições HTTP: envie imagens via POST para os endpoints:

Salvar imagem:

POST /salvarImagem
Form-Data: image=<arquivo>


Processar imagem:

POST /processarImagem
Form-Data: image=<arquivo>


Resposta JSON:

{
  "message": "Imagem processada com sucesso!",
  "resultado": "uploads/processed_<nome_da_imagem>.json"
}


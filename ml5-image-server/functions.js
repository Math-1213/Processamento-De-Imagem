const puppeteer = require("puppeteer");
const path = require("path");
const fs = require("fs");

// Função para salvar a imagem localmente (no front-end é apenas preview, no Node salva no uploads/)
function mostrarImagem(imgSrc, container, labelText = null) {
  const imgContainer = document.createElement("div");
  imgContainer.style.margin = "20px 0";

  const imgEl = document.createElement("img");
  imgEl.src = imgSrc;
  imgEl.width = 200;

  imgContainer.appendChild(imgEl);

  if (labelText) {
    const label = document.createElement("p");
    label.innerText = labelText;
    imgContainer.appendChild(label);
  }

  container.appendChild(imgContainer);
}

// Função para processar imagem com MobileNet
async function processarImagemNode(caminhoImagem, pastaSaida) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  const ext = path.extname(caminhoImagem).toLowerCase();
  const mime = ext === ".png" ? "image/png" : "image/jpeg";
  const imageBase64 = fs.readFileSync(caminhoImagem, { encoding: "base64" });
  const imgDataUrl = `data:${mime};base64,${imageBase64}`;

  console.log("1")
  await page.goto("about:blank");
  await page.addScriptTag({
    url: "https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.6.0/p5.min.js",
  });
  console.log("1.5")
  await page.addScriptTag({
    url: "https://unpkg.com/ml5@1/dist/ml5.min.js",
  });
  console.log("2")

  await page.waitForFunction("typeof ml5 !== 'undefined'", { timeout: 10000 });

  const resultado = await page.evaluate(async (imgSrc) => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.src = imgSrc;
      img.onload = async () => {
        try {
          const classifier = await ml5.imageClassifier("MobileNet");
          const results = await classifier.classify(img);
          resolve(results);
        } catch (err) {
          console.error("Erro no evaluate:", err);
          reject(err);
        }
      };
      img.onerror = (e) => reject("Erro ao carregar imagem: " + e);
    });
  }, imgDataUrl);

  await browser.close();

  const outputFilename = path.join(
    pastaSaida,
    "processed_" + path.basename(caminhoImagem) + ".json"
  );
  fs.writeFileSync(outputFilename, JSON.stringify(resultado, null, 2));

  return outputFilename;
}

// Exportar funções para Node.js (server)
if (typeof module !== "undefined") {
  module.exports = { mostrarImagem, processarImagemNode };
}

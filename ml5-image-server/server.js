const express = require("express");
const multer = require("multer");
const cors = require("cors");
const path = require("path");
const fs = require("fs");

// Importar função do functions.js
const { processarImagemNode } = require("./functions");

const app = express();
const port = 5000;

app.use(cors());
app.use(express.json());

// Certifica que a pasta uploads existe
const uploadDir = path.join(__dirname, "uploads");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir);
}

// Configuração do multer para salvar imagens
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) =>
    cb(null, Date.now() + path.extname(file.originalname)),
});
const upload = multer({ storage });

// Endpoint para salvar imagem
app.post("/salvarImagem", upload.single("image"), (req, res) => {
  if (!req.file)
    return res.status(400).json({ message: "Nenhuma imagem enviada!" });

  console.log("Imagem salva:", req.file.filename);
  res.json({ message: "Imagem salva com sucesso!", filename: req.file.filename });
});

// Endpoint para processar imagem com ml5 + Puppeteer
app.post("/processarImagem", upload.single("image"), async (req, res) => {
  if (!req.file)
    return res.status(400).json({ message: "Nenhuma imagem enviada!" });

  const caminhoImagem = path.join(uploadDir, req.file.filename);
  console.log("Processando imagem:", req.file.filename);

  try {
    const resultadoProcessamento = await processarImagemNode(
      caminhoImagem,
      uploadDir
    );

    // Lê o JSON processado e retorna como resultado
    const dados = JSON.parse(fs.readFileSync(resultadoProcessamento, "utf8"));
    res.json({
      message: "Imagem processada com sucesso!",
      resultado: dados,
      arquivoProcessado: path.basename(resultadoProcessamento),
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Erro ao processar imagem", erro: err.toString() });
  }
});

// Servir arquivos estáticos (HTML/JS)
app.use(express.static("."));

app.listen(port, () => console.log(`Servidor rodando em http://localhost:${port}`));

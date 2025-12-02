const imageInput = document.getElementById("imageInput");
const imageList = document.getElementById("imageList");
const btnSalvar = document.getElementById("btnSalvar");
const btnProcessar = document.getElementById("btnProcessar");

let filesSelecionados = [];

// Pega os arquivos selecionados
imageInput.addEventListener("change", (event) => {
  filesSelecionados = Array.from(event.target.files);
  imageList.innerHTML = "";
  filesSelecionados.forEach(file => {
    const reader = new FileReader();
    reader.onload = (e) => {
      mostrarImagem(e.target.result, imageList);
    };
    reader.readAsDataURL(file);
  });
});

// Botão para salvar
btnSalvar.addEventListener("click", () => {
  filesSelecionados.forEach(file => {
    const formData = new FormData();
    formData.append("image", file);

    fetch("http://localhost:5000/salvarImagem", {
      method: "POST",
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      mostrarImagem(URL.createObjectURL(file), imageList, "Imagem salva!");
    });
  });
});

// Botão para processar
btnProcessar.addEventListener("click", () => {
  filesSelecionados.forEach(file => {
    const formData = new FormData();
    formData.append("image", file);

    fetch("http://localhost:5000/processarImagem", {
      method: "POST",
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      mostrarImagem(URL.createObjectURL(file), imageList, "Imagem processada!");
    });
  });
});

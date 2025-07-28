const allergyForm = document.getElementById("components-form");
const btnSubmit = document.getElementById("submit-check");
const btnAdd = document.querySelector("button[name='increase_allergy']");
const imageLabel = document.querySelector("label[for='image']");
const imageInput = document.getElementById("imageInput");
const loader = document.getElementById("loader");

// Função para adicionar mais inputs
function increaseAllergy() {
  let newInput = document.createElement("input");
  newInput.name = "components[]";
  newInput.type = "text";
  newInput.placeholder = "Insira um novo componente...";

  const buttonSubmit = allergyForm.querySelector('button[type="submit"]');
  allergyForm.insertBefore(newInput, buttonSubmit);
}

// Escutador para o botão "Checar!"
btnSubmit.addEventListener("click", function (event) {
  // Esconde todos os inputs de texto
  document.querySelectorAll("input[name='components[]']").forEach((input) => {
    input.style.display = "none";
  });

  // Esconde label e input de imagem
  imageLabel.style.display = "none";
  imageInput.style.display = "none";

  // Esconde botão de adicionar componente
  btnAdd.style.display = "none";

  // Troca texto do botão e desativa
  btnSubmit.innerText = "Checando...";
  btnSubmit.disabled = true;

  // Mostra loader
  loader.style.display = "grid";
});

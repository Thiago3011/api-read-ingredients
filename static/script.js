const allergyForm = document.getElementById("components-form");
const btnSubmit = document.getElementById("submit-check");
const btnAdd = document.querySelector("button[name='increase_allergy']");
const loader = document.getElementById("loader");
const fileNameSpan = document.getElementById('file-name');

// Função para adicionar mais inputs
function increaseAllergy() {
  let newInput = document.createElement("input");
  newInput.name = "components[]";
  newInput.type = "text";
  newInput.placeholder = "Insira um novo componente...";

  const uploadGroup = document.querySelector(".upload-group");
  allergyForm.insertBefore(newInput, uploadGroup);
}

// Listener para o evento submit do form
allergyForm.addEventListener("submit", function (event) {
    // Verifica se algum input de texto tem valor
  const inputs = allergyForm.querySelectorAll("input[name='components[]']");
  const algumInputPreenchido = Array.from(inputs).some(input => input.value.trim() !== "");

    // Verifica se algum arquivo foi selecionado
  const arquivoSelecionado = imageInput.files.length > 0;

  if (!algumInputPreenchido && !arquivoSelecionado) {
    alert("Por favor, preencha pelo menos um componente ou selecione uma imagem antes de continuar.");
    event.preventDefault(); 
    return; 
  }

  // Manipula visibilidade dos elementos antes de enviar
  allergyForm.querySelectorAll("input, label, p, button").forEach(el => {
    if (el === btnSubmit || el === loader) {
      el.style.display = "";
    } else {
      el.style.display = "none";
    }
  });

  if (fileNameSpan) {
    fileNameSpan.style.display = "none";
  }

  btnSubmit.innerText = "Checando...";
  btnSubmit.disabled = true;

  loader.style.display = "grid";

});

// Listener para o botão adicionar componentes
btnAdd.addEventListener("click", increaseAllergy);

// Atualiza nome do arquivo selecionado
const imageInput = document.getElementById("imageInput");
imageInput.addEventListener('change', () => {
  if (imageInput.files.length > 0) {
    fileNameSpan.style.display = 'inline';
    fileNameSpan.textContent = `Arquivo selecionado: ${imageInput.files[0].name}`;
  } else {
    fileNameSpan.style.display = 'none';
    fileNameSpan.textContent = '';
  }
});

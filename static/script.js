// Seleção dos elementos do DOM utilizados no script
const allergyForm = document.getElementById("components-form");
const btnSubmit = document.getElementById("submit-check");
const btnAdd = document.querySelector("button[name='increase_allergy']");
const loader = document.getElementById("loader");
const fileNameSpan = document.getElementById('file-name');
const imageInput = document.getElementById("imageInput");

/**
 * Adiciona dinamicamente um novo campo de input para o usuário inserir mais componentes alérgicos.
 * O novo input é inserido acima da área de upload.
 */
function increaseAllergy() {
  let newInput = document.createElement("input");
  newInput.name = "components[]";
  newInput.type = "text";
  newInput.placeholder = "Insira um novo componente...";

  const uploadGroup = document.querySelector(".upload-group");
  allergyForm.insertBefore(newInput, uploadGroup);
}

// Adiciona o campo ao clicar no botão "Adicionar Componente"
btnAdd.addEventListener("click", increaseAllergy);

/**
 * Listener para o envio do formulário.
 * Realiza validações:
 * - Garante que pelo menos um input esteja preenchido ou uma imagem tenha sido selecionada
 * - Exibe loader e altera o botão durante o processamento
 */
allergyForm.addEventListener("submit", function (event) {
  // Verifica se algum input foi preenchido
  const inputs = allergyForm.querySelectorAll("input[name='components[]']");
  const algumInputPreenchido = Array.from(inputs).some(input => input.value.trim() !== "");

  // Verifica se um arquivo foi selecionado
  const arquivoSelecionado = imageInput.files.length > 0;

  // Exibe alerta e cancela envio se nenhum dado foi fornecido
  if (!algumInputPreenchido && !arquivoSelecionado) {
    alert("Por favor, preencha pelo menos um componente ou selecione uma imagem antes de continuar.");
    event.preventDefault(); 
    return; 
  }

  // Oculta os elementos do formulário e exibe o loader durante o envio
  allergyForm.querySelectorAll("input, label, p, button").forEach(el => {
    if (el === btnSubmit || el === loader) {
      el.style.display = "";
    } else {
      el.style.display = "none";
    }
  });

  // Oculta o nome do arquivo durante o carregamento
  if (fileNameSpan) {
    fileNameSpan.style.display = "none";
  }

  // Atualiza o botão de submit para indicar carregamento
  btnSubmit.innerText = "Checando...";
  btnSubmit.disabled = true;
  loader.style.display = "grid";
});

/**
 * Atualiza o texto exibido com o nome do arquivo selecionado,
 * assim que o usuário escolhe um arquivo de imagem.
 */
imageInput.addEventListener('change', () => {
  if (imageInput.files.length > 0) {
    fileNameSpan.style.display = 'inline';
    fileNameSpan.textContent = `Arquivo selecionado: ${imageInput.files[0].name}`;
  } else {
    fileNameSpan.style.display = 'none';
    fileNameSpan.textContent = '';
  }
});

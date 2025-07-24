const allergyForm = document.getElementById("components-form")

function increaseAllergy() {
    let newInput = document.createElement('input')
    newInput.name = "components[]"
    newInput.type = "text";
    newInput.placeholder = "Insira um novo componente..."
    
    const buttonSubmit = allergyForm.querySelector('button[type="submit"]')
    allergyForm.insertBefore(newInput, buttonSubmit)
}

document.getElementById('imageInput').addEventListener('change', function(event) {
  const file = event.target.files[0];
  if (file) {
    alert(`📷 Nome do arquivo: ${file.name}\n📦 Tipo MIME: ${file.type}`);
    console.log('📷 Nome do arquivo:', file.name);
    console.log('📦 Tipo MIME:', file.type);
  } else {
    alert('Nenhum arquivo selecionado');
  }
});
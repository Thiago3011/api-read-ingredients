const allergyForm = document.getElementById("components-form")

function increaseAllergy() {
    let newInput = document.createElement('input')
    newInput.name = "components[]"
    newInput.type = "text";
    newInput.placeholder = "Insira um novo componente..."
    
    const buttonSubmit = allergyForm.querySelector('button[type="submit"]')
    allergyForm.insertBefore(newInput, buttonSubmit)
}
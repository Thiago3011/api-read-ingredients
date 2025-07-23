const allergyForm = document.getElementById("ingredients-form")

function increaseAllergy() {
    let newInput = document.createElement('input')
    newInput.name = "ingredients[]"
    newInput.type = "text";
    
    const buttonSubmit = allergyForm.querySelector('button[type="submit"]')
    allergyForm.insertBefore(newInput, buttonSubmit)
}
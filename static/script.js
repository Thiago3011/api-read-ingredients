// =========================
// CONFIGURAÇÃO
// =========================

const API_BASE_URL = "";


// =========================
// ELEMENTOS — PERFIL
// =========================

const profileButton = document.getElementById("profile-button");
const profileMenu = document.getElementById("profile-menu");
const myAllergiesButton = document.getElementById("my-allergies-button");
const logoutButton = document.getElementById("logout-button");


// =========================
// ELEMENTOS — AUTH
// =========================

const authScreen = document.getElementById("auth-screen");
const checkerScreen = document.getElementById("checker-screen");

const loginContainer = document.getElementById("login-container");
const registerContainer = document.getElementById("register-container");

const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");

const showRegisterButton = document.getElementById("show-register");
const showLoginButton = document.getElementById("show-login");

const loginMessage = document.getElementById("login-message");
const registerMessage = document.getElementById("register-message");


// =========================
// ELEMENTOS — ALERGIAS
// =========================

const allergiesModal = document.getElementById("allergies-modal");
const closeAllergiesModal = document.getElementById(
    "close-allergies-modal"
);

const createAllergyForm = document.getElementById(
    "create-allergy-form"
);

const newAllergyInput = document.getElementById(
    "new-allergy"
);

const allergyMessage = document.getElementById(
    "allergy-message"
);

const allergiesList = document.getElementById(
    "allergies-list"
);

const allergySearch = document.getElementById(
    "allergy-search"
);


// =========================
// ELEMENTOS — VALIDAÇÃO
// =========================

const validationForm = document.getElementById(
    "validation-form"
);

const componentsInput = document.getElementById(
    "components"
);

const imageInput = document.getElementById(
    "image"
);

const fileName = document.getElementById(
    "file-name"
);

const validateButton = document.getElementById(
    "validate-button"
);

const validationMessage = document.getElementById(
    "validation-message"
);

const loader = document.getElementById(
    "loader"
);

const result = document.getElementById(
    "result"
);

const resultContent = document.getElementById(
    "result-content"
);


// =========================
// TOKEN
// =========================

function getToken() {
    return localStorage.getItem("access_token");
}


function setToken(token) {
    localStorage.setItem("access_token", token);
}


function removeToken() {
    localStorage.removeItem("access_token");
}


// =========================
// AUTH STATE
// =========================

function updateAuthScreen() {

    const token = getToken();

    if (token) {
        authScreen.classList.add("hidden");
        checkerScreen.classList.remove("hidden");

        return;
    }

    checkerScreen.classList.add("hidden");
    authScreen.classList.remove("hidden");
}


// =========================
// MENSAGENS DE AUTH
// =========================

function showAuthMessage(
    element,
    message,
    success = false
) {

    if (!element) {
        return;
    }

    element.textContent = message || "";

    element.classList.toggle(
        "success",
        success
    );
}


function clearAuthMessages() {

    showAuthMessage(
        loginMessage,
        ""
    );

    showAuthMessage(
        registerMessage,
        ""
    );
}


// =========================
// PERFIL
// =========================

function closeProfileMenu() {

    if (!profileMenu) {
        return;
    }

    profileMenu.classList.add("hidden");
}


function toggleProfileMenu() {

    if (!profileMenu) {
        return;
    }

    profileMenu.classList.toggle("hidden");
}


// =========================
// AUTH FORM
// =========================

function showLoginForm() {

    loginContainer.classList.remove("hidden");
    registerContainer.classList.add("hidden");

    clearAuthMessages();
}


function showRegisterForm() {

    loginContainer.classList.add("hidden");
    registerContainer.classList.remove("hidden");

    clearAuthMessages();
}


// =========================
// MODAL ALERGIAS
// =========================

function openAllergiesModal() {

    closeProfileMenu();

    allergiesModal.classList.remove("hidden");

    allergySearch.value = "";

    clearAllergyMessage();

    loadAllergies();
}


function closeAllergiesModalWindow() {

    allergiesModal.classList.add("hidden");

    clearAllergyMessage();
}


// =========================
// UNAUTHORIZED
// =========================

function handleUnauthorized(message) {

    removeToken();

    closeProfileMenu();
    closeAllergiesModalWindow();

    updateAuthScreen();

    showLoginForm();

    showAuthMessage(
        loginMessage,
        message || "Sua sessão expirou. Faça login novamente."
    );
}


// =========================
// MODAIS
// =========================

if (allergiesModal) {

    allergiesModal.addEventListener(
        "click",
        (event) => {

            if (event.target === allergiesModal) {
                closeAllergiesModalWindow();
            }

        }
    );

}


document.addEventListener(
    "keydown",
    (event) => {

        if (event.key !== "Escape") {
            return;
        }

        closeProfileMenu();
        closeAllergiesModalWindow();

    }
);


// =========================
// PERFIL — CLICK
// =========================

if (profileButton) {

    profileButton.addEventListener(
        "click",
        (event) => {

            event.stopPropagation();

            if (!getToken()) {
                return;
            }

            toggleProfileMenu();

        }
    );

}


// =========================
// FECHAR MENU AO CLICAR FORA
// =========================

document.addEventListener(
    "click",
    (event) => {

        if (!profileMenu || !profileButton) {
            return;
        }

        if (
            !profileMenu.contains(event.target) &&
            !profileButton.contains(event.target)
        ) {

            closeProfileMenu();

        }

    }
);


// =========================
// MINHAS ALERGIAS
// =========================

if (myAllergiesButton) {

    myAllergiesButton.addEventListener(
        "click",
        () => {

            if (!getToken()) {
                handleUnauthorized(
                    "Você precisa estar logado para acessar suas alergias."
                );

                return;
            }

            openAllergiesModal();

        }
    );

}


// =========================
// LOGOUT
// =========================

if (logoutButton) {

    logoutButton.addEventListener(
        "click",
        () => {

            removeToken();

            closeProfileMenu();

            clearResult();
            clearMessage();

            updateAuthScreen();

        }
    );

}


// =========================
// AUTH — TROCA
// =========================

if (showRegisterButton) {

    showRegisterButton.addEventListener(
        "click",
        showRegisterForm
    );

}


if (showLoginButton) {

    showLoginButton.addEventListener(
        "click",
        showLoginForm
    );

}


// =========================
// LOGIN
// =========================

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();

            clearAuthMessages();

            const email = document
                .getElementById("login-email")
                .value
                .trim();

            const password = document
                .getElementById("login-password")
                .value;

            if (!email || !password) {

                showAuthMessage(
                    loginMessage,
                    "Preencha e-mail e senha."
                );

                return;
            }

            const submitButton =
                loginForm.querySelector(
                    "button[type='submit']"
                );

            if (submitButton) {
                submitButton.disabled = true;
            }

            try {

                const response = await fetch(
                    `${API_BASE_URL}/auth/login`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            email: email,
                            password: password
                        })
                    }
                );

                const data = await response.json();

                if (!response.ok) {

                    showAuthMessage(
                        loginMessage,
                        data.detail ||
                        "Não foi possível realizar o login."
                    );

                    return;
                }

                if (!data.access_token) {

                    showAuthMessage(
                        loginMessage,
                        "O servidor não retornou um token."
                    );

                    return;
                }

                setToken(data.access_token);

                updateAuthScreen();

                showAuthMessage(
                    loginMessage,
                    "Login realizado com sucesso!",
                    true
                );

            } catch (error) {

                console.error(
                    "Erro no login:",
                    error
                );

                showAuthMessage(
                    loginMessage,
                    "Não foi possível conectar ao servidor."
                );

            } finally {

                if (submitButton) {
                    submitButton.disabled = false;
                }

            }

        }
    );

}


// =========================
// CADASTRO
// =========================

if (registerForm) {

    registerForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();

            clearAuthMessages();

            const name = document
                .getElementById("register-name")
                .value
                .trim();

            const email = document
                .getElementById("register-email")
                .value
                .trim();

            const password = document
                .getElementById("register-password")
                .value;

            if (!name || !email || !password) {

                showAuthMessage(
                    registerMessage,
                    "Preencha todos os campos."
                );

                return;
            }

            const submitButton =
                registerForm.querySelector(
                    "button[type='submit']"
                );

            if (submitButton) {
                submitButton.disabled = true;
            }

            try {

                const response = await fetch(
                    `${API_BASE_URL}/user/`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            name: name,
                            email: email,
                            password: password
                        })
                    }
                );

                const data = await response.json();

                if (!response.ok) {

                    showAuthMessage(
                        registerMessage,
                        data.detail ||
                        "Não foi possível criar a conta."
                    );

                    return;
                }

                showAuthMessage(
                    registerMessage,
                    "Conta criada com sucesso! Agora faça login.",
                    true
                );

                registerForm.reset();

                setTimeout(
                    () => {

                        showLoginForm();

                        const loginEmail =
                            document.getElementById(
                                "login-email"
                            );

                        if (loginEmail) {
                            loginEmail.value = email;
                        }

                    },
                    700
                );

            } catch (error) {

                console.error(
                    "Erro no cadastro:",
                    error
                );

                showAuthMessage(
                    registerMessage,
                    "Não foi possível conectar ao servidor."
                );

            } finally {

                if (submitButton) {
                    submitButton.disabled = false;
                }

            }

        }
    );

}


// =========================
// UPLOAD — NOME DO ARQUIVO
// =========================

if (imageInput) {

    imageInput.addEventListener(
        "change",
        () => {

            if (!imageInput.files.length) {

                fileName.textContent =
                    "Nenhuma imagem selecionada";

                return;
            }

            fileName.textContent =
                imageInput.files[0].name;

        }
    );

}


// =========================
// MENSAGEM DA VALIDAÇÃO
// =========================

function showMessage(
    message,
    isError = true
) {

    if (!validationMessage) {
        return;
    }

    validationMessage.textContent =
        message || "";

    validationMessage.classList.remove(
        "hidden"
    );

    if (isError) {

        validationMessage.style.borderColor =
            "#4a3030";

        validationMessage.style.background =
            "#1c1010";

        validationMessage.style.color =
            "#e9a0a0";

    } else {

        validationMessage.style.borderColor =
            "#304a36";

        validationMessage.style.background =
            "#101c13";

        validationMessage.style.color =
            "#9ed6ad";

    }

}


function clearMessage() {

    if (!validationMessage) {
        return;
    }

    validationMessage.textContent = "";

    validationMessage.classList.add(
        "hidden"
    );
}


// =========================
// RESULTADO
// =========================

function clearResult() {

    if (!result || !resultContent) {
        return;
    }

    resultContent.innerHTML = "";

    result.classList.add("hidden");
}


function showResult(allergies) {

    if (!result || !resultContent) {
        return;
    }

    result.classList.remove("hidden");

    resultContent.innerHTML = "";

    if (
        !allergies ||
        !Array.isArray(allergies) ||
        allergies.length === 0
    ) {

        resultContent.innerHTML = `
            <p class="result-success">
                Nenhuma alergia encontrada para os
                componentes informados.
            </p>
        `;

        return;
    }

    const title = document.createElement("p");

    title.className = "result-danger";

    title.textContent =
        "Foram encontradas possíveis alergias:";

    resultContent.appendChild(title);

    const list =
        document.createElement("ul");

    list.className = "result-list";

    allergies.forEach(
        (allergy) => {

            const item =
                document.createElement("li");

            item.textContent = allergy;

            list.appendChild(item);

        }
    );

    resultContent.appendChild(list);
}


// =========================
// VALIDAÇÃO
// =========================

if (validationForm) {

    validationForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();

            clearMessage();
            clearResult();

            const token = getToken();

            if (!token) {

                updateAuthScreen();
                showAuthMessage(
                    loginMessage,
                    "Você precisa estar logado para realizar uma validação."
                );

                return;
            }

            const componentsValue =
                componentsInput.value.trim();

            const image =
                imageInput.files[0];

            if (!componentsValue && !image) {

                showMessage(
                    "Informe os componentes ou envie uma imagem."
                );

                return;
            }

            const formData =
                new FormData();

            if (componentsValue) {

                const components =
                    componentsValue
                        .split(",")
                        .map(
                            component =>
                                component.trim()
                        )
                        .filter(
                            component =>
                                component.length > 0
                        );

                components.forEach(
                    component => {

                        formData.append(
                            "components",
                            component
                        );

                    }
                );

            }

            if (image) {

                formData.append(
                    "image",
                    image
                );

            }

            loader.classList.remove(
                "hidden"
            );

            validateButton.disabled = true;

            try {

                const response =
                    await fetch(
                        `${API_BASE_URL}/validation/`,
                        {
                            method: "POST",

                            headers: {
                                Authorization:
                                    `Bearer ${token}`
                            },

                            body: formData
                        }
                    );

                if (response.status === 401) {

                    handleUnauthorized(
                        "Sua sessão expirou. Faça login novamente."
                    );

                    return;
                }

                const data =
                    await response.json();

                if (!response.ok) {

                    showMessage(
                        data.detail ||
                        "Não foi possível realizar a validação."
                    );

                    return;
                }

                showResult(
                    data.allergies
                );

            } catch (error) {

                console.error(
                    "Erro na validação:",
                    error
                );

                showMessage(
                    "Não foi possível conectar ao servidor."
                );

            } finally {

                loader.classList.add(
                    "hidden"
                );

                validateButton.disabled = false;

            }

        }
    );

}


// =========================
// ALERGIAS
// =========================

let allAllergies = [];


// =========================
// MENSAGEM DAS ALERGIAS
// =========================

function showAllergyMessage(
    message,
    isError = false
) {

    if (!allergyMessage) {
        return;
    }

    allergyMessage.textContent =
        message || "";

    allergyMessage.classList.toggle(
        "error",
        isError
    );
}


function clearAllergyMessage() {

    showAllergyMessage(
        "",
        false
    );
}


// =========================
// CARREGAR ALERGIAS
// =========================

async function loadAllergies() {

    if (!allergiesList) {
        return;
    }

    const token = getToken();

    if (!token) {

        handleUnauthorized(
            "Você precisa estar logado para acessar suas alergias."
        );

        return;
    }

    allergiesList.innerHTML = `
        <div class="allergies-loading">
            Carregando alergias...
        </div>
    `;

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/user/allergies/`,
                {
                    method: "GET",

                    headers: {
                        Authorization:
                            `Bearer ${token}`
                    }
                }
            );

        if (response.status === 401) {

            handleUnauthorized(
                "Sua sessão expirou. Faça login novamente."
            );

            return;
        }

        if (!response.ok) {

            const data =
                await response.json()
                    .catch(() => ({}));

            throw new Error(
                data.detail ||
                "Erro ao carregar suas alergias."
            );
        }

        const data =
            await response.json();

        allAllergies =
            Array.isArray(data)
                ? data
                : [];

        renderAllergies();

    } catch (error) {

        console.error(
            "Erro ao carregar alergias:",
            error
        );

        allergiesList.innerHTML = `
            <div class="allergies-empty">
                Não foi possível carregar suas alergias.
            </div>
        `;
    }
}


// =========================
// RENDERIZAR ALERGIAS
// =========================

function renderAllergies() {

    if (!allergiesList) {
        return;
    }

    const search =
        allergySearch.value
            .trim()
            .toLowerCase();

    const filteredAllergies =
        allAllergies.filter(
            allergy =>
                allergy.name
                    .toLowerCase()
                    .includes(search)
        );

    allergiesList.innerHTML = "";

    if (filteredAllergies.length === 0) {

        allergiesList.innerHTML = `
            <div class="allergies-empty">
                ${
                    search
                        ? "Nenhuma alergia encontrada."
                        : "Você ainda não cadastrou nenhuma alergia."
                }
            </div>
        `;

        return;
    }

    filteredAllergies.forEach(
        allergy => {

            const item =
                document.createElement("div");

            item.className =
                "allergy-item";

            const name =
                document.createElement("span");

            name.className =
                "allergy-name";

            name.textContent =
                allergy.name;

            const deleteButton =
                document.createElement("button");

            deleteButton.type =
                "button";

            deleteButton.className =
                "delete-allergy-button";

            deleteButton.title =
                "Excluir alergia";

            deleteButton.setAttribute(
                "aria-label",
                `Excluir ${allergy.name}`
            );

            deleteButton.textContent =
                "🗑️";

            deleteButton.addEventListener(
                "click",
                () => {
                    deleteAllergy(
                        allergy.id
                    );
                }
            );

            item.appendChild(name);
            item.appendChild(deleteButton);

            allergiesList.appendChild(item);

        }
    );
}


// =========================
// CRIAR ALERGIA
// =========================

if (createAllergyForm) {

    createAllergyForm.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();

            clearAllergyMessage();

            const token = getToken();

            if (!token) {

                handleUnauthorized(
                    "Sua sessão expirou. Faça login novamente."
                );

                return;
            }

            const name =
                newAllergyInput.value.trim();

            if (!name) {

                showAllergyMessage(
                    "Digite o nome da alergia.",
                    true
                );

                return;
            }

            const submitButton =
                createAllergyForm.querySelector(
                    "button[type='submit']"
                );

            if (submitButton) {
                submitButton.disabled = true;
            }

            try {

                const response =
                    await fetch(
                        `${API_BASE_URL}/user/allergies/?name=${encodeURIComponent(name)}`,
                        {
                            method: "POST",

                            headers: {
                                Authorization:
                                    `Bearer ${token}`
                            }
                        }
                    );

                if (response.status === 401) {

                    handleUnauthorized(
                        "Sua sessão expirou. Faça login novamente."
                    );

                    return;
                }

                const data =
                    await response.json();

                if (!response.ok) {

                    showAllergyMessage(
                        data.detail ||
                        "Não foi possível adicionar a alergia.",
                        true
                    );

                    return;
                }

                newAllergyInput.value = "";

                showAllergyMessage(
                    "Alergia adicionada com sucesso!"
                );

                await loadAllergies();

            } catch (error) {

                console.error(
                    "Erro ao criar alergia:",
                    error
                );

                showAllergyMessage(
                    "Não foi possível conectar ao servidor.",
                    true
                );

            } finally {

                if (submitButton) {
                    submitButton.disabled = false;
                }

            }

        }
    );

}


// =========================
// EXCLUIR ALERGIA
// =========================

async function deleteAllergy(
    allergyId
) {

    const token = getToken();

    if (!token) {

        handleUnauthorized(
            "Sua sessão expirou. Faça login novamente."
        );

        return;
    }

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/user/allergies/${allergyId}`,
                {
                    method: "DELETE",

                    headers: {
                        Authorization:
                            `Bearer ${token}`
                    }
                }
            );

        if (response.status === 401) {

            handleUnauthorized(
                "Sua sessão expirou. Faça login novamente."
            );

            return;
        }

        const data =
            await response.json()
                .catch(() => ({}));

        if (!response.ok) {

            showAllergyMessage(
                data.detail ||
                "Não foi possível excluir a alergia.",
                true
            );

            return;
        }

        showAllergyMessage(
            "Alergia removida com sucesso!"
        );

        await loadAllergies();

    } catch (error) {

        console.error(
            "Erro ao excluir alergia:",
            error
        );

        showAllergyMessage(
            "Não foi possível conectar ao servidor.",
            true
        );
    }
}


// =========================
// BUSCA
// =========================

if (allergySearch) {

    allergySearch.addEventListener(
        "input",
        renderAllergies
    );

}


// =========================
// FECHAR MODAL
// =========================

if (closeAllergiesModal) {

    closeAllergiesModal.addEventListener(
        "click",
        closeAllergiesModalWindow
    );

}


// =========================
// INICIALIZAÇÃO
// =========================

function initializeApp() {

    closeProfileMenu();
    closeAllergiesModalWindow();

    clearMessage();
    clearResult();
    clearAllergyMessage();

    updateAuthScreen();

}


initializeApp();
async function handleRequestErrors(response) {
    if (!response.ok) {
        switch (response.status) {
            case 404:
                throw new Error(ERR.NOT_FOUND);
            case 403:
                throw new Error(ERR.ACCESS_DENIED);
            case 401:
                throw new Error(ERR.UNAUTHORIZED);
            case 429:
                throw new Error(ERR.TOO_MANY_REQUESTS);
            case 500:
                throw new Error(ERR.INTERNAL_SERVER_ERROR);
            default:
                throw new Error(ERR.REQUEST_ERROR);
        }
    }
}

function disabledForm(form, disabled = true) {
    var elementosFormulario = form.elements;

    for (var i = 0; i < elementosFormulario.length; i++) {
        elementosFormulario[i].disabled = disabled;
    }
}

async function submitForm(event, form, callback = null, c_method = null, loading_msg = DEF.PROCESSING) {
    event.preventDefault();
    if (!form.classList.contains('disabled')) {
        placeholderLoading('nav-loading');
        const loadingFlash = showFlashMessage(loading_msg, 'loadingFlash', 0);
        form.classList.add('disabled');
        form.classList.add('disableInputEvents');

        const formData = new FormData(form);
        const url = form.action;
        const method = c_method ? c_method : form.method;

        try {
            const response = await fetch(url, {
                method: method,
                body: formData,
                credentials: 'same-origin'
            });

            await handleRequestErrors(response);

            const req_data = await response.json();

            showFlashMessage(req_data.message, req_data.success ? 'successFlash' : 'errorFlash');
            resetErrorMessages(req_data.data.form_fields, req_data.data.form_errors);

            const cookies = response.headers.get('Set-Cookie');
            if (cookies) {
                document.cookie = cookies;

            }

            if (callback && typeof callback === 'string' && req_data.success) {
                executeCallbacks(callback, form.id, req_data)
            }
        } catch (error) {
            showFlashMessage(error.message, 'errorFlash');
            return error.status;
        } finally {
            setTimeout(() => {
                form.classList.remove('disabled');
                form.classList.remove('disableInputEvents');
                smoothErrorElement(loadingFlash, 250);
                placeholderLoading('nav-loading', false);
            }, 500);
        }
    }
}


async function addTemplate(urlRota, elementoId, executarScripts = false, showLoading = true) {
    const elemento = document.getElementById(elementoId);
    try {

        if (elemento && showLoading) {
            elemento.innerHTML = DEFAULT_LOADING_SPINNER;
        }

        const response = await fetch(urlRota);

        setTimeout(() => {
            switch (response.status) {
                case 401: location.reload(); break;
                case 403: location.reload(); break;
            }
        }, 2000);

        await handleRequestErrors(response);

        const html = await response.text();

        if (elemento) {
            elemento.innerHTML = html;
            if (executarScripts) {
                setInnerHTML(elemento, html);
            }
        }
    } catch (error) {
        showFlashMessage(error.message, 'errorFlash');
        if (elemento) {
            elemento.innerHTML = '';
        }

        return error.status;
    }
}

var pageImage = 1
var onlyArts = false
var currentQuery = ""
async function fetchImages(nextPage = false, only_arts = onlyArts, query = currentQuery) {

    onlyArts = only_arts;
    currentQuery = query;

    placeholderLoading('nav-loading');
    if (nextPage) pageImage++;
    else pageImage = 1;

    let fetchURL = "/api/gallery/list" + "?page=" + String(pageImage) + (only_arts ? "&is_artwork=True" : "") + (query != "" ? "&query=" + query : "")

    await fetch(fetchURL)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateImageGrid(data.data.images, nextPage ? true : false);
            } else {
                setTimeout(() => {
                    if (!nextPage) document.getElementById('imageGrid').innerHTML = "";
                }, 100);
            }
        })
        .catch(error => {
            showFlashMessage(error, "errorFlash")
        });

    setTimeout(() => {
        placeholderLoading('nav-loading', false)
    }, 500);
}

var pageModalities = 1;
var currentQuery = "";
var currentTags = "";
async function fetchModalities(nextPage = false, query = currentQuery, tags = currentTags) {

    currentTags = tags;
    currentQuery = query;

    placeholderLoading('nav-loading');
    if (nextPage) pageModalities++;
    else pageModalities = 1;

    let fetchURL = "/api/commissions/modality/list" + "?page=" + String(pageModalities) + (tags ? "&tags=" + tags : "") + (query != "" ? "&query=" + query : "")

    await fetch(fetchURL)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateModalityGrid(data.data.modalities, nextPage ? true : false);
            } else {
                setTimeout(() => {
                    if (!nextPage) document.getElementById('modalityGrid').innerHTML = "";
                }, 100);
            }
        })
        .catch(error => {
            showFlashMessage(error, "errorFlash")
        });

    setTimeout(() => {
        placeholderLoading('nav-loading', false)
    }, 500);
}
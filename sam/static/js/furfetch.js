async function handleRequestErrors(response) {
    if (!response.ok) {
        switch (response.status) {
            case 404:
                throw new Error(ERR.NOT_FOUND);
            case 403:
                throw new Error(ERR.ACCESS_DENIED);
            case 401:
                throw new Error(ERR.UNAUTHORIZED);
            default:
                throw new Error(ERR.REQUEST_ERROR);
        }
    }
}

async function submitForm(event, form, callback = null) {
    
    event.preventDefault();
    placeholderLoading('nav-loading')
    const loadingFlash = showFlashMessage(DEF.PROCESSING, 'loadingFlash', 0);
    form.classList.add('disabled');
    form.classList.add('disableInputEvents');

    const formData = new FormData(form);
    const url = form.action;
    const method = form.method;

    var req_data

    try {
        const response = await fetch(url, {
            method: method,
            body: formData,
        });

        await handleRequestErrors(response);

        req_data = await response.json();
        console.log('Resposta do servidor:', req_data.message);
        showFlashMessage(req_data.message, req_data.success ? 'successFlash' : 'errorFlash');
        resetErrorMessages(req_data.data.form_fields, req_data.data.form_errors);
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
            placeholderLoading('nav-loading', false)
        }, 500);
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
            switch (response.status){
                case 401: location.reload()
                case 403: location.reload()
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

function executeCallbacks(callback = "self" , target, data){
    switch (callback){
        case "self": resetAndShowImageLink(target, data);
    }
}

// Função para povoar a grade de imagens

var pageImage = 1
// Função para obter as imagens da API e povoar a grade de imagens
async function fetchImages(nextPage = false) {
    placeholderLoading('nav-loading');
    if(nextPage) pageImage++;
    else pageImage = 1;

    await fetch('/api/gallery/list' + "?page=" + String(pageImage))
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            populateImageGrid(data.data.images, nextPage ? true : false);
        } else {
            showFlashMessage(data.message, "warningFlash")
        }
    })
    .catch(error => {
        showFlashMessage(error, "errorFlash")
    });

    setTimeout(() => {
        placeholderLoading('nav-loading', false)
    }, 500);

    //smoothErrorElement(loadingFlash, 250);
}
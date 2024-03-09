async function submitForm(event, form) {
    var loadingFlash = showFlashMessage(DEF.PROCCESSING, 'loadingFlash', 0);
    event.preventDefault();
    form.classList.add('disabled')
    form.classList.add('disableInputEvents')

    const formData = new FormData(form);
    const url = form.action; 
    const metodo = form.method; 

    try {
        const response = await fetch(url, {
            method: metodo,
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Resposta do servidor:', data.message);
            showFlashMessage(data.message, data.success ? 'successFlash' : 'errorFlash');
            resetErrorMessages(data.data.form_data, data.data.form_errors)
        } else {
            console.error('Erro ao enviar o formulário:', response.statusText);
            switch (response.status) {
                case 404:
                    showFlashMessage(ERR.NOT_FOUND, 'errorFlash');
                    break;
                case 403:
                    showFlashMessage(ERR.ACCESS_DENIED, 'errorFlash');
                    break;
                case 401:
                    showFlashMessage(ERR.UNAUTHORIZED, 'errorFlash');
                    break;
                default:
                    showFlashMessage(ERR.REQUEST_ERROR, 'errorFlash');
            }
        }
        
        
    } catch (error) {
        console.error('Erro de rede:', error);
        showFlashMessage(ERR.REQUEST_ERROR, 'errorFlash');
    }
    setTimeout(() => {
        form.classList.remove('disabled')
        form.classList.remove('disableInputEvents')
        smoothErrorElement(loadingFlash, 250);
    }, 500);
    
}
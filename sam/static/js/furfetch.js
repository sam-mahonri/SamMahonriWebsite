async function submitForm(event, form) {
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
            showFlashMessage(response.statusText, 'errorFlash');
        }
        setTimeout(() => {
            form.classList.remove('disabled')
            form.classList.remove('disableInputEvents')
        }, 500);
        
    } catch (error) {
        console.error('Erro de rede:', error);
    }
}


var popupCallback = ["", {}]

function resetAndShowImageLink(id, data){
    popupCallback = ['refreshImgs', {}]
    resetForm(id);
    elementVisible(id, false);
    var linkMacroId = id + "-req-img-link";
    showLinkToCopy(linkMacroId, data.data.image_data.url);
    elementVisible(id + '-success-section', true);
    
}

function closePopsAndReload(){
    elementVisible('pop-container', false);
    elementVisible('pop-container-2', false);
    fetchImages(false);
}

function closeReloadSelf(id, data){
    popupCallback = ['reloadOpenedImage', {"image_id":data.data.form_fields.image_id}]
}

function reloadModalities(id, data){
    resetForm(id);
    elementVisible('pop-container', false);
    fetchModalities()
}

// Ações realizadas ao fechar o popUp
function popCallback(){
    switch(popupCallback[0]){
        case "refreshImgs": fetchImages(); break;
        case "refreshModalities": fetchModalities(); break;
        case "reloadOpenedImage": 
            fetchImages();
            launchPopup("/macro/image-viewer?db-image-id=" + popupCallback[1]["image_id"], 'pop-container'); break;
    }
}

// Ações realizadas quando a operação no servidor foi bem sucedida
function executeCallbacks(callback = "self" , target, data){
    switch (callback){
        case "self": resetAndShowImageLink(target, data); break;
        case "closeReloadSelf": closeReloadSelf(target, data); break;
        case "loginSuccess": window.location = "/admin"; break;
        case "closePops": closePopsAndReload(); break;
        case "reloadModalities": reloadModalities(target, data); break;
        case "onlyReloadModalities": popupCallback[0] = "refreshModalities"; break;
        case "closePopsModalities": reloadModalities(target, data); elementVisible('pop-container', false); break;
    }
}
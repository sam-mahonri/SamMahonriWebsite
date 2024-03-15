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
    
    setTimeout(() => {
        elementVisible('pop-container', false);
        elementVisible('pop-container-2', false);
        fetchImages(false);
        
    }, 1000);
    
}

function closeReloadSelf(id, data){
    console.log(data)
    popupCallback = ['reloadOpenedImage', {"image_id":data.data.form_fields.image_id}]
}

function popCallback(){
    switch(popupCallback[0]){
        case "refreshImgs": fetchImages(); break;
        case "reloadOpenedImage": 
            fetchImages();
            launchPopup("/macro/image-viewer?db-image-id=" + popupCallback[1]["image_id"], 'pop-container'); break;
    }
}
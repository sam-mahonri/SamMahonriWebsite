var popupCallback = ["", {}]

function resetAndShowImageLink(id, data){
    resetForm(id);
    var linkMacroId = id + "-req-img-link";
    showLinkToCopy(linkMacroId, data.data.image_data.url);
    elementVisible(id, false); elementVisible(id + '-success-section', true);
}

function popCallback(){
    switch(popupCallback[0]){
        case "refreshImgs": fetchImages();
    }
}
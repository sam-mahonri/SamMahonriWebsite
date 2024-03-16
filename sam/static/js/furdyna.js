document.addEventListener('DOMContentLoaded', function () {
    var elementosTopScroll = document.querySelectorAll('.topInvScroll');

    function verificaScroll() {
        elementosTopScroll.forEach(function (elemento) {
            var classOnScroll = elemento.getAttribute('class-on-scroll') || 'applyTopInvScroll';
            var offsetOnScroll = parseInt(elemento.getAttribute('offset-on-scroll')) || 32;
            var inverseOnScroll = elemento.getAttribute('inverse-on-scroll') || true

            if (window.scrollY > offsetOnScroll) {
                if (inverseOnScroll) { elemento.classList.remove(classOnScroll) }
                else { elemento.classList.add(classOnScroll); }
            } else {
                if (inverseOnScroll) { elemento.classList.add(classOnScroll); }
                else { elemento.classList.remove(classOnScroll); }
            }
        });
    }

    window.addEventListener('scroll', verificaScroll);

    verificaScroll();
});

function scrollToSection(element, duration = 1000) {
    const targetElement = document.getElementById(element);
    if (!targetElement) return;

    const targetPosition = targetElement.offsetTop,
        startPosition = window.scrollY || window.pageYOffset,
        distance = targetPosition - startPosition,
        startTime = performance.now();

    function scrollStep(timestamp) {
        const currentTime = timestamp - startTime;
        window.scrollTo(0, ease(currentTime, startPosition, distance, duration));
        if (currentTime < duration) {
            requestAnimationFrame(scrollStep);
        }
    }

    function ease(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t * t + b;
        t -= 2;
        return c / 2 * (t * t * t + 2) + b;
    }

    requestAnimationFrame(scrollStep);
}

function toggleMenu(bt) {
    var navbar = document.querySelector('.navbar');
    navbar.classList.toggle('noCollapsed');
    if (navbar.classList.contains('noCollapsed')) {lockBodyYScroll('hidden'); bt.innerHTML = '<i class="fa-regular fa-circle-xmark"></i>' }
    else {lockBodyYScroll('auto'); bt.innerHTML = '<i class="fa-solid fa-bars"></i>' }
};

function showFlashMessage(message, type = 'errorFlash', duration = 5000) {
    const flashContainer = document.querySelector('.flashMessages');
    const div = document.createElement('div');
    div.className = `flashMessage ${type} borderBox aos-init gapSmall flex alignCenter justifyCenter`;
    div.dataset.aos = 'zoom-in-right';
    div.dataset.aosDelay = '0';
    div.dataset.aosDuration = '250';
    if (type == "loadingFlash") { div.innerHTML = DEFAULT_LOADING_SPINNER }
    div.innerHTML += `<p>${message}</p>`;

    flashContainer.appendChild(div);
    if (duration != 0) {
        smoothErrorElement(div, duration);
    }

    return div
}

function smoothErrorElement(element, duration = 0) {
    setTimeout(() => {
        element.classList.add('opacity0');
        setTimeout(() => {
            element.remove();
        }, 1000);

    }, duration);

}

function resetErrorMessages(data, errors) {
    Object.keys(data).forEach(key => {
        input = document.getElementById(key)
        input.classList.remove('errorInput');
        const children = input.parentNode.parentNode.children;

        for (let i = 0; i < children.length; i++) {
            const child = children[i];
            if (child.tagName.toLowerCase() === 'span') {
                child.remove();
            }
        }
    });


    Object.keys(errors).forEach(key => {

        const element = document.getElementById(key);
        element.classList.add('errorInput');
        if (element) {

            errors[key].forEach(errorMessage => {
                const span = document.createElement('span');
                span.className = 'tag backRed';
                span.textContent = errorMessage;
                element.parentNode.parentNode.appendChild(span);
            });
        }
    });
}

function elementVisible(id, visible, lockBody = false) {
    var element = document.getElementById(id);

    if (visible) {
        element.classList.remove('hideElement');
    }

    setTimeout(() => {
        if (visible) {
            element.classList.remove('opacity0');
            if (lockBody) {
                lockBodyYScroll('hidden');
            }
        } else {
            element.classList.add('opacity0');
        }
    }, 50);

    setTimeout(() => {
        if (!visible) {
            element.classList.add('hideElement');
            if (lockBody) {
                lockBodyYScroll('auto');
            }
        }
    }, 400);
}

function lockBodyYScroll(type = 'hidden') {
    document.documentElement.style.setProperty('overflow-y', type, 'important');
}

function imgPreview(self, view) {
    var fileInput = self;
    var file = self ? fileInput.files[0] : null;
    var viewElement = document.getElementById(view)

    if (file && (file.type === 'image/png' || file.type === 'image/jpeg' || file.type === 'image/jpg' || file.type === 'image/gif')) {

        var reader = new FileReader();
        reader.onload = function (e) {

            viewElement.classList.remove('hideElement')
            viewElement.src = e.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        viewElement.classList.add('hideElement');
        if (file) showFlashMessage(ERR.IMAGE_NOT_ALLOWED, "errorFlash");
        if (file) fileInput.value = null;
    }
}

function resetForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
    }
}

function showLinkToCopy(LinkCopyId, link) {
    const COPY_LINK_ELEMENT = document.getElementById(LinkCopyId)
    const LINK_FIELD_ELEMENT = document.getElementById(LinkCopyId + "_link_input")

    COPY_LINK_ELEMENT.classList.remove('disabled')
    COPY_LINK_ELEMENT.classList.remove('disableInputEvents')
    COPY_LINK_ELEMENT.classList.remove('hideElement')

    LINK_FIELD_ELEMENT.value = link
}


// [obsoleto] AVISO: Este script executa todos os scripts de uma página recém modificada em um innerHTML(exemplo), tenho certeza que todos os elementos do HTML Jinja2 estão livres de códigos maliciosos para evitar ataques XSS
function setInnerHTML(elm, html) {
    elm.innerHTML = html;

    Array.from(elm.querySelectorAll("script"))
        .forEach(oldScriptEl => {
            const newScriptEl = document.createElement("script");

            Array.from(oldScriptEl.attributes).forEach(attr => {
                newScriptEl.setAttribute(attr.name, attr.value)
            });

            const scriptText = document.createTextNode(oldScriptEl.innerHTML);
            newScriptEl.appendChild(scriptText);

            oldScriptEl.parentNode.replaceChild(newScriptEl, oldScriptEl);
        });
}

function removeAllClasses(element, selector = 'a', classToRemove = "activeAT") {
    const elements = element.querySelectorAll(selector);
    elements.forEach(i => {
        i.classList.remove(classToRemove);
    });
}

function updateUrl(newUrl) { history.pushState(null, null, newUrl); }

window.addEventListener('beforeunload', function(event) {
    placeholderLoading('nav-loading');
});

// [obsoleto] Atualiza o conteúdo da página sem carregá-la novamente
async function changePage(c_page, r_page = null, self_link = null) { 
    if (!r_page) r_page = c_page.replace("c/", "");

    placeholderLoading('nav-loading')
    
    await addTemplate(c_page, 'all-content', true, false);
    scrollToSection('all-content', 0);

    setTimeout(() => {
        placeholderLoading('nav-loading', false)
    }, 1000);

    removeAllClasses(document.getElementById('main-navbar-links'), 'a', 'activeAT');
    if (self_link) self_link.classList.add('activeAT');

    toggleMenu(document.getElementById('mobile-expand-nav'))

    lockBodyYScroll('auto');

    updateUrl(r_page);
}

function placeholderLoading(elementId = "", show = true) {
    if (elementId != "") {
        var element = document.getElementById(elementId);
        show ? element.classList.remove("opacity0") : element.classList.add("opacity0");
    }

}

function changeLanguage(url) {
    const currentPagePath = window.location.pathname;
    window.location.href = `${url}?page=${currentPagePath}`;
}

function copyText(idInput=null, text = "") {
    var inputElement;
    if (idInput){
        inputElement = document.getElementById(idInput);
        text = inputElement.value;
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text)
            .then(() => {
                if(inputElement) inputElement.select();
                showFlashMessage(OK.COPIED, 'successFlash');
            })
            .catch(err => {
                showFlashMessage(ERR.COPY_ERROR, 'errorFlash');
            });
    } else {
        showFlashMessage(ERR.COPY_UNSUPPORTED, 'errorFlash');
    }
}

function toggleBtSubmit(ch, id){
    let btDel = document.getElementById(id + "-bt-submit");
    ch ? btDel.classList.remove('disabled') : btDel.classList.add('disabled');
}

var lockCheckScrollEnd = false;

function populateImageGrid(images, update = false) {
    const gridContainer = document.getElementById('imageGrid');
    const fragment = document.createDocumentFragment();

    if (!update) gridContainer.innerHTML = '';

    let loadedImagesCount = 0;
    let indexCounter = 0;

    images.forEach((image, index) => {
        indexCounter++;
        const container = document.createElement('div');
        container.classList.add('imageContainer');

        container.onclick = function(){
            launchPopup("/macro/image-viewer?db-image-id=" + image._id, 'pop-container')
        }

        const imageElement = new Image();
        imageElement.classList.add('aos-init');
        imageElement.dataset.aos = 'zoom-out';
        imageElement.dataset.aosDelay = String(indexCounter * 200);
        imageElement.alt = image.title;

        const overlay = document.createElement('div');
        overlay.classList.add('overlay');

        const title = document.createElement('h3');
        title.textContent = image.title;

        const tag = document.createElement('span');
        tag.classList.add('tag');
        tag.innerHTML = '<i class="fas fa-paint-brush"></i>';

        overlay.appendChild(title);
        if (image.is_artwork) overlay.appendChild(tag);


        container.appendChild(imageElement);
        container.appendChild(overlay);

        fragment.appendChild(container);

        imageElement.onload = () => {
            loadedImagesCount++;

            if (loadedImagesCount === images.length) {
                gridContainer.appendChild(fragment);

                setTimeout(() => {
                    gridContainer.querySelectorAll('.imageContainer').forEach(container => {
                        container.querySelector('img').classList.add('active');
                    });
                }, 0);

                const lastImageContainer = gridContainer.querySelector('.imageContainer:last-child');
                if (lastImageContainer) {
                    lockCheckScrollEnd = false;
                    checkScrollEnd(selector = '#imageGrid .imageContainer:last-child', 'image');
                }
            }
        };

        imageElement.src = image.image_links.thumbnail;
    });
}

function populateModalityGrid(modalities, update = false) {
    const gridContainer = document.getElementById('modalityGrid');
    const fragment = document.createDocumentFragment();

    if (!update) gridContainer.innerHTML = '';

    let loadedModalitiesCount = 0;
    let indexCounter = 0;

    modalities.forEach((modality, index) => {
        indexCounter++;
        const container = document.createElement('div');
        container.classList.add('postContainer');
        container.classList.add('aos-init');
        container.dataset.aos = 'fade-up';
        container.dataset.aosDelay = String(indexCounter * 200);

        const imageElement = new Image();
        imageElement.classList.add('aos-init');
        imageElement.dataset.aos = 'zoom-out';
        imageElement.dataset.aosDelay = String(indexCounter * 200);
        imageElement.alt = modality.title;

        const title = document.createElement('h2');
        title.textContent = modality.title;

        const description = document.createElement('p');
        description.textContent = modality.description;

        const price = document.createElement('h2');
        price.textContent = LC.CIFR + String(modality.type_value).replace('.', ',');

        const descrSection = document.createElement('div');
        descrSection.className = "paddingMedium flex columnFlex gapSmall wp100 alignCenter justifyCenter"

        container.appendChild(imageElement);
        descrSection.appendChild(title);
        descrSection.appendChild(description);
        descrSection.appendChild(price);
        
        if (SYMBOLIC_LOGGED){
            const commandSection = document.createElement('div');
            commandSection.className = "flex rowFlex gapMedium";

            const editBt = document.createElement('button');
            editBt.className = "selectorButton";
            editBt.innerHTML = "<i class='fa-solid fa-pen-to-square'></i>";
            editBt.onclick = function(){
                launchPopup('/macro/edit_modality?&slug=' + modality.slug, 'pop-container');
            }

            const deleteBt = document.createElement('button');
            deleteBt.className = "selectorButton";
            deleteBt.innerHTML = "<i class='fa-solid fa-trash-can'></i>";
            deleteBt.onclick = function(){
                launchPopup('/macro/delete-item?callback=closePopsModalities&item-id=' + modality.slug + '&route=/api/commissions/modality', 'pop-container');
            }

            commandSection.appendChild(editBt);
            commandSection.appendChild(deleteBt);

            descrSection.appendChild(commandSection);
        }       


        container.appendChild(descrSection)

        fragment.appendChild(container);

        imageElement.onload = () => {
            loadedModalitiesCount++;

            if (loadedModalitiesCount === modalities.length) {
                gridContainer.appendChild(fragment);

                setTimeout(() => {
                    gridContainer.querySelectorAll('.postContainer').forEach(container => {
                        container.querySelector('img').classList.add('active');
                    });
                }, 0);

                const lastModalityContainer = gridContainer.querySelector('.postContainer:last-child');
                if (lastModalityContainer) {
                    lockCheckScrollEnd = false;
                    checkScrollEnd(selector = '#modalityGrid .postContainer:last-child', 'modality');
                }
            }
        };

        imageElement.src = modality.image_link;
    });
}

function checkScrollEnd(selector, processType) {
    let requestId;
    
    function handleScroll() {
        const lastElement = document.querySelector(selector);
        if (lastElement) {
            const lastElementRect = lastElement.getBoundingClientRect();
            if (lastElementRect.bottom <= window.innerHeight + 256 && !lockCheckScrollEnd) {
                lockCheckScrollEnd = true;
                if (processType === 'modality') {
                    fetchModalities(true);
                } else if (processType === 'image') {
                    fetchImages(true);
                }
                
            }
        }
        requestId = null;
    }

    function requestCheckScrollEnd() {
        if (!requestId) {
            requestId = window.requestAnimationFrame(handleScroll);
        }
    }

    window.addEventListener('scroll', requestCheckScrollEnd);

    requestCheckScrollEnd();

    return function () {
        window.removeEventListener('scroll', requestCheckScrollEnd);
    };
}

function launchPopup(url, popupId){
    elementVisible(popupId, true, false);
    addTemplate(url, popupId + "-content");
    popupCallback = ['', {}];
    
}
document.addEventListener('DOMContentLoaded', function () {
    var elementosTopScroll = document.querySelectorAll('.topInvScroll');

    function verificaScroll() {
        elementosTopScroll.forEach(function(elemento) {
            var classOnScroll = elemento.getAttribute('class-on-scroll') || 'applyTopInvScroll';
            var offsetOnScroll = parseInt(elemento.getAttribute('offset-on-scroll')) || 32;
            var inverseOnScroll = elemento.getAttribute('inverse-on-scroll') || true

            if (window.scrollY > offsetOnScroll) {
                if(inverseOnScroll){elemento.classList.remove(classOnScroll)}
                else{elemento.classList.add(classOnScroll);}
            } else {
                if(inverseOnScroll){elemento.classList.add(classOnScroll);}
                else{elemento.classList.remove(classOnScroll);}
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

function showFlashMessage(message, type='errorFlash', duration=5000) {
    const flashContainer = document.querySelector('.flashMessages');
    const div = document.createElement('div');
    div.className = `flashMessage ${type} borderBox aos-init`;
    div.dataset.aos = 'zoom-in-right';
    div.dataset.aosDelay = '0';
    div.dataset.aosDuration = '500';
    div.innerHTML = `<p>${message}</p>`;
    
    flashContainer.appendChild(div);
    setTimeout(() => {
        div.classList.add('opacity0');
        setTimeout(() => {
            flashContainer.removeChild(div);
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
document.addEventListener('DOMContentLoaded', function () {
    var elementosNoBack = document.querySelectorAll('.noBack');

    function verificaScroll() {
        elementosNoBack.forEach(function(elemento) {
            if (window.scrollY > 32) {
                elemento.classList.remove('applyNoBack');
            } else {
                elemento.classList.add('applyNoBack');
            }
        });
    }

    window.addEventListener('scroll', verificaScroll);

    verificaScroll();
});

function scrollToSection(element, duration = 2000) {
    const targetElement = document.getElementById(element);
    if (!targetElement) return; // Verifica se o elemento existe

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
        // Função de easing personalizada para entrada e saída mais lentas
        t /= d / 2;
        if (t < 1) return c / 2 * t * t * t + b; // Mais lento no início
        t -= 2;
        return c / 2 * (t * t * t + 2) + b; // Mais lento no final
    }

    requestAnimationFrame(scrollStep);
}

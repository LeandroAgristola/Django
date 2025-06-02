document.addEventListener("DOMContentLoaded", function () {
    const toggler = document.querySelector(".navbar-toggler");
    const menu = document.querySelector(".navbar-collapse");
    const body = document.body;
    const links = document.querySelectorAll(".nav-link");
    const header = document.querySelector("header"); // Capturamos el header

    toggler.addEventListener("click", function () {
        const headerHeight = header.offsetHeight; // Altura del header dinámicamente
        menu.style.top = `${headerHeight}px`; // Ajustamos el menú debajo del header

        if (!menu.classList.contains("show")) {
            menu.style.display = "flex"; // Se muestra antes de animar
            setTimeout(() => {
                menu.classList.add("show");
            }, 10); // Pequeño delay para activar la animación
        } else {
            menu.classList.remove("show");
            setTimeout(() => {
                menu.style.display = "none";
            }, 300); // Se oculta después de la animación
        }

        toggler.classList.toggle("active");
        body.classList.toggle("menu-open");
    });

    // Cerrar el menú cuando se hace clic en un enlace del navbar
    links.forEach(link => {
        link.addEventListener("click", function () {
            menu.classList.remove("show");
            setTimeout(() => {
                menu.style.display = "none";
            }, 300);
            toggler.classList.remove("active");
            body.classList.remove("menu-open");
        });
    });
});
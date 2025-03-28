document.addEventListener("DOMContentLoaded", function () {
    const toggler = document.querySelector(".navbar-toggler");
    const menu = document.querySelector(".navbar-collapse");

    toggler.addEventListener("click", function () {
        menu.classList.toggle("show");
        toggler.classList.toggle("active");
    });

    // Cerrar el menú cuando se hace clic en un enlace del navbar
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function () {
            menu.classList.remove("show");
            toggler.classList.remove("active");
        });
    });
});
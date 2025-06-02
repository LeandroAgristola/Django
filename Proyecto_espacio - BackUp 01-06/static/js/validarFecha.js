function validarFecha(formulario, inputId) {
    const inputFecha = document.getElementById(inputId);
    if (!inputFecha.value) {
        inputFecha.classList.add('is-invalid');
        return false;
    }
    return true;
}

const modo = document.getElementById('modo_cliente');
const cargado = document.getElementById('cliente_existente');
const nuevo = document.getElementById('nuevo_cliente');

modo.addEventListener('change', () => {
    if (modo.value === 'cargado') {
        cargado.style.display = 'block';
        nuevo.style.display = 'none';
    } else if (modo.value === 'nuevo') {
        cargado.style.display = 'none';
        nuevo.style.display = 'block';
    } else {
        cargado.style.display = 'none';
        nuevo.style.display = 'none';
    }
});
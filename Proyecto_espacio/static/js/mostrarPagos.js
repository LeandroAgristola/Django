const precioInput = document.getElementById('id_precio');
const opcionesPago = document.getElementById('opciones_pago');
const formaPago = document.getElementById('forma_pago');
const inputLinkPago = document.getElementById('input_link_pago');

precioInput.addEventListener('input', () => {
    const precio = parseFloat(precioInput.value) || 0;
    opcionesPago.style.display = precio > 0 ? 'block' : 'none';
});

formaPago.addEventListener('change', () => {
    inputLinkPago.style.display = formaPago.value === 'link' ? 'block' : 'none';
});
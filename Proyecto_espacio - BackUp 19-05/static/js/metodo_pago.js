document.addEventListener('DOMContentLoaded', function () {
    const precioInput = document.getElementById('id_precio');
    const metodoContainer = document.getElementById('metodo-pago-container');
    const linkPagoContainer = document.getElementById('link-pago-container');
    const selectMetodo = document.getElementById('id_metodo_pago');
  
    function toggleMetodoPago() {
      const precio = parseFloat(precioInput.value);
      if (!isNaN(precio) && precio > 0) {
        metodoContainer.style.display = "block";
        applyMetodoLogic();
      } else {
        metodoContainer.style.display = "none";
        linkPagoContainer.style.display = "none";
        if (selectMetodo) {
          selectMetodo.value = "";
        }
      }
    }
  
    function applyMetodoLogic() {
      if (!selectMetodo) return;
      const metodo = selectMetodo.value;
      if (metodo === "enlace") {
        linkPagoContainer.style.display = "block";
      } else {
        linkPagoContainer.style.display = "none";
      }
    }
  
    if (precioInput) {
      precioInput.addEventListener('input', toggleMetodoPago);
    }
    if (selectMetodo) {
      selectMetodo.addEventListener('change', applyMetodoLogic);
    }
  
    // Ejecutar al cargar para precargar la vista en caso de edición o valor ya definido
    toggleMetodoPago();
  });
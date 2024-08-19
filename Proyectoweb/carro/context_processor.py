def importe_total_carro(request):
    total = 0
    # Verifica si 'carro' está en la sesión
    if "carro" in request.session:
        for key, value in request.session["carro"].items():
            total += float(value["precio"])
    return {"importe_total_carro": total}
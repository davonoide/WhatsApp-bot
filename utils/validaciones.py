def corregir_numero_cel(numero):
    # Quitar letras y símbolos
    numero = "".join(filter(str.isdigit, numero))
    
    # Asegurar formato +52 para México
    if len(numero) == 10 and not numero.startswith("52"):
        numero = "52" + numero
    if not numero.startswith("+"):
        numero = "+" + numero

    return numero

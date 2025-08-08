import time
import random
from utils.driver import abrir_navegador
from utils.validaciones import corregir_numero_cel
from utils.enviar_mensaje import enviar_mensaje_telefonos as enviar_mensaje
from utils.lector_csv import cargar_csv, extraer_telefonos
from utils.lector_de_mensaje import leer_mensaje

def enviar_mensaje_whatsapp(ruta_csv, ruta_txt):
    print("📥 Cargando datos...")

    # Leer contactos del CSV
    df = cargar_csv(ruta_csv)
    if df is None:
        print("❌ No se pudo cargar el CSV.")
        return
    
    contactos = extraer_telefonos(df)
    if not contactos:
        print("❌ No se encontraron contactos en el CSV.")
        return

    mensaje = leer_mensaje(ruta_txt)
    if not mensaje:
        print("❌ No se pudo leer el mensaje.")
        return

    # Abrir navegador
    print("🟢 Abriendo navegador...")
    driver = abrir_navegador()
    try:
        driver.get("https://web.whatsapp.com/")
        print("\n⚠️ IMPORTANTE ⚠️")
        print("1. Escanea el código QR con WhatsApp Web")
        input("2. Presiona ENTER cuando estés listo...")

        for numero in contactos:
            numero_correcto = corregir_numero_cel(numero)
            print(f"➡️ Enviando a: {numero_correcto}")
            exito, mensaje_retorno = enviar_mensaje(driver, numero_correcto, mensaje)
            print(mensaje_retorno)
            time.sleep(random.uniform(2, 5))

        print("✅ Todos los mensajes han sido enviados.")

    finally:
        print("🔒 Cerrando navegador.")
        driver.quit()

def enviar_mensaje_whatsapp_directo(ruta_csv, ruta_txt, driver):
    from utils.lector_csv import cargar_csv, extraer_telefonos
    from utils.lector_de_mensaje import leer_mensaje
    from utils.validaciones import corregir_numero_cel
    from utils.enviar_mensaje import enviar_mensaje_telefonos
    import time, random

    df = cargar_csv(ruta_csv)
    if df is None:
        raise Exception("No se pudo cargar el archivo CSV.")
    
    contactos = extraer_telefonos(df)
    if not contactos:
        raise Exception("No se encontraron teléfonos válidos.")

    mensaje = leer_mensaje(ruta_txt)
    if not mensaje:
        raise Exception("No se pudo leer el archivo de mensaje.")

    for numero in contactos:
        numero_correcto = corregir_numero_cel(numero)
        exito, resultado = enviar_mensaje_telefonos(driver, numero_correcto, mensaje)
        print(resultado)
        time.sleep(random.uniform(2, 4))

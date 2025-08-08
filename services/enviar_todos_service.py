import time, random
from utils.lector_csv import cargar_csv, extraer_telefonos, extraer_grupos
from utils.lector_de_mensaje import leer_mensaje
from utils.validaciones import corregir_numero_cel
from utils.enviar_mensaje import enviar_mensaje_con_multimedia, enviar_mensaje_a_grupo

def enviar_mensajes_a_todos(ruta_csv, ruta_txt, driver, ruta_imagen=None, enviar_documento=False, ruta_documento=None):
    df = cargar_csv(ruta_csv)
    if df is None:
        raise Exception("❌ No se pudo cargar el archivo CSV.")

    mensaje = leer_mensaje(ruta_txt)
    if not mensaje:
        raise Exception("❌ No se pudo leer el archivo TXT.")

    # Teléfonos
    telefonos = extraer_telefonos(df)
    if telefonos:
        print(f"📱 Enviando a {len(telefonos)} teléfonos...")
        for numero in telefonos:
            numero_correcto = corregir_numero_cel(numero)
            exito, resultado = enviar_mensaje_con_multimedia(
                driver, numero_correcto, mensaje,
                ruta_imagen=ruta_imagen,
                enviar_documento=enviar_documento,
                ruta_documento=ruta_documento
            )
            print(resultado)
            time.sleep(random.uniform(2, 4))
    else:
        print("⚠️ No se encontraron teléfonos.")

    # Grupos
    grupos = extraer_grupos(df)
    if grupos:
        print(f"👥 Enviando a {len(grupos)} grupos...")
        for grupo in grupos:
            exito, resultado = enviar_mensaje_a_grupo(
                driver, grupo, mensaje,
                ruta_imagen=ruta_imagen,
                enviar_documento=enviar_documento,
                ruta_documento=ruta_documento
            )
            print(resultado)
            time.sleep(random.uniform(2, 4))
    else:
        print("⚠️ No se encontraron grupos.")

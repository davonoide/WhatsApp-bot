import time, random
from utils.lector_csv import cargar_csv, extraer_grupos
from utils.lector_de_mensaje import leer_mensaje
from utils.enviar_mensaje import enviar_mensaje_a_grupo

def enviar_mensaje_whatsapp_a_grupos(ruta_csv, ruta_txt, driver, ruta_imagen=None, enviar_documento=False, ruta_documento=None):
    df = cargar_csv(ruta_csv)
    if df is None:
        raise Exception("No se pudo cargar el archivo CSV.")

    grupos = extraer_grupos(df)
    if not grupos:
        raise Exception("No se encontraron nombres de grupos válidos.")

    mensaje = leer_mensaje(ruta_txt)
    if not mensaje:
        raise Exception("No se pudo leer el mensaje.")

    for grupo in grupos:
        exito, resultado = enviar_mensaje_a_grupo(
            driver, grupo, mensaje,
            ruta_imagen=ruta_imagen,
            enviar_documento=enviar_documento,
            ruta_documento=ruta_documento
        )
        print(resultado)
        time.sleep(random.uniform(2, 4))

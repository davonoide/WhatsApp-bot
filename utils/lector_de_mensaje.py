def leer_mensaje(ruta_txt):
    try:
        with open(ruta_txt, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            return contenido.strip()  # Elimina espacios/vacíos al inicio y fin
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_txt}")
        return None
    except Exception as e:
        print(f"⚠️ Error al leer el archivo: {e}")
        return None

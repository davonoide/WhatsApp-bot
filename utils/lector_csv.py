import pandas as pd
import os

def cargar_csv(ruta_csv):
    try:
        return pd.read_csv(ruta_csv)
    except Exception as e:
        print(f"❌ Error al cargar el archivo CSV: {e}")
        return None

def encontrar_columna(df, posibles_nombres):
    for nombre in df.columns:
        nombre_normalizado = nombre.lower().strip()
        for posible in posibles_nombres:
            if posible in nombre_normalizado:
                return nombre
    return None

def extraer_telefonos(df):
    columnas_telefono = ["telefono", "celular", "cel", "teléfono celular", "teléfono","telefonos", "teléfonos"]
    col_tel = encontrar_columna(df, columnas_telefono)
    if col_tel:
        return df[col_tel].dropna().astype(str).tolist()
    else:
        print("⚠️ No se encontró una columna de teléfono.")
        return []

def extraer_grupos(df):
    columnas_grupo = ["grupo", "grupos", "nombre del grupo"]
    col_grupo = encontrar_columna(df, columnas_grupo)
    if col_grupo:
        return df[col_grupo].dropna().astype(str).tolist()
    else:
        print("⚠️ No se encontró una columna de grupo.")
        return []

def obtener_ruta_archivo(valor, carpeta_base="."):
    if os.path.isabs(valor) or os.path.exists(valor):
        return valor
    posible_ruta = os.path.join(carpeta_base, valor)
    return posible_ruta if os.path.exists(posible_ruta) else None

def extraer_imagen(df, carpeta_base="."):
    columnas_imagen = ["imagen", "img", "layer", "flayer", "flyer", "foto"]
    col_img = encontrar_columna(df, columnas_imagen)
    if col_img:
        valor = df[col_img].dropna().astype(str).iloc[0]
        ruta = obtener_ruta_archivo(valor, carpeta_base)
        if ruta:
            return ruta
        print(f"⚠️ Imagen no encontrada en ruta: {valor}")
    else:
        print("⚠️ No se encontró una columna de imagen.")
    return None

def extraer_archivo(df, carpeta_base="."):
    columnas_archivo = ["archivo", "pdf", "programa", "documento"]
    col_arch = encontrar_columna(df, columnas_archivo)
    if col_arch:
        valor = df[col_arch].dropna().astype(str).iloc[0]
        ruta = obtener_ruta_archivo(valor, carpeta_base)
        if ruta:
            return ruta
        print(f"⚠️ Archivo no encontrado en ruta: {valor}")
    else:
        print("⚠️ No se encontró una columna de archivo.")
    return None


"""
from extractor_datos_csv import cargar_csv, extraer_telefonos, extraer_grupos, extraer_imagen, extraer_archivo

ruta_csv = "datos_contactos.csv"
df = cargar_csv(ruta_csv)

if df is not None:
    telefonos = extraer_telefonos(df)
    grupos = extraer_grupos(df)
    ruta_imagen = extraer_imagen(df)
    ruta_archivo = extraer_archivo(df)

    print("📱 Teléfonos:", telefonos)
    print("👥 Grupos:", grupos)
    print("🖼 Imagen:", ruta_imagen)
    print("📄 Archivo:", ruta_archivo)

"""
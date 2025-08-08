import flet as ft
import os
from utils.lector_de_mensaje import leer_mensaje

# Variables compartidas (puedes controlar visibilidad y estado desde fuera)
archivo_csv = None
archivo_txt = None
driver = None

def construir_seleccion_archivos(page: ft.Page):
    global archivo_csv, archivo_txt, driver

    # Widgets de texto para rutas y mensaje
    texto_ruta_csv = ft.Text("No se ha seleccionado archivo CSV.", size=14, color=ft.Colors.WHITE)
    texto_ruta_txt = ft.Text("No se ha seleccionado archivo TXT.", size=14, color=ft.Colors.WHITE)
    mensaje_contenido = ft.Text("", size=14, selectable=True, color=ft.Colors.WHITE)

    contenedor_ruta_csv = ft.Container(texto_ruta_csv, height=60, padding=10, bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE), border_radius=8, border=ft.border.all(1, ft.Colors.GREY_700))
    contenedor_ruta_txt = ft.Container(texto_ruta_txt, height=60, padding=10, bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE), border_radius=8, border=ft.border.all(1, ft.Colors.GREY_700))
    contenedor_mensaje = ft.Container(ft.Column([mensaje_contenido], scroll=ft.ScrollMode.AUTO), height=300, padding=10, bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE), border_radius=10, border=ft.border.all(1, ft.Colors.GREY_700))

    instrucciones = ft.Text("", size=16, color=ft.Colors.WHITE)
    boton_confirmar_envio = ft.ElevatedButton(text="Enviar mensaje", icon=ft.icons.SEND, visible=False, disabled=False)
    boton_iniciar = ft.ElevatedButton(text="Iniciar", icon=ft.icons.START, disabled=True)

    def verificar_todo_listo():
        if archivo_csv and archivo_txt:
            boton_iniciar.disabled = False
        else:
            boton_iniciar.disabled = True
        page.update()

    def seleccionar_archivo_csv(e: ft.FilePickerResultEvent):
        global archivo_csv
        if e.files:
            archivo_csv = e.files[0].path
            texto_ruta_csv.value = f"CSV seleccionado: {archivo_csv}"
        else:
            texto_ruta_csv.value = "No se seleccionó ningún archivo CSV."
        verificar_todo_listo()
        page.update()

    def seleccionar_archivo_txt(e: ft.FilePickerResultEvent):
        global archivo_txt
        if e.files:
            archivo_txt = e.files[0].path
            texto_ruta_txt.value = f"TXT seleccionado: {archivo_txt}"
            contenido = leer_mensaje(archivo_txt)
            mensaje_contenido.value = contenido if contenido else "⚠️ No se pudo leer el mensaje."
        else:
            texto_ruta_txt.value = "No se seleccionó ningún archivo TXT."
            mensaje_contenido.value = ""
        verificar_todo_listo()
        page.update()

    file_picker_csv = ft.FilePicker(on_result=seleccionar_archivo_csv)
    file_picker_txt = ft.FilePicker(on_result=seleccionar_archivo_txt)
    page.overlay.extend([file_picker_csv, file_picker_txt])

    boton_csv = ft.ElevatedButton(
        text="Seleccionar archivo CSV",
        on_click=lambda e: file_picker_csv.pick_files(
            allow_multiple=False,
            allowed_extensions=["csv"],
            initial_directory=os.path.abspath("archivos_input")
        )
    )

    boton_txt = ft.ElevatedButton(
        text="Seleccionar archivo TXT",
        on_click=lambda e: file_picker_txt.pick_files(
            allow_multiple=False,
            allowed_extensions=["txt"],
            initial_directory=os.path.abspath("archivos_input")
        )
    )

    return {
        "boton_csv": boton_csv,
        "contenedor_ruta_csv": contenedor_ruta_csv,
        "boton_txt": boton_txt,
        "contenedor_ruta_txt": contenedor_ruta_txt,
        "contenedor_mensaje": contenedor_mensaje,
        "boton_iniciar": boton_iniciar,
        "instrucciones": instrucciones,
        "boton_confirmar_envio": boton_confirmar_envio,
        "get_archivos": lambda: (archivo_csv, archivo_txt),
        "set_driver": lambda d: globals().__setitem__('driver', d),
        "get_driver": lambda: driver
    }

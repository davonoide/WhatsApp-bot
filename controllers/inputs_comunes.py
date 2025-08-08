import flet as ft
import os
from utils.lector_de_mensaje import leer_mensaje

# Variables compartidas (puedes controlar visibilidad y estado desde fuera)
archivo_csv = None
archivo_txt = None
driver = None
ruta_imagen = None
ruta_documento = None
enviar_imagen = False
enviar_documento = False


def construir_seleccion_archivos(page: ft.Page):
    global archivo_csv, archivo_txt, driver

    # Widgets de texto para rutas y mensaje
    texto_ruta_csv = ft.Text("No se ha seleccionado archivo CSV.", size=14, color=ft.Colors.WHITE)
    texto_ruta_txt = ft.Text("No se ha seleccionado archivo TXT.", size=14, color=ft.Colors.WHITE)
    mensaje_contenido = ft.Text("", size=14, selectable=True, color=ft.Colors.WHITE)
    texto_ruta_imagen = ft.Text("No se ha seleccionado imagen.", size=14, color=ft.Colors.WHITE)
    texto_ruta_documento = ft.Text("No se ha seleccionado archivo.", size=14, color=ft.Colors.WHITE)

    contenedor_ruta_imagen = ft.Container(texto_ruta_imagen, padding=10, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), border_radius=8, border=ft.border.all(1, ft.Colors.GREY_700), visible=False)
    contenedor_ruta_documento = ft.Container(texto_ruta_documento, padding=10, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), border_radius=8, border=ft.border.all(1, ft.Colors.GREY_700), visible=False)


    contenedor_ruta_csv = ft.Container(texto_ruta_csv, padding=10, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), border_radius=8, border=ft.border.all(1, ft.Colors.GREY_700))
    contenedor_ruta_txt = ft.Container(texto_ruta_txt, padding=10, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), border_radius=8, border=ft.border.all(1, ft.Colors.GREY_700))
    contenedor_mensaje = ft.Container(ft.Column([mensaje_contenido], scroll=ft.ScrollMode.AUTO), height=300, padding=10, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), border_radius=10, border=ft.border.all(1, ft.Colors.GREY_700))

    instrucciones = ft.Text("", size=16, color=ft.Colors.WHITE)
    boton_confirmar_envio = ft.ElevatedButton(text="Enviar mensaje", icon=ft.Icons.SEND, visible=False, disabled=False)
    boton_iniciar = ft.ElevatedButton(text="Iniciar", icon=ft.Icons.START, disabled=True)

    switch_imagen = ft.Switch(label="¿Enviar imagen?", value=False)
    switch_documento = ft.Switch(label="¿Enviar archivo?", value=False)

    divider_imagen = ft.Divider(visible=False)
    divider_documento = ft.Divider(visible=False)
    fila_switches = ft.Row([switch_imagen, switch_documento])

    imagen_preview = ft.Image(
        src="",
        width=200,
        height=200,
        fit=ft.ImageFit.CONTAIN,
        visible=False,
    )



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

    def seleccionar_imagen(e: ft.FilePickerResultEvent):
        global ruta_imagen
        if e.files:
            ruta_imagen = e.files[0].path
            texto_ruta_imagen.value = f"Imagen: {ruta_imagen}"
            imagen_preview.src = ruta_imagen
            imagen_preview.visible = True
        else:
            ruta_imagen = None
            texto_ruta_imagen.value = "No se seleccionó imagen."
            imagen_preview.visible = False
            imagen_preview.src = ""
        page.update()


    def seleccionar_documento(e: ft.FilePickerResultEvent):
        global ruta_documento
        if e.files:
            ruta_documento = e.files[0].path
            texto_ruta_documento.value = f"Archivo: {ruta_documento}"
        else:
            texto_ruta_documento.value = "No se seleccionó archivo."
        page.update()

    file_picker_csv = ft.FilePicker(on_result=seleccionar_archivo_csv)
    file_picker_txt = ft.FilePicker(on_result=seleccionar_archivo_txt)
    page.overlay.extend([file_picker_csv, file_picker_txt])

    file_picker_imagen = ft.FilePicker(on_result=seleccionar_imagen)
    file_picker_documento = ft.FilePicker(on_result=seleccionar_documento)
    page.overlay.extend([file_picker_imagen, file_picker_documento])


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

    boton_imagen = ft.ElevatedButton(
        text="Seleccionar imagen",
        visible=False,
        on_click=lambda e: file_picker_imagen.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"],
            initial_directory=os.path.abspath("archivos_input")
        )
    )

    boton_documento = ft.ElevatedButton(
        text="Seleccionar archivo",
        visible=False,
        on_click=lambda e: file_picker_documento.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf", "docx", "xlsx", "pptx"],
            initial_directory=os.path.abspath("archivos_input")
        )
    )
    def actualizar_switches(e):
        global enviar_imagen, enviar_documento
        enviar_imagen = switch_imagen.value
        enviar_documento = switch_documento.value

        # Imagen
        boton_imagen.visible = enviar_imagen
        contenedor_ruta_imagen.visible = enviar_imagen
        divider_imagen.visible = enviar_imagen
        imagen_preview.visible = enviar_imagen and ruta_imagen is not None


        # Archivo
        boton_documento.visible = enviar_documento
        contenedor_ruta_documento.visible = enviar_documento
        divider_documento.visible = enviar_documento

        page.update()


    switch_imagen.on_change = actualizar_switches
    switch_documento.on_change = actualizar_switches


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
        "get_driver": lambda: driver,
        "fila_switches": fila_switches,
        "boton_imagen": boton_imagen,
        "contenedor_ruta_imagen": contenedor_ruta_imagen,
        "boton_documento": boton_documento,
        "contenedor_ruta_documento": contenedor_ruta_documento,
        "get_multimedia_flags": lambda: (enviar_imagen, enviar_documento),
        "get_rutas_extra": lambda: (ruta_imagen, ruta_documento),
        "divider_imagen": divider_imagen,
        "divider_documento": divider_documento,
        "imagen_preview": imagen_preview

    }

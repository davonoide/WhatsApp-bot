import flet as ft
import os
from utils.lector_de_mensaje import leer_mensaje
from services.enviar_telefonos_service import enviar_mensaje_whatsapp
from utils.driver import abrir_navegador
from services.enviar_telefonos_service import enviar_mensaje_whatsapp_directo


# Variables globales
archivo_csv = None
archivo_txt = None
driver = None  # Guardará el navegador abierto
instrucciones = ft.Text("", size=16)

def ComponenteEnviarTelefonos(page: ft.Page):
    global archivo_csv, archivo_txt

    texto_ruta_csv = ft.Text("No se ha seleccionado archivo CSV.", size=14)
    texto_ruta_txt = ft.Text("No se ha seleccionado archivo TXT.", size=14)

    # --- FilePicker para CSV ---
    def seleccionar_archivo_csv(e: ft.FilePickerResultEvent):
        global archivo_csv
        if e.files:
            archivo_csv = e.files[0].path
            texto_ruta_csv.value = f"CSV seleccionado: {archivo_csv}"
        else:
            texto_ruta_csv.value = "No se seleccionó ningún archivo CSV."
        page.update()
        verificar_si_todo_listo()

    def al_enviar_click(e):
        print("🚀 Iniciando envío de mensajes...")
        enviar_mensaje_whatsapp(archivo_csv, archivo_txt)

    def iniciar_proceso(e):
        global driver
        boton_iniciar.disabled = True
        instrucciones.value = (
            "⚠️ IMPORTANTE ⚠️\n"
            "1. Escanea el código QR con WhatsApp Web\n"
            "2. Da clic en 'Enviar mensaje' para comenzar"
        )
        boton_confirmar_envio.visible = True
        page.update()

        driver = abrir_navegador()
        driver.get("https://web.whatsapp.com/")

    def enviar_click(e):
        instrucciones.value = "📨 Enviando mensajes..."
        boton_confirmar_envio.disabled = True
        page.update()

        try:
            enviar_mensaje_whatsapp_directo(archivo_csv, archivo_txt, driver)
            instrucciones.value = "✅ Mensajes enviados correctamente."
        except Exception as ex:
            instrucciones.value = f"❌ Ocurrió un error: {str(ex)}"
        finally:
            if driver:
                driver.quit()
            boton_iniciar.disabled = False
            boton_confirmar_envio.visible = False
            boton_confirmar_envio.disabled = False
            page.update()

    file_picker_csv = ft.FilePicker(on_result=seleccionar_archivo_csv)
    page.overlay.append(file_picker_csv)
    mensaje_contenido = ft.Text("", size=14, selectable=True, color=ft.Colors.WHITE)

    contenedor_mensaje = ft.Container(
        content=ft.Column(
            [mensaje_contenido],
            scroll=ft.ScrollMode.AUTO,
        ),
        height=300,
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),  # tono oscuro semitransparente
        border_radius=10,
        border=ft.border.all(1, ft.Colors.GREY_700),
    )

    contenedor_ruta_csv = ft.Container(
        content=texto_ruta_csv,
        #height=60,
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        border_radius=8,
        border=ft.border.all(1, ft.Colors.GREY_700),
    )

    contenedor_ruta_txt = ft.Container(
        content=texto_ruta_txt,
        #height=60,
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        border_radius=8,
        border=ft.border.all(1, ft.Colors.GREY_700),
    )

    boton_csv = ft.ElevatedButton(
        text="Seleccionar archivo CSV",
        on_click=lambda e: file_picker_csv.pick_files(
            allow_multiple=False,
            allowed_extensions=["csv"],
            initial_directory=os.path.abspath("archivos_input")
        )
    )  

    boton_iniciar = ft.ElevatedButton(
        text="Iniciar",
        disabled=True,
        icon=ft.Icons.START,
        on_click=iniciar_proceso
    )

    boton_confirmar_envio = ft.ElevatedButton(
        text="Enviar mensaje",
        icon=ft.Icons.SEND,
        visible=False,  # Oculto al principio
        disabled=False,
        on_click=enviar_click
    )
    # --- FilePicker para TXT ---
    def seleccionar_archivo_txt(e: ft.FilePickerResultEvent):
        global archivo_txt
        if e.files:
            archivo_txt = e.files[0].path
            texto_ruta_txt.value = f"TXT seleccionado: {archivo_txt}"
            contenido = leer_mensaje(archivo_txt)

            if contenido:
                mensaje_contenido.value = contenido
            else:
                mensaje_contenido.value = "⚠️ No se pudo leer el contenido del mensaje."
        else:
            texto_ruta_txt.value = "No se seleccionó ningún archivo TXT."
            mensaje_contenido.value = ""

        page.update()
        verificar_si_todo_listo()

    def verificar_si_todo_listo():
        if archivo_csv and archivo_txt:
            boton_iniciar.disabled = False
        else:
            boton_iniciar.disabled = True
        page.update()



    
    
    file_picker_txt = ft.FilePicker(on_result=seleccionar_archivo_txt)
    page.overlay.append(file_picker_txt)


    boton_txt = ft.ElevatedButton(
        text="Seleccionar archivo TXT",
        on_click=lambda e: file_picker_txt.pick_files(
            allow_multiple=False,
            allowed_extensions=["txt"],
            initial_directory=os.path.abspath("archivos_input")
        )
    )

    return ft.Column([
        ft.Text("Formulario para enviar a teléfonos 📱", size=20),

        ft.Text("1. Selecciona el archivo CSV:", size=16),
        boton_csv,
        contenedor_ruta_csv,

        ft.Divider(thickness=1, color=ft.Colors.GREY_800),

        ft.Text("2. Selecciona el archivo TXT:", size=16),
        boton_txt,
        contenedor_ruta_txt,

        ft.Divider(thickness=1, color=ft.Colors.GREY_800),

        ft.Text("Vista previa del mensaje:", size=16, weight=ft.FontWeight.BOLD),
        contenedor_mensaje,

        ft.Divider(thickness=1, color=ft.Colors.GREY_800),
        boton_iniciar,
        instrucciones,
        boton_confirmar_envio
    ])


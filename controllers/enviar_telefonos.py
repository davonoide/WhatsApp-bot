import flet as ft
from controllers.inputs_comunes import construir_seleccion_archivos
from services.enviar_telefonos_service import enviar_mensaje_whatsapp_directo
from utils.driver import abrir_navegador

def ComponenteEnviarTelefonos(page: ft.Page):
    componentes = construir_seleccion_archivos(page)

    def iniciar_click(e):
        driver = abrir_navegador()
        componentes["set_driver"](driver)
        driver.get("https://web.whatsapp.com/")
        componentes["instrucciones"].value = (
            "⚠️ IMPORTANTE ⚠️\n"
            "1. Escanea el código QR con WhatsApp Web\n"
            "2. Da clic en 'Enviar mensaje' para comenzar"
        )
        componentes["boton_confirmar_envio"].visible = True
        componentes["boton_iniciar"].disabled = True
        page.update()

    def enviar_click(e):
        componentes["instrucciones"].value = "📨 Enviando mensajes..."
        componentes["boton_confirmar_envio"].disabled = True
        page.update()

        archivo_csv, archivo_txt = componentes["get_archivos"]()
        driver = componentes["get_driver"]()

        try:
            enviar_mensaje_whatsapp_directo(archivo_csv, archivo_txt, driver)
            componentes["instrucciones"].value = "✅ Mensajes enviados correctamente."
        except Exception as ex:
            componentes["instrucciones"].value = f"❌ Error: {str(ex)}"
        finally:
            driver.quit()
            componentes["boton_iniciar"].disabled = False
            componentes["boton_confirmar_envio"].visible = False
            componentes["boton_confirmar_envio"].disabled = False
            page.update()

    # Asignar acciones a botones
    componentes["boton_iniciar"].on_click = iniciar_click
    componentes["boton_confirmar_envio"].on_click = enviar_click

    return ft.Column([
        ft.Text("Enviar a teléfonos", size=20),
        componentes["boton_csv"],
        componentes["contenedor_ruta_csv"],
        ft.Divider(),
        componentes["boton_txt"],
        componentes["contenedor_ruta_txt"],
        ft.Divider(),
        componentes["contenedor_mensaje"],
        ft.Divider(),
        componentes["boton_iniciar"],
        componentes["instrucciones"],
        componentes["boton_confirmar_envio"]
    ])

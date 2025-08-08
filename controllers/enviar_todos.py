import flet as ft
from controllers.inputs_comunes import construir_seleccion_archivos
from services.enviar_todos_service import enviar_mensajes_a_todos
from utils.driver import abrir_navegador

def ComponenteEnviarTodos(page: ft.Page):
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
        componentes["instrucciones"].value = "📨 Enviando mensajes a teléfonos y grupos..."
        componentes["boton_confirmar_envio"].disabled = True
        page.update()

        ruta_csv, ruta_txt = componentes["get_archivos"]()
        driver = componentes["get_driver"]()

        enviar_imagen, enviar_documento = componentes["get_multimedia_flags"]()
        ruta_imagen, ruta_documento = componentes["get_rutas_extra"]()

        try:
            enviar_mensajes_a_todos(
                ruta_csv,
                ruta_txt,
                driver,
                ruta_imagen if enviar_imagen else None,
                enviar_documento,
                ruta_documento if enviar_documento else None
            )
            componentes["instrucciones"].value = "✅ Mensajes enviados correctamente a teléfonos y grupos."
        except Exception as ex:
            componentes["instrucciones"].value = f"❌ Error: {str(ex)}"
        finally:
            driver.quit()
            componentes["boton_iniciar"].disabled = False
            componentes["boton_confirmar_envio"].visible = False
            componentes["boton_confirmar_envio"].disabled = False
            page.update()

    componentes["boton_iniciar"].on_click = iniciar_click
    componentes["boton_confirmar_envio"].on_click = enviar_click

    return ft.Column([
        ft.Text("Enviar a teléfonos y grupos", size=20),
        componentes["fila_switches"],
        ft.Divider(),

        componentes["boton_imagen"],
        componentes["contenedor_ruta_imagen"],
        componentes["imagen_preview"],
        componentes["divider_imagen"],

        componentes["boton_documento"],
        componentes["contenedor_ruta_documento"],
        componentes["divider_documento"],

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

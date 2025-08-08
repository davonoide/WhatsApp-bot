import flet as ft
from controllers.enviar_telefonos import ComponenteEnviarTelefonos
from controllers.enviar_grupos import ComponenteEnviarGrupos
from controllers.enviar_todos import ComponenteEnviarTodos

def main(page: ft.Page):
    page.title = "Interfaz Chatbot"
    page.scroll = ft.ScrollMode.AUTO
    page.window.height = 1280


    contenido_dinamico = ft.Column()

    def dropdown_changed(e):
        seleccion = dropdown.value
        contenido_dinamico.controls.clear()

        if seleccion == "Bot para enviar a telefonos":
            contenido_dinamico.controls.append(ComponenteEnviarTelefonos(page))
        elif seleccion == "Bot para enviar a grupos":
            contenido_dinamico.controls.append(ComponenteEnviarGrupos(page))
        elif seleccion == "Bot para enviar a telefonos y grupos":
            contenido_dinamico.controls.append(ComponenteEnviarTodos(page))
        else:
            contenido_dinamico.controls.append(ft.Text("Selecciona una opción"))

        page.update()

    dropdown = ft.Dropdown(
        label="Selecciona una acción del bot",
        options=[
            ft.dropdown.Option("Bot para enviar a telefonos"),
            ft.dropdown.Option("Bot para enviar a grupos"),
            ft.dropdown.Option("Bot para enviar a telefonos y grupos"),
        ],
        on_change=dropdown_changed,
        width=400
    )

    page.add(dropdown, contenido_dinamico)

ft.app(target=main)




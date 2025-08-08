# pip install selenium
from selenium import webdriver

# Submodulos
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# configuracion de ChromeDriver --pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager

# Para interactuar con la web
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException # Evita que el bot se trabe si tarda algo

import time # Para usar temporizador
import urllib.parse # Modifica URLs sin errores
import random
import pyperclip

import flet as ft
from controllers.enviar_telefonos import ComponenteEnviarTelefonos

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
            contenido_dinamico.controls.append(ft.Text("Formulario para enviar a grupos 👥"))
        elif seleccion == "Bot para enviar a telefonos y grupos":
            contenido_dinamico.controls.append(ft.Text("Formulario para ambos 🔀"))
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
        width=300
    )

    page.add(dropdown, contenido_dinamico)

ft.app(target=main)




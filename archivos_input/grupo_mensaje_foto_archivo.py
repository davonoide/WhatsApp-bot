from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip
import time
import os
import sys

# Configuración del navegador
service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)
browser.maximize_window()

browser.get("https://web.whatsapp.com/")

print("\n⚠️ IMPORTANTE ⚠️")
print("1. Escanea el código QR con WhatsApp Web")
input("2. Presiona Enter cuando estés listo...")

# Inputs
enviar_documento = True  # o False
ruta_documento = os.path.abspath("Grupos_mensaje.py")
grupos = ["Grupo 🥹🧌🧌 test", "Grupo test 1"]
mensaje = "Hola, este es un mensaje automático con archivo adjunto."
ruta_imagen = os.path.abspath("astrid.png")

for group in grupos:
    search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'

    search_box = WebDriverWait(browser, 500).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
    )

    search_box.clear()

    time.sleep(1)

    pyperclip.copy(group)

    search_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"

    time.sleep(2)

    group_xpath = f'//span[@title="{group}"]'
    group_title = browser.find_element(By.XPATH, group_xpath)

    group_title.click()

    time.sleep(1)

    # Esperar y hacer clic en botón "Adjuntar"
    attachment_btn = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, '//button[.//span[@data-icon="plus-rounded"]]'))
    )
    browser.execute_script("arguments[0].click();", attachment_btn)

    # Enviar archivo
    image_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
    )
    image_input.send_keys(ruta_imagen)
    time.sleep(1)

    # Esperar a que cargue el campo de comentario
    comentario_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @data-lexical-editor="true"]'))
    )

    # Escribir el mensaje dentro del comentario
    pyperclip.copy(mensaje)
    comentario_box.send_keys(Keys.SHIFT, Keys.INSERT)
    time.sleep(1)

    # Enviar imagen y comentario juntos
    send_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]//span[@data-icon="wds-ic-send-filled"]/ancestor::div[@role="button"]'))
    )
    browser.execute_script("arguments[0].click();", send_btn)
    time.sleep(2)

    if enviar_documento:
        # Hacer clic en el botón de clip otra vez
        attachment_btn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[.//span[@data-icon="plus-rounded"]]'))
        )
        browser.execute_script("arguments[0].click();", attachment_btn)
        time.sleep(1)

        # Buscar input de documentos (acepta cualquier archivo)
        doc_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@accept="*"]'))
        )
        doc_input.send_keys(ruta_documento)
        time.sleep(2)

        # Enviar documento (mismo botón)
        doc_send_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]//span[@data-icon="wds-ic-send-filled"]/ancestor::div[@role="button"]'))
        )
        browser.execute_script("arguments[0].click();", doc_send_btn)
        time.sleep(2)


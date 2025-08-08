
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

from utils.driver import abrir_navegador
from utils.validaciones import corregir_numero_cel

def enviar_mensaje_whatsapp_numero_individual(contactos,grupos,mensaje):

    print("Abriendo Navegador Chrome...")
    driver = abrir_navegador()
    try:
        driver.get("https://web.whatsapp.com/")
        print("\n⚠️ IMPORTANTE ⚠️")
        print("1. Escanea el código QR con WhatsApp Web")
        input("2. Presiona Enter cuando estés listo...")

        # Enviar a contactos individuales
        for numero in contactos:
            numero_correcto = corregir_numero_cel(numero)
            print(f"Enviando a contacto: {numero_correcto}")
            exito, mensaje_retorno = enviar_mensaje(driver, numero_correcto, mensaje)
            print(mensaje_retorno)
            time.sleep(random.uniform(4, 6))

        # Enviar a grupos
        for grupo in grupos:
            print(f"Enviando a grupo: {grupo}")
            exito, mensaje_retorno = enviar_mensaje_grupo(driver, grupo, mensaje)
            print(mensaje_retorno)
            time.sleep(random.uniform(4, 6))

    except Exception as e:
        print(f"⚠️ Hay un error! ⚠️ \n{str(e)}")

    finally:
        input("\nMensajes enviados. Presione Enter para cerrar")
        driver.quit()

def enviar_mensaje
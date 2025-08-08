from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip

import time

import urllib.parse  # Para codificar la URL del mensaje correctamente
import random  # Para hacer que los tiempos de espera sean aleatorios (simula comportamiento humano)

# Función para enviar un mensaje con imagen y opcionalmente un archivo adjunto a un grupo de WhatsApp
def grupos_enviar_mensaje_foto_archivo(browser, group, msn, ruta_imagen, enviar_documento, ruta_documento):
    try:
        # Esperar que aparezca el campo de búsqueda de chats
        if enviar_documento:
            print(f"-----Grupo: {group} en proceso, imagen con mensaje y archivo-----") 
        else: 
            print(f"-----Grupo: {group} en proceso, imagen con mensaje-----")
        print(f"Buscando grupo: {group} ...")
        search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
        search_box = WebDriverWait(browser, 500).until(
            EC.presence_of_element_located((By.XPATH, search_xpath))
        )

        # Limpiar el campo de búsqueda y pegar el nombre del grupo
        search_box.clear()
        time.sleep(1)
        pyperclip.copy(group)
        search_box.send_keys(Keys.SHIFT, Keys.INSERT)  # También podría usarse CTRL + V
        time.sleep(2)

        # Buscar y hacer clic en el grupo específico
        print(f"Seleccionando grupo {group} ...")
        group_xpath = f'//span[@title="{group}"]'
        group_title = browser.find_element(By.XPATH, group_xpath)
        group_title.click()
        time.sleep(1)

        # Esperar y hacer clic en el botón de adjuntar (clip)
        print(f"Preparando para djuntar imangen...")
        attachment_btn = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, '//button[.//span[@data-icon="plus-rounded"]]'))
        )
        browser.execute_script("arguments[0].click();", attachment_btn)

        # Buscar el input para subir imagen/video y enviar la imagen
        print(f"Adjuntanto imagen...")
        image_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
        )
        image_input.send_keys(ruta_imagen)
        time.sleep(1)

        # Esperar a que aparezca el campo de comentario de imagen
        print(f"Preparando mensaje...")
        comentario_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @data-lexical-editor="true"]'))
        )

        # Escribir el mensaje dentro del comentario
        pyperclip.copy(msn)
        comentario_box.send_keys(Keys.SHIFT, Keys.INSERT)
        print(f"Mensaje escrito.")
        time.sleep(random.uniform(1, 2))

        # Enviar imagen junto con el comentario
        print("Enviando imagen con mensaje...")
        send_btn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]//span[@data-icon="wds-ic-send-filled"]/ancestor::div[@role="button"]'))
        )
        browser.execute_script("arguments[0].click();", send_btn)
        time.sleep(random.uniform(2, 3.5))

        print("Imagen con mensaje enviados!!")

        # Si se especifica enviar un documento adicional
        if enviar_documento:
            # Volver a hacer clic en el botón de adjuntar (clip)
            print("Preparando para enviar archivo...")
            attachment_btn = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[.//span[@data-icon="plus-rounded"]]'))
            )
            browser.execute_script("arguments[0].click();", attachment_btn)
            time.sleep(1)

            # Buscar input para adjuntar cualquier tipo de archivo
            print("Cargando archivo...")
            doc_input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@accept="*"]'))
            )
            doc_input.send_keys(ruta_documento)
            print("Enviando archivo...")
            time.sleep(random.uniform(2, 3))
        
            # Enviar el documento adjunto (mismo botón de enviar)
            doc_send_btn = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]//span[@data-icon="wds-ic-send-filled"]/ancestor::div[@role="button"]'))
            )
            browser.execute_script("arguments[0].click();", doc_send_btn)
            print("Archivo enviado !!!")
            time.sleep(random.uniform(2, 4))
    except Exception as e:
        # Manejo de errores en caso de que algo falle (por ejemplo, número inválido)
        print(f"⚠️ Algo salio mal enviando el mensaje!  :( {str(e)}")
        return False, f"⚠️ Error al enviar mensaje: {str(e)}"

# Función para enviar solo mensajes de texto a un grupo de WhatsApp
def grupos_enviar_mensaje(browser, group, msn):
    try:
        # Espera hasta que esté disponible el cuadro de búsqueda de chats (campo de búsqueda superior)
        print(f"Buscando grupo: {group} ...")
        search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
        search_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, search_xpath))
        )

        # Limpia el cuadro de búsqueda para asegurarse de que esté vacío
        search_box.clear()
        time.sleep(1)

        # Copia el nombre del grupo al portapapeles y lo pega en el cuadro de búsqueda
        pyperclip.copy(group)
        search_box.send_keys(Keys.SHIFT, Keys.INSERT)  # También se puede usar Keys.CONTROL + "v"
        time.sleep(2)

        # Localiza el grupo en la lista de chats usando el nombre exacto del grupo
        print(f"Seleccionando grupo {group} ...")
        group_xpath = f'//span[@title="{group}"]'
        group_title = browser.find_element(By.XPATH, group_xpath)
        group_title.click()  # Abre el chat del grupo
        time.sleep(1)

        # Encuentra el campo donde se escribe el mensaje (parte inferior del chat)
        print(f"Enviando mensaje...")
        input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
        input_box = browser.find_element(By.XPATH, input_xpath)

        # Copia el mensaje al portapapeles, lo pega en el campo de texto y lo envía
        pyperclip.copy(msn)
        input_box.send_keys(Keys.SHIFT, Keys.INSERT)
        print(f"Mensaje escrito")
        input_box.send_keys(Keys.ENTER)
        print(f"Mensaje enviado!!")
        time.sleep(2)  # Espera para evitar errores antes de pasar al siguiente grupo

    except Exception as e:
        # Manejo de errores en caso de que algo falle (por ejemplo, número inválido)
        print(f"⚠️ Algo salio mal enviando el mensaje!  :( {str(e)}")
        return False, f"⚠️ Error al enviar mensaje: {str(e)}"

# Función para enviar mensaje, imagen y archivo a un número
def enviar_mensaje_con_multimedia(driver, numero, mensaje, ruta_imagen=None, enviar_documento=False, ruta_documento=None):
    try:
        mensaje_codificado = urllib.parse.quote(mensaje)
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensaje_codificado}"

        print(f"\nAbriendo chat con: {numero}")
        driver.get(url)

        # Esperar que cargue el botón de enviar mensaje
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Enviar']"))
        )
        time.sleep(random.uniform(3, 4))  # Simula comportamiento humano

        # Si no se va a enviar imagen ni documento, solo clic en enviar
        if not ruta_imagen and not enviar_documento:
            print("Enviando solo mensaje de texto...")
            driver.find_element(By.XPATH, "//button[@aria-label='Enviar']").click()
            time.sleep(random.uniform(2, 3))
            return True, "Mensaje de texto enviado"

        # Si hay imagen, hacer clic en botón de adjuntar
        print("Preparando para adjuntar imagen...")
        attachment_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//button[.//span[@data-icon="plus-rounded"]]'))
        )
        driver.execute_script("arguments[0].click();", attachment_btn)

        if ruta_imagen:
            print("Adjuntando imagen...")
            image_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
            )
            image_input.send_keys(ruta_imagen)
            time.sleep(1)

            # Escribir mensaje como comentario de la imagen
            comentario_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="textbox" and @data-lexical-editor="true"]'))
            )
            pyperclip.copy(mensaje)
            comentario_box.send_keys(Keys.SHIFT, Keys.INSERT)
            time.sleep(random.uniform(1, 2))

            # Enviar imagen con mensaje
            send_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]//span[@data-icon="wds-ic-send-filled"]/ancestor::div[@role="button"]'))
            )
            driver.execute_script("arguments[0].click();", send_btn)
            print("Imagen con mensaje enviada")
            time.sleep(random.uniform(2, 3))

        # Si se requiere enviar documento adicional
        if enviar_documento and ruta_documento:
            print("Adjuntando archivo...")
            attachment_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[.//span[@data-icon="plus-rounded"]]'))
            )
            driver.execute_script("arguments[0].click();", attachment_btn)
            time.sleep(1)

            doc_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@accept="*"]'))
            )
            doc_input.send_keys(ruta_documento)
            time.sleep(random.uniform(2, 3))

            doc_send_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button"]//span[@data-icon="wds-ic-send-filled"]/ancestor::div[@role="button"]'))
            )
            driver.execute_script("arguments[0].click();", doc_send_btn)
            print("Archivo enviado")
            time.sleep(random.uniform(2, 4))

        return True, "Mensaje con imagen y/o archivo enviado correctamente"

    except Exception as e:
        print(f"⚠️ Error al enviar al número {numero}: {str(e)}")
        return False, f"⚠️ Error: {str(e)}"

# Función que envía un mensaje de WhatsApp a un número dado
def enviar_mensaje_telefonos(driver, numero, mensaje):
    try:
        # Codifica el mensaje para que sea válido dentro de una URL
        mensaje_codificado = urllib.parse.quote(mensaje)
        # Construye la URL para abrir el chat con el número y mensaje prellenado
        url = f"https://web.whatsapp.com/send?phone={numero}&text={mensaje_codificado}"

        print(f"Abriendo conexion con: {numero}")
        driver.get(url)  # Abre la conversación en WhatsApp Web

        # Espera hasta que el botón de enviar esté disponible
        espera = WebDriverWait(driver, 20)
        boton_enviar = espera.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Enviar']"))
        )

        # Simula espera aleatoria para no parecer un bot (más natural)
        print("Preparando mensaje...")
        time.sleep(random.uniform(3, 4))

        # Hace clic en el botón de enviar
        print("Enviando mensaje...")
        boton_enviar.click()

        # Espera nuevamente para evitar conflictos en la interfaz
        print("Esperando confirmacion...")
        time.sleep(random.uniform(3, 4))
        
        return True, "Mensaje enviado!"
    
    except Exception as e:
        # Manejo de errores en caso de que algo falle (por ejemplo, número inválido)
        print(f"⚠️ Algo salio mal enviando el mensaje!  :( {str(e)}")
        return False, f"⚠️ Error al enviar mensaje: {str(e)}"

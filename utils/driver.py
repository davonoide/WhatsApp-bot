from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def abrir_navegador():
    opciones = Options()

    # Tamaño y configuración general del navegador
    opciones.add_argument("--window-size=1100,700")
    opciones.add_argument("--disable-notifications")
    opciones.add_argument("--disable-infobars")
    opciones.add_argument("--disable-extensions")
    opciones.add_argument("--start-maximized")

    # Inicializa el driver de Chrome
    servicio = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servicio, options=opciones)

    return driver
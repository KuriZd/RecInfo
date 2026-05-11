from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

URL = "https://sim.morelia.tecnm.mx/encuestas/evaluacion-docente"

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get(URL)

input("Inicia sesión y avanza hasta la encuesta. Luego presiona ENTER aquí...")

while True:
    selects = driver.find_elements(By.TAG_NAME, "select")

    pendientes = 0
    respondidos = 0

    for select_element in selects:
        selected_option = select_element.find_element(By.CSS_SELECTOR, "option:checked").text.strip()

        if selected_option.lower() == "sin evaluar":
            pendientes += 1

            valor = str(random.choice([4, 5]))

            selector = Select(select_element)

            try:
                selector.select_by_value(valor)

                time.sleep(random.uniform(0.1, 0.3))

                respondidos += 1
                print(f"  ✔ Campo '{select_element.get_attribute('name')}' → valor {valor} seleccionado")

            except Exception as e:
                print(f"  ✘ No se pudo seleccionar el campo '{select_element.get_attribute('name')}': {e}")

    print(f"\nResumen: {respondidos} campos respondidos / {pendientes} estaban pendientes.")

    # Verificar si quedó alguno sin responder
    selects_restantes = driver.find_elements(By.TAG_NAME, "select")
    aun_pendientes = sum(
        1 for s in selects_restantes
        if s.find_element(By.CSS_SELECTOR, "option:checked").text.strip().lower() == "sin evaluar"
    )

    if aun_pendientes == 0:
        print("✅ Todos los campos respondidos. Puedes presionar 'Siguiente' manualmente.")
    else:
        print(f"⚠️  Aún quedan {aun_pendientes} campos sin responder.")

    continuar = input("\nPresiona ENTER para volver a revisar, o escribe 'salir': ")

    if continuar.lower() == "salir":
        break

driver.quit()
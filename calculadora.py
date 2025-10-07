from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from datetime import datetime

# Crear carpetas para guardar pantallazos y errores
os.makedirs("pantallazos", exist_ok=True)
os.makedirs("errorCalculadora", exist_ok=True)

# Función para generar nombre único de error
def nombre_error(caso_num):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"errores/error_caso{caso_num}_{timestamp}.txt"

# Iniciar el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) 

# Abrir la página
driver.get("https://testsheepnz.github.io/minimum-viable-calculator.html")
time.sleep(5)

# Capturar los elementos del formulario
number1_input = driver.find_element(By.ID, "number1Field")
number2_input = driver.find_element(By.ID, "number2Field")

# Casos de prueba
casos_de_prueba = [
    ("--1", "--2"),
    ("110", "-53"),
    ("abc", "234"),
    ("", "11"),
    ("22", ""),
    ("!!","][]*"),
    ("98.5","1,9"),
    ("98.5","1.9"),
    ("98.a5","*"),
    (" "," "),
    ("","9.765"),
    ("999999999393939393939393939393993","9000000023020302300230230203"),
    ("-17","-983"),
    ("-23","983")
]

for i, caso in enumerate(casos_de_prueba, start=1):
    
    numero1, numero2 = caso

    number1_input.clear()
    number2_input.clear()

    number1_input.send_keys(numero1)
    number2_input.send_keys(numero2)

    # Clic en el botón
    calculate_button = driver.find_element(By.ID, "calculateButton")
    calculate_button.click()
    time.sleep(3)

    print(f"\n🔍 Caso de prueba #{i}: ({numero1}, {numero2})")
    
    try:
        error_label = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "errorMsgField"))
        )
        error_text = error_label.text.strip()

        if error_text:
            print("❌ Error en el cálculo:", error_text)

            # Guardar error en archivo .txt
            ruta_error = nombre_error(i)
            with open(ruta_error, "w", encoding="utf-8") as f:
                f.write(f"Caso de prueba #{i}\n")
                f.write(f"Valores: ({numero1}, {numero2})\n")
                f.write(f"Mensaje de error: {error_text}\n")
            print(f"📝 Error guardado en: {ruta_error}")

        else:
            result_input = driver.find_element(By.ID, "numberAnswerField")
            print("✅ Cálculo exitoso, resultado = ", result_input.get_attribute("value"))

    except Exception as e:
        print("⚠️ No se pudo validar el resultado:", str(e))
    
    # Tomar pantallazo del caso de prueba
    screenshot_path = f"pantallazos/caso_{i}.png"
    driver.save_screenshot(screenshot_path)
    print(f"📸 Pantallazo guardado en: {screenshot_path}")

    time.sleep(2)

# Cerrar navegador
driver.quit()

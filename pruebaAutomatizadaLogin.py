from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from datetime import datetime

# Crear carpetas para pantallazos y errores
os.makedirs("pantallazos_login", exist_ok=True)
os.makedirs("errores_login", exist_ok=True)

# Función para generar nombre único de pantallazo
def nombre_pantallazo(caso):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"pantallazos_login/{caso}_{timestamp}.png"

# Función para generar nombre único de archivo de error
def nombre_error(caso):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"errores{caso}_{timestamp}.txt"

# Iniciar navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://the-internet.herokuapp.com/login")

# Casos de prueba: (usuario, contraseña, nombre_caso)
casos_login = [
    ("tomsmith", "SuperSecretPassword!", "login_exitoso"),
    #("tomsmith", "wrongPassword", "usuario_correcto_pass_incorrecta"),
    #("wrongUser", "SuperSecretPassword!", "usuario_incorrecto_pass_correcta"),
    #("", "", "campos_vacios"),("#==[]", "][*["Q"]]", "caracteres_especiales")
]

for usuario, password, nombre_caso in casos_login:
    # Esperar los campos antes de usarlos
    user_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    pass_input = driver.find_element(By.ID, "password")

    # Limpiar y enviar valores
    user_input.clear()
    pass_input.clear()
    user_input.send_keys(usuario)
    pass_input.send_keys(password)

    # Hacer clic en login
    login_button = driver.find_element(By.CSS_SELECTOR, "button.radius")
    login_button.click()

    # Esperar resultado
    try:
        mensaje = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "flash"))
        ).text.strip()

        print(f"\n🔍 Caso: {nombre_caso}")
        print("📢 Mensaje mostrado:", mensaje)

        # Guardar errores en TXT si no es exitoso
        if "You logged into a secure area!" not in mensaje:
            ruta_error = nombre_error(nombre_caso)
            with open(ruta_error, "w", encoding="utf-8") as f:
                f.write(f"Caso: {nombre_caso}\n")
                f.write(f"Usuario: {usuario}\n")
                f.write(f"Contraseña: {password}\n")
                f.write(f"Mensaje de error: {mensaje}\n")
            print(f"📝 Error guardado en: {ruta_error}")

    except Exception as e:
        print(f"\n⚠️ Caso {nombre_caso}: No se encontró mensaje ({str(e)})")

    # Tomar pantallazo único
    path = nombre_pantallazo(nombre_caso)
    driver.save_screenshot(path)
    print(f"📸 Pantallazo guardado en: {path}")

    time.sleep(5)

# Cerrar navegador
driver.quit()

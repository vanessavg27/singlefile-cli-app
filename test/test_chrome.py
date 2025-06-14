#!/usr/bin/env python3
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

print("DEBUG: Iniciando test_chrome.py", flush=True)

try:
    # Aquí se intenta descargar/verificar y obtener la ruta de ChromeDriver
    print("DEBUG: Intentando instalar/obtener ChromeDriver...", flush=True)
    
    # Primero vamos a ver qué versión de Chrome tienes instalada
    print("DEBUG: Verificando instalación de Chrome...", flush=True)
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    if os.path.exists(chrome_path):
        print(f"DEBUG: Chrome encontrado en: {chrome_path}", flush=True)
    else:
        print(f"DEBUG: ⚠️ Chrome NO encontrado en: {chrome_path}", flush=True)
        # Verificar ubicaciones alternativas
        alt_paths = [
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
        ]
        for alt_path in alt_paths:
            if os.path.exists(alt_path):
                print(f"DEBUG: Chrome encontrado en ubicación alternativa: {alt_path}", flush=True)
                chrome_path = alt_path
                break
        else:
            print("DEBUG: ❌ No se encontró Chrome en ninguna ubicación estándar")
    
    # Intentar obtener ChromeDriver
    service = Service(ChromeDriverManager().install())
    print(f"DEBUG: ChromeDriver obtenido en: {service.path}", flush=True)
    
    # Verificar que el archivo ChromeDriver existe y es ejecutable
    if os.path.exists(service.path):
        print(f"DEBUG: ✅ ChromeDriver existe en: {service.path}", flush=True)
        print(f"DEBUG: Tamaño del archivo: {os.path.getsize(service.path)} bytes", flush=True)
        
        # Verificar permisos
        if os.access(service.path, os.R_OK):
            print("DEBUG: ✅ ChromeDriver tiene permisos de lectura", flush=True)
        else:
            print("DEBUG: ❌ ChromeDriver NO tiene permisos de lectura", flush=True)
            
        if os.access(service.path, os.X_OK):
            print("DEBUG: ✅ ChromeDriver tiene permisos de ejecución", flush=True)
        else:
            print("DEBUG: ❌ ChromeDriver NO tiene permisos de ejecución", flush=True)
    else:
        print(f"DEBUG: ❌ ChromeDriver NO existe en: {service.path}", flush=True)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Lo ponemos en headless para que no abra una ventana
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Vamos a probar sin el perfil personalizado primero
    print("DEBUG: Intentando iniciar webdriver.Chrome SIN perfil personalizado...", flush=True)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("DEBUG: ✅ WebDriver de Chrome iniciado con éxito (sin perfil personalizado).", flush=True)

    driver.get("https://www.google.com")
    print(f"DEBUG: Título de la página: {driver.title}", flush=True)

    driver.quit()
    print("DEBUG: ✅ WebDriver de Chrome cerrado con éxito.", flush=True)

    # Si llegamos aquí, el problema podría estar en el perfil personalizado
    print("\n" + "="*50)
    print("DEBUG: Ahora probando CON perfil personalizado...")
    print("="*50)
    
    # Configuración de perfil como en tu código original
    from pathlib import Path
    chrome_profile_path = str(Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data")
    chrome_profile_name = "Default"
    
    print(f"DEBUG: Ruta del perfil: {chrome_profile_path}", flush=True)
    print(f"DEBUG: Nombre del perfil: {chrome_profile_name}", flush=True)
    
    if os.path.exists(chrome_profile_path):
        print("DEBUG: ✅ Directorio del perfil de Chrome existe", flush=True)
    else:
        print("DEBUG: ❌ Directorio del perfil de Chrome NO existe", flush=True)
    
    chrome_options_with_profile = Options()
    chrome_options_with_profile.add_argument("--headless=new")
    chrome_options_with_profile.add_argument("--disable-gpu")
    chrome_options_with_profile.add_argument("--no-sandbox")
    chrome_options_with_profile.add_argument("--disable-dev-shm-usage")
    chrome_options_with_profile.add_argument("--window-size=1920,1080")
    chrome_options_with_profile.add_argument(f"--user-data-dir={chrome_profile_path}")
    chrome_options_with_profile.add_argument(f"--profile-directory={chrome_profile_name}")
    
    print("DEBUG: Intentando iniciar webdriver.Chrome CON perfil personalizado...", flush=True)
    driver_with_profile = webdriver.Chrome(service=service, options=chrome_options_with_profile)
    print("DEBUG: ✅ WebDriver de Chrome con perfil iniciado con éxito.", flush=True)

    driver_with_profile.get("https://www.google.com")
    print(f"DEBUG: Título de la página (con perfil): {driver_with_profile.title}", flush=True)

    driver_with_profile.quit()
    print("DEBUG: ✅ WebDriver de Chrome con perfil cerrado con éxito.", flush=True)

except Exception as e:
    print(f"❌ ERROR: Fallo en test_chrome.py: {type(e).__name__}: {e}", flush=True)
    import traceback
    traceback.print_exc()

print("DEBUG: test_chrome.py finalizado.", flush=True)
#!/usr/bin/env python3
import os
import glob
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

print("DEBUG: Iniciando fix_chromedriver.py", flush=True)

try:
    # Primero, vamos a ver qué está devolviendo webdriver_manager
    print("DEBUG: Obteniendo ruta de webdriver_manager...", flush=True)
    wrong_path = ChromeDriverManager().install()
    print(f"DEBUG: webdriver_manager devuelve: {wrong_path}", flush=True)
    
    # Extraer el directorio padre donde debería estar el chromedriver.exe real
    wrong_dir = os.path.dirname(wrong_path)
    print(f"DEBUG: Directorio del ChromeDriver: {wrong_dir}", flush=True)
    
    # Listar todos los archivos en ese directorio
    print("DEBUG: Archivos en el directorio del ChromeDriver:", flush=True)
    if os.path.exists(wrong_dir):
        for file in os.listdir(wrong_dir):
            file_path = os.path.join(wrong_dir, file)
            size = os.path.getsize(file_path) if os.path.isfile(file_path) else "DIR"
            print(f"  - {file} ({size} bytes)", flush=True)
    
    # Buscar el archivo chromedriver.exe real
    chromedriver_exe = None
    possible_names = ["chromedriver.exe", "chromedriver"]
    
    for name in possible_names:
        candidate = os.path.join(wrong_dir, name)
        if os.path.exists(candidate):
            print(f"DEBUG: ✅ Encontrado {name} en: {candidate}", flush=True)
            chromedriver_exe = candidate
            break
    
    if not chromedriver_exe:
        # Buscar recursivamente en subdirectorios
        print("DEBUG: Buscando chromedriver.exe recursivamente...", flush=True)
        base_dir = os.path.dirname(wrong_dir)  # Subir un nivel
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file in possible_names:
                    candidate = os.path.join(root, file)
                    print(f"DEBUG: ✅ Encontrado {file} en: {candidate}", flush=True)
                    chromedriver_exe = candidate
                    break
            if chromedriver_exe:
                break
    
    if not chromedriver_exe:
        print("DEBUG: ❌ No se pudo encontrar chromedriver.exe", flush=True)
        raise FileNotFoundError("No se encontró chromedriver.exe")
    
    print(f"DEBUG: Usando ChromeDriver en: {chromedriver_exe}", flush=True)
    
    # Verificar que sea un ejecutable válido
    if os.path.exists(chromedriver_exe):
        size = os.path.getsize(chromedriver_exe)
        print(f"DEBUG: Tamaño del archivo chromedriver.exe: {size} bytes", flush=True)
        
        # Un chromedriver.exe típico tiene varios MB, no unos pocos KB
        if size < 1000000:  # Menos de 1MB es sospechoso
            print(f"DEBUG: ⚠️ Advertencia: El archivo chromedriver.exe parece muy pequeño ({size} bytes)")
        else:
            print("DEBUG: ✅ El tamaño del archivo parece correcto")
    
    # Ahora probemos con la ruta correcta
    service = Service(chromedriver_exe)
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    print("DEBUG: Intentando iniciar WebDriver con la ruta corregida...", flush=True)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("DEBUG: ✅ WebDriver iniciado con éxito!", flush=True)
    
    driver.get("https://www.google.com")
    print(f"DEBUG: Título de la página: {driver.title}", flush=True)
    
    driver.quit()
    print("DEBUG: ✅ WebDriver cerrado con éxito.", flush=True)
    
    # Guardar la ruta correcta para usar en el código principal
    print(f"\n{'='*60}")
    print("🎉 SOLUCIÓN ENCONTRADA:")
    print(f"Usar esta ruta en tu código: {chromedriver_exe}")
    print(f"{'='*60}")

except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}", flush=True)
    import traceback
    traceback.print_exc()

print("DEBUG: fix_chromedriver.py finalizado.", flush=True)
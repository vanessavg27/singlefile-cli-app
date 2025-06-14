#!/usr/bin/env python3
import os
import subprocess
import tempfile
import time
from datetime import datetime

def test_singlefile_and_save():
    """
    Versión que GUARDA el archivo descargado en lugar de eliminarlo
    """
    print("🔧 Probando SingleFile y guardando el archivo...", flush=True)
    
    # URL de prueba
    test_url = "https://github.com/gildas-lormeau/single-file-cli/issues/163"
    
    # Crear nombre de archivo permanente en el directorio actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"github_issue_163_{timestamp}.html"
    output_path = os.path.join(os.getcwd(), output_filename)
    
    print(f"📄 URL: {test_url}")
    print(f"📁 Guardando en: {output_path}")
    
    singlefile_exe_path = "D:\\scripts\\scripts-github-projects\\singlefile-cli-app\\single-file.exe"
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    
    # Usar la configuración que sabemos que funciona
    cmd = [
        singlefile_exe_path,
        test_url,
        output_path,
        "--browser-wait-delay=8000"
    ]
    
    print(f"🚀 Ejecutando comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=180,
            text=True
        )
        
        print(f"📊 Código de retorno: {result.returncode}")
        
        if result.stderr:
            print(f"⚠️ Stderr: {result.stderr[:200]}")
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"📏 Tamaño del archivo: {file_size} bytes")
            
            if file_size > 1000:
                print("✅ ¡ARCHIVO DESCARGADO Y GUARDADO EXITOSAMENTE!")
                print(f"📁 Ubicación: {output_path}")
                
                # Mostrar información del contenido
                try:
                    with open(output_path, 'r', encoding='utf-8') as f:
                        content = f.read(1000)
                        
                        if '<title>' in content.lower():
                            start = content.lower().find('<title>') + 7
                            end = content.lower().find('</title>')
                            if end > start:
                                title = content[start:end].strip()
                                print(f"📋 Título de la página: {title}")
                        
                        if 'github' in content.lower():
                            print("✅ Contenido de GitHub confirmado")
                        if 'issue' in content.lower():
                            print("✅ Contenido de issue confirmado")
                
                except Exception as e:
                    print(f"⚠️ Error leyendo contenido: {e}")
                
                # Instrucciones para el usuario
                print("\n" + "="*60)
                print(f"🎉 ARCHIVO GUARDADO EXITOSAMENTE")
                print(f"📍 Ubicación: {output_path}")
                print(f"💡 Puedes abrir el archivo con cualquier navegador")
                print("="*60)
                
                return True
            else:
                print("❌ Archivo muy pequeño o vacío")
                return False
        else:
            print("❌ Archivo no fue creado")
            return False
            
    except subprocess.TimeoutExpired:
        print("⌛ Timeout - comando tardó más de 3 minutos")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def download_and_save_github_url(url, custom_filename=None):
    """
    Función para descargar cualquier URL de GitHub y guardarla
    """
    print(f"🌐 Descargando: {url}")
    
    # Generar nombre de archivo
    if custom_filename:
        output_filename = custom_filename
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Extraer parte de la URL para el nombre
        url_part = url.replace("https://github.com/", "").replace("/", "_")
        if len(url_part) > 50:
            url_part = url_part[:50]
        output_filename = f"github_{url_part}_{timestamp}.html"
    
    output_path = os.path.join(os.getcwd(), output_filename)
    
    singlefile_exe_path = "D:\\scripts\\scripts-github-projects\\singlefile-cli-app\\single-file.exe"
    
    cmd = [
        singlefile_exe_path,
        url,
        output_path,
        "--browser-wait-delay=8000"
    ]
    
    try:
        print(f"🚀 Descargando...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            file_size = os.path.getsize(output_path)
            print(f"✅ Descarga exitosa: {file_size} bytes")
            print(f"📁 Guardado en: {output_path}")
            return output_path
        else:
            print(f"❌ Error en descarga. Código: {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Probar descarga y guardado
    success = test_singlefile_and_save()
    
    if success:
        print("\n🔥 ¡Todo funcionando correctamente!")
        print("💡 Ahora puedes usar la función download_and_save_github_url() para otras URLs")
    else:
        print("\n❌ Hubo un problema con la descarga")
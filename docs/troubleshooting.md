# 🔧 Guía de Solución de Problemas

Esta guía te ayudará a resolver los problemas más comunes que puedes encontrar al usar GitHub Offline Downloader.

## 📋 Diagnóstico Rápido

Antes de comenzar, ejecuta estos comandos para obtener información del sistema:

```bash
# Información del sistema
python --version
google-chrome --version  # o chromium --version
pip list | grep selenium

# Ejecutar diagnósticos automáticos
python test/test_chrome.py
python test/test_singlefile.py
```

## 🚫 Problemas de Instalación

### ❌ "Python no encontrado" o "python no se reconoce como comando"

**Síntomas:**
```
'python' no se reconoce como un comando interno o externo
python: command not found
```

**Soluciones:**

<details>
<summary><strong>Windows</strong></summary>

1. **Verificar instalación de Python:**
   ```cmd
   py --version
   python3 --version
   ```

2. **Reinstalar Python:**
   - Descargar desde [python.org](https://python.org/downloads/)
   - ⚠️ **IMPORTANTE:** Marcar "Add Python to PATH"
   - Elegir "Install for all users"

3. **Reparar PATH manualmente:**
   ```cmd
   # Agregar a PATH del sistema
   set PATH=%PATH%;C:\Python39;C:\Python39\Scripts
   
   # O abrir "Variables de entorno" y agregar:
   C:\Users\TuUsuario\AppData\Local\Programs\Python\Python39\
   C:\Users\TuUsuario\AppData\Local\Programs\Python\Python39\Scripts\
   ```

4. **Usar py launcher:**
   ```cmd
   py -m pip install --upgrade pip
   py run.py https://github.com/usuario/repo
   ```

</details>

<details>
<summary><strong>Linux</strong></summary>

1. **Instalar Python 3.8+:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   
   # CentOS/RHEL
   sudo dnf install python3 python3-pip
   
   # Arch Linux
   sudo pacman -S python python-pip
   ```

2. **Crear alias si es necesario:**
   ```bash
   echo 'alias python=python3' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Verificar versión:**
   ```bash
   python3 --version
   which python3
   ```

</details>

<details>
<summary><strong>macOS</strong></summary>

1. **Instalar con Homebrew:**
   ```bash
   # Instalar Homebrew si no lo tienes
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Instalar Python
   brew install python3
   ```

2. **Verificar instalación:**
   ```bash
   python3 --version
   which python3
   ```

3. **Usar Python del sistema (último recurso):**
   ```bash
   /usr/bin/python3 --version
   ```

</details>

### ❌ "Chrome no se puede iniciar" o "ChromeDriver no funciona"

**Síntomas:**
```
selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start
Message: 'chromedriver' executable needs to be in PATH
DevToolsActivePort file doesn't exist
```

**Soluciones:**

<details>
<summary><strong>1. Verificar instalación de Chrome</strong></summary>

**Windows:**
```cmd
# Verificar que Chrome esté instalado
dir "C:\Program Files\Google\Chrome\Application\chrome.exe"
dir "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

# Si no está instalado, descargar desde:
# https://chrome.google.com/
```

**Linux:**
```bash
# Verificar Chrome/Chromium
which google-chrome
which chromium-browser

# Instalar Chrome si no está
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt update
sudo apt install google-chrome-stable

# O instalar Chromium
sudo apt install chromium-browser
```

**macOS:**
```bash
# Verificar Chrome
ls -la "/Applications/Google Chrome.app"

# Instalar con Homebrew
brew install --cask google-chrome
```

</details>

<details>
<summary><strong>2. Cerrar instancias de Chrome</strong></summary>

```bash
# Linux/macOS
pkill -f chrome
pkill -f chromium

# Windows (PowerShell como administrador)
taskkill /f /im chrome.exe
taskkill /f /im chromedriver.exe
```

</details>

<details>
<summary><strong>3. Reparar ChromeDriver</strong></summary>

```bash
# Ejecutar script de reparación
python test/fix_chromedriver.py

# Eliminar ChromeDriver corrupto
rm -rf ~/.cache/selenium  # Linux/macOS
rmdir /s %USERPROFILE%\.cache\selenium  # Windows

# Forzar descarga nueva
python -c "
from webdriver_manager.chrome import ChromeDriverManager
ChromeDriverManager().install()
"
```

</details>

<details>
<summary><strong>4. Usar perfil temporal</strong></summary>

```bash
# Evitar conflictos con perfiles existentes
python run.py https://github.com/usuario/repo --profile temporal
```

</details>

### ❌ "Permission denied" o "No se pueden escribir archivos"

**Síntomas:**
```
PermissionError: [Errno 13] Permission denied
OSError: [Errno 13] Permission denied: '/path/to/file'
```

**Soluciones:**

<details>
<summary><strong>Windows</strong></summary>

1. **Ejecutar como administrador:**
   - Clic derecho en cmd/PowerShell → "Ejecutar como administrador"
   - O ejecutar el script desde un prompt elevado

2. **Verificar permisos del directorio:**
   ```cmd
   # Dar permisos completos al directorio
   icacls "C:\Users\%USERNAME%\Downloads" /grant "%USERNAME%":F /T
   
   # Cambiar directorio de instalación
   set INSTALL_DIR=C:\GitHub-Offline-Downloader
   mkdir %INSTALL_DIR%
   cd %INSTALL_DIR%
   ```

3. **Desactivar Windows Defender temporalmente:**
   - Windows Security → Virus & threat protection
   - Manage settings → Real-time protection OFF

</details>

<details>
<summary><strong>Linux/macOS</strong></summary>

1. **Verificar permisos:**
   ```bash
   ls -la ~/Downloads/
   ls -la .
   
   # Dar permisos de escritura
   chmod 755 ~/Downloads
   chmod +x *.sh
   ```

2. **Cambiar propietario si es necesario:**
   ```bash
   sudo chown -R $USER:$USER ~/GitHub-Offline-Downloader
   ```

3. **Verificar espacio en disco:**
   ```bash
   df -h ~
   du -sh ~/Downloads/github-offline/
   ```

</details>

## 🌐 Problemas de Descarga

### ❌ "Archivos HTML vacíos" o "Archivos muy pequeños"

**Síntomas:**
- Archivos de menos de 1KB
- Contenido "Access Denied" o páginas de error
- Archivos con solo estructura HTML básica

**Causas y Soluciones:**

<details>
<summary><strong>1. Repositorio privado sin acceso</strong></summary>

```bash
# Usar perfil con sesión activa de GitHub
python run.py https://github.com/empresa/repo-privado --profile "Tu-Perfil-GitHub"

# Verificar acceso manual
# 1. Abrir Chrome con tu perfil
# 2. Navegar al repositorio manualmente
# 3. Verificar que puedes acceder
```

</details>

<details>
<summary><strong>2. Rate limiting de GitHub</strong></summary>

```bash
# Aumentar delay entre requests
python run.py URL --delay 10

# Usar modo headless para evitar detección
python run.py URL --headless --delay 15

# Usar perfil temporal sin historial
python run.py URL --profile temporal --delay 20
```

</details>

<details>
<summary><strong>3. Problemas con SingleFile</strong></summary>

```bash
# Probar SingleFile manualmente
python test/test_singlefile.py

# Reinstalar SingleFile CLI (si tienes Node.js)
npm uninstall -g single-file-cli
npm install -g single-file-cli

# Verificar configuración
single-file --help

# Usar configuración alternativa
python run.py URL --browser-wait-delay=15000
```

</details>

<details>
<summary><strong>4. Problemas de red</strong></summary>

```bash
# Verificar conectividad
ping github.com
curl -I https://github.com

# Usar proxy si es necesario
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port

# Configurar timeout más alto
# Editar src/config.py:
# PAGE_LOAD_TIMEOUT = 60
```

</details>

### ❌ "SingleFile no funciona" o "Comando no encontrado"

**Síntomas:**
```
single-file: command not found
Error ejecutando SingleFile
SingleFile failed with exit code 1
```

**Soluciones:**

<details>
<summary><strong>1. Verificar Node.js (Método Recomendado)</strong></summary>

```bash
# Verificar Node.js
node --version
npm --version

# Instalar Node.js si no está
# Windows: https://nodejs.org/
# Linux: sudo apt install nodejs npm
# macOS: brew install node

# Instalar SingleFile CLI
npm install -g single-file-cli

# Verificar instalación
single-file --help
```

</details>

<details>
<summary><strong>2. Usar descarga automática (Fallback)</strong></summary>

```bash
# Eliminar SingleFile existente (Windows)
del single-file.exe

# Eliminar configuración (Linux/macOS)
rm -f /usr/local/bin/single-file

# Permitir descarga automática
# SingleFile se descargará en la primera ejecución
python run.py URL
```

</details>

<details>
<summary><strong>3. Configuración manual de ruta</strong></summary>

```python
# Editar src/config.py
class Config:
    SINGLEFILE_PATH = "/usr/local/bin/single-file"  # Linux/macOS
    # SINGLEFILE_PATH = "C:\\path\\to\\single-file.exe"  # Windows
```

</details>

## 🔗 Problemas de Enlaces y Navegación

### ❌ "Enlaces rotos en navegación offline"

**Síntomas:**
- Enlaces que llevan a "404 Not Found"
- Navegación que no funciona entre páginas
- Issues individuales no accesibles

**Soluciones:**

<details>
<summary><strong>1. Regenerar navegación</strong></summary>

```python
# Ejecutar reescritura de enlaces manualmente
python -c "
from src.link_rewriter import OfflineLinkRewriter
from src.github_parser import GitHubParser

repo_info = GitHubParser.parse_repo_url('https://github.com/usuario/repo')
rewriter = OfflineLinkRewriter('/ruta/a/descarga', repo_info)
rewriter.rewrite_all_links()
"
```

</details>

<details>
<summary><strong>2. Verificar estructura de archivos</strong></summary>

```bash
# Verificar que todos los directorios existen
ls -la downloads/github-offline/usuario_repo-offline/
ls -la downloads/github-offline/usuario_repo-offline/issues/
ls -la downloads/github-offline/usuario_repo-offline/issues/open/individual/

# Regenerar índices si faltan
python -c "
from src.offline_navigator import OfflineNavigator
OfflineNavigator.generate_navigation_index('repo-name', {}, '/ruta/descarga')
"
```

</details>

<details>
<summary><strong>3. Reparar enlaces manualmente</strong></summary>

```bash
# Crear script de reparación
cat > fix_links.py << 'EOF'
import os
from pathlib import Path
from src.link_rewriter import OfflineLinkRewriter
from src.github_parser import GitHubParser

# Configurar
repo_url = "https://github.com/usuario/repo"
download_path = "downloads/github-offline/usuario_repo-offline"

# Reparar
repo_info = GitHubParser.parse_repo_url(repo_url)
rewriter = OfflineLinkRewriter(download_path, repo_info)
files, links = rewriter.rewrite_all_links()

print(f"Reparados {links} enlaces en {files} archivos")
EOF

python fix_links.py
```

</details>

## 💾 Problemas de Rendimiento

### ❌ "Descarga muy lenta" o "Timeout errors"

**Síntomas:**
- Cada página tarda más de 30 segundos
- Errores de timeout frecuentes
- Proceso se congela

**Soluciones:**

<details>
<summary><strong>1. Ajustar configuración de velocidad</strong></summary>

```bash
# Aumentar delays
python run.py URL --delay 10

# Configurar timeouts más altos
# Editar src/config.py:
# PAGE_LOAD_TIMEOUT = 90
# DOWNLOAD_DELAY = 8
```

</details>

<details>
<summary><strong>2. Usar modo headless optimizado</strong></summary>

```bash
# Modo headless consume menos recursos
python run.py URL --headless --delay 5

# Optimizar Chrome
# En src/github_offline.py, añadir:
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")
chrome_options.add_argument("--disable-plugins")
```

</details>

<details>
<summary><strong>3. Monitorear recursos del sistema</strong></summary>

```bash
# Linux/macOS
top -p $(pgrep -f python)
ps aux | grep chrome

# Windows
tasklist | findstr python
tasklist | findstr chrome
```

</details>

## 🐛 Problemas Específicos por Sistema

### Windows Específicos

<details>
<summary><strong>"Windows Defender bloquea el script"</strong></summary>

1. **Añadir exclusión:**
   - Windows Security → Virus & threat protection
   - Manage settings → Add or remove exclusions
   - Añadir carpeta: `C:\Users\TuUsuario\GitHub-Offline-Downloader`

2. **Desactivar SmartScreen temporalmente:**
   - Windows Security → App & browser control
   - Reputation-based protection settings → OFF

</details>

<details>
<summary><strong>"PowerShell execution policy error"</strong></summary>

```powershell
# Cambiar política de ejecución temporalmente
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Ejecutar script
.\setup.bat

# Restaurar política
Set-ExecutionPolicy -ExecutionPolicy Default -Scope CurrentUser
```

</details>

### Linux Específicos

<details>
<summary><strong>"Display environment variable not set"</strong></summary>

```bash
# Para servidores sin GUI
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &

# O usar modo headless siempre
python run.py URL --headless
```

</details>

<details>
<summary><strong>"libgconf-2.so.4: No such file"</strong></summary>

```bash
# Ubuntu/Debian
sudo apt install libgconf-2-4

# CentOS/RHEL
sudo yum install GConf2
```

</details>

### macOS Específicos

<details>
<summary><strong>"chromedriver cannot be opened because the developer cannot be verified"</strong></summary>

```bash
# Permitir ejecución de chromedriver
sudo xattr -r -d com.apple.quarantine ~/.cache/selenium/

# O aprobar manualmente
# System Preferences → Security & Privacy → General → Allow
```

</details>

## 📞 Obtener Ayuda Adicional

### Información para reportar bugs

Cuando reportes un problema, incluye:

```bash
# Información del sistema
python --version
google-chrome --version
pip list | grep -E "(selenium|requests|tqdm|beautifulsoup4)"

# Información del error
python run.py URL --debug 2>&1 | tee error.log

# Estructura de archivos
find . -name "*.html" | head -10
ls -la downloads/github-offline/
```

### Logs de debug

```python
# Habilitar logs detallados en src/config.py
import logging
logging.basicConfig(level=logging.DEBUG)

# O ejecutar con verbose
python run.py URL --verbose
```

### Scripts de diagnóstico completo

```bash
# Crear script de diagnóstico
cat > diagnose.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

print("🔍 DIAGNÓSTICO DEL SISTEMA")
print("=" * 50)

# Python
stdout, stderr, code = run_cmd("python --version")
print(f"Python: {stdout.strip() if code == 0 else 'ERROR: ' + stderr}")

# Chrome
stdout, stderr, code = run_cmd("google-chrome --version")
print(f"Chrome: {stdout.strip() if code == 0 else 'No encontrado'}")

# Módulos Python
for module in ["selenium", "requests", "tqdm", "bs4"]:
    try:
        __import__(module)
        print(f"✅ {module}: OK")
    except ImportError:
        print(f"❌ {module}: FALTA")

# Archivos del proyecto
files = ["run.py", "src/github_offline.py", "requirements.txt"]
for file in files:
    if Path(file).exists():
        print(f"✅ {file}: OK")
    else:
        print(f"❌ {file}: FALTA")

print("\n🧪 EJECUTAR PRUEBAS:")
print("python test/test_chrome.py")
print("python test/test_singlefile.py")
EOF

python diagnose.py
```

---

Si ninguna de estas soluciones funciona, por favor [abre un issue](https://github.com/tu-usuario/tu-repo/issues) con toda la información de diagnóstico. ¡Estaremos encantados de ayudarte! 🚀
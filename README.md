# 📱 GitHub Offline Downloader

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com)

> 🌐 **Descarga repositorios completos de GitHub para navegación offline** - Issues, Pull Requests, Releases, Tags y más, todo disponible sin conexión a internet.

![Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=GitHub+Offline+Downloader+Demo)

## 📋 Tabla de Contenidos

- [🚀 Instalación Rápida](#-instalación-rápida)
- [📖 Uso Básico](#-uso-básico)
- [✨ Características](#-características)
- [🎯 ¿Para qué sirve?](#-para-qué-sirve)
- [⚙️ Configuración](#️-configuración)
- [📚 Ejemplos](#-ejemplos)
- [🔧 Troubleshooting](#-troubleshooting)
- [🤝 Contribuir](#-contribuir)

## 🚀 Instalación Rápida

### 🤖 Instalación Automática (Recomendada)

#### Windows
```cmd
# Descargar y ejecutar el instalador
curl -o setup.bat https://raw.githubusercontent.com/tu-usuario/tu-repo/main/setup.bat
setup.bat
```

#### Linux/macOS
```bash
# Descargar y ejecutar el instalador
curl -sSL https://raw.githubusercontent.com/tu-usuario/tu-repo/main/setup.sh | bash
```

### 🔧 Instalación Manual

<details>
<summary>📋 Requisitos</summary>

**📦 Software Necesario:**
- **Python 3.8+** - [Descargar](https://python.org/downloads/)
- **Google Chrome** - [Descargar](https://chrome.google.com/)
- **Git** (opcional) - [Descargar](https://git-scm.com/)

**💾 Espacio en Disco:**
- Mínimo: 500 MB para la instalación
- Recomendado: 2 GB+ para repositorios grandes

**🌐 Conexión a Internet:**
- Necesaria solo durante la descarga inicial
- Los archivos funcionan completamente offline después

</details>

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/github-offline-downloader.git
cd github-offline-downloader

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. ¡Listo para usar!
python run.py https://github.com/microsoft/vscode
```

## 📖 Uso Básico

### 🎯 Descarga Simple

```bash
# Activar entorno virtual (si no está activo)
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Descargar repositorio
python run.py https://github.com/usuario/repositorio
```

### 🎛️ Opciones Disponibles

```bash
# Modo headless (sin ventana de Chrome visible)
python run.py https://github.com/usuario/repo --headless

# Usar perfil específico de Chrome
python run.py https://github.com/usuario/repo --profile "Perfil 1"

# Ajustar velocidad de descarga (segundos entre páginas)
python run.py https://github.com/usuario/repo --delay 5.0

# Combinación de opciones
python run.py https://github.com/facebook/react --headless --delay 10
```

### 📁 Resultado de la Descarga

Después de la descarga, encontrarás:

```
~/Downloads/github-offline/usuario_repositorio-offline/
├── 📄 index.html              # Página principal del repositorio
├── 🧭 navigation.html         # Índice de navegación offline
├── 📁 issues/                 # Issues del repositorio
│   ├── 📁 open/              # Issues abiertos
│   │   ├── 📄 page-1.html    # Lista de issues (página 1)
│   │   ├── 📄 page-2.html    # Lista de issues (página 2)
│   │   └── 📁 individual/    # Issues individuales
│   │       ├── 📄 issue-1.html
│   │       ├── 📄 issue-2.html
│   │       └── ...
│   └── 📁 closed/            # Issues cerrados (misma estructura)
├── 📁 pulls/                 # Pull requests (misma estructura que issues)
├── 📁 releases/              # Releases del proyecto
│   ├── 📄 page-1.html        # Lista de releases
│   └── 📁 individual/        # Releases individuales
│       ├── 📄 release-v1.0.0.html
│       └── ...
└── 📁 tags/                  # Tags del proyecto
    ├── 📄 page-1.html        # Lista de tags
    └── 📁 individual/        # Tags individuales
```

**🌐 Para navegar:** Abre `navigation.html` en tu navegador favorito y tendrás acceso completo al repositorio sin internet.

## ✨ Características

### 🎯 Descarga Completa
- **📄 Página Principal**: Código fuente y README del repositorio
- **🐛 Issues**: Abiertos y cerrados, con todos los comentarios y discusiones
- **🔄 Pull Requests**: Estado completo con diffs, revisiones y comentarios
- **🚀 Releases**: Todas las versiones publicadas con notas de cambio
- **🏷️ Tags**: Historial completo de etiquetas y versiones
- **📖 Wiki**: Documentación del proyecto (si está disponible)
- **📊 Projects**: Tableros de proyecto y métricas

### 🌟 Funcionalidades Avanzadas
- **👤 Selector de Perfiles**: Usa automáticamente tus sesiones activas de GitHub
- **🔗 Navegación Offline**: Enlaces reescritos para funcionar sin internet
- **📱 Interfaz Intuitiva**: Índice de navegación HTML generado automáticamente
- **⚡ Descarga Inteligente**: Manejo automático de paginación y rate limiting
- **🎨 Preservación Visual**: Mantiene el diseño original de GitHub
- **🔧 Configuración Flexible**: Delays personalizables, modo headless, perfiles específicos

### 🛠️ Compatibilidad
- **🖥️ Sistemas**: Windows 10+, Linux (Ubuntu, CentOS, Arch), macOS 10.14+
- **🌐 Navegadores**: Chrome, Chromium, Edge
- **🐍 Python**: 3.8, 3.9, 3.10, 3.11+

## 🎯 ¿Para qué sirve?

### 📚 Casos de Uso Principales

#### 🔬 **Investigación y Análisis**
```bash
# Analizar issues de un proyecto grande
python run.py https://github.com/tensorflow/tensorflow --delay 15

# Estudiar pull requests de frameworks populares
python run.py https://github.com/angular/angular --headless
```

#### 📖 **Documentación y Archivo**
```bash
# Crear backup completo de repositorios importantes
python run.py https://github.com/company/critical-project --delay 10

# Archivar decisiones técnicas documentadas en issues
python run.py https://github.com/team/project --profile "Work"
```

#### 🎓 **Educación y Aprendizaje**
```bash
# Estudiar código fuente offline
python run.py https://github.com/microsoft/vscode

# Analizar patrones de desarrollo en proyectos open source
python run.py https://github.com/facebook/react --delay 5
```

#### 🏢 **Uso Empresarial**
```bash
# Auditorías de seguridad offline
python run.py https://github.com/company/private-repo --profile "Security"

# Análisis de dependencias y compliance
python run.py https://github.com/vendor/library --headless --delay 20
```

### 🌟 **Ventajas Clave**

- ✅ **Acceso sin internet**: Navega issues y PRs completamente offline
- ✅ **Velocidad**: No esperes a que cargue GitHub, todo es local
- ✅ **Privacidad**: Toda la información se queda en tu computadora
- ✅ **Investigación**: Analiza patrones y tendencias sin límites de API
- ✅ **Backup**: Preserva información importante para el futuro
- ✅ **Presentaciones**: Demuestra proyectos sin depender de internet

## ⚙️ Configuración

### 👤 Selector de Perfiles de Chrome

La herramienta detecta automáticamente tus perfiles de Chrome y te permite elegir:

```
🌐 SELECTOR DE PERFIL DE CHROME
================================================================================
📁 Directorio de Chrome: /Users/usuario/.../Chrome/User Data
📊 Perfiles encontrados: 3

1. 👤 Perfil Principal
   📧 Email: usuario@gmail.com
   📁 Carpeta: Default
   🕒 Último uso: 2024-01-15 14:30
   ⭐ Perfil por defecto

2. 👤 Trabajo
   📧 Email: usuario@empresa.com
   📁 Carpeta: Profile 1
   🕒 Último uso: 2024-01-15 09:15

3. 🔒 Usar perfil temporal (sin datos personales)
   📧 Sin sesiones guardadas
   📁 Directorio temporal

👉 Selecciona un perfil (1-3):
```

### 🔧 Configuración Personalizada

Edita `src/config.py` para personalizar comportamiento:

```python
class Config:
    # 📁 Directorio de descargas (personalizable)
    BASE_DOWNLOAD_DIR = str(Path.home() / "Downloads" / "github-offline")
    
    # ⏱️ Tiempos de espera
    DOWNLOAD_DELAY = 3          # segundos entre descargas
    PAGE_LOAD_TIMEOUT = 30      # timeout de páginas
    
    # 🎛️ Comportamiento por defecto
    DEFAULT_HEADLESS = False    # mostrar Chrome por defecto
    
    # 🌐 Configuración de Chrome
    CHROME_PROFILE_NAME = "Default"  # perfil por defecto
```

### 📊 Configuración por Tipo de Repositorio

```bash
# Repositorios grandes (muchos issues)
python run.py https://github.com/kubernetes/kubernetes --delay 15 --headless

# Repositorios privados (usar perfil con sesión)
python run.py https://github.com/company/private --profile "Work" --delay 8

# Descarga rápida para demos
python run.py https://github.com/small/project --delay 2
```

## 📚 Ejemplos

### 🎯 Casos de Uso Específicos

<details>
<summary><strong>📊 Analizar un proyecto de machine learning</strong></summary>

```bash
# Descargar TensorFlow para análisis offline
python run.py https://github.com/tensorflow/tensorflow --delay 12 --headless

# Resultado: Podrás analizar offline:
# - Issues relacionados con bugs y nuevas características
# - Pull requests con mejoras de rendimiento
# - Releases con cambios importantes
# - Discusiones técnicas en comentarios
```

</details>

<details>
<summary><strong>🔒 Auditoría de seguridad</strong></summary>

```bash
# Usar perfil específico para trabajo de seguridad
python run.py https://github.com/organization/security-lib --profile "Security" --delay 20

# Analizar offline:
# - Issues relacionados con vulnerabilidades
# - Pull requests de parches de seguridad
# - Discusiones sobre CVEs
# - Historial de fixes de seguridad
```

</details>

<details>
<summary><strong>📖 Crear material educativo</strong></summary>

```bash
# Descargar proyectos educativos famosos
python run.py https://github.com/microsoft/vscode --delay 8
python run.py https://github.com/facebook/react --delay 6
python run.py https://github.com/angular/angular --delay 6

# Usar para:
# - Estudiar arquitectura de software offline
# - Analizar procesos de desarrollo
# - Crear presentaciones sin internet
# - Investigar patrones de código
```

</details>

<details>
<summary><strong>🏢 Backup empresarial</strong></summary>

```bash
# Backup de repositorios críticos de la empresa
python run.py https://github.com/company/core-system --profile "Work" --delay 15

# Beneficios:
# - Preservar decisiones técnicas documentadas en issues
# - Backup de discusiones importantes
# - Historial completo independiente de GitHub
# - Acceso sin internet para auditorías
```

</details>

### 📝 Uso Programático

Puedes usar la herramienta desde Python:

```python
from src.github_offline import GitHubOfflineAutomation

# Uso básico
downloader = GitHubOfflineAutomation("https://github.com/usuario/repo")
downloader.run()

# Con configuración personalizada
downloader = GitHubOfflineAutomation(
    github_url="https://github.com/facebook/react",
    headless=True,
    download_delay=8.0
)
downloader.run()
```

## 🔧 Troubleshooting

### ❌ Problemas Comunes

<details>
<summary><strong>🚫 "Chrome no se puede iniciar"</strong></summary>

**Síntomas:** Error al iniciar ChromeDriver

**Soluciones:**
1. **Cerrar Chrome completamente:**
   ```bash
   # Linux/macOS
   pkill chrome
   
   # Windows (PowerShell como admin)
   taskkill /f /im chrome.exe
   ```

2. **Usar perfil temporal:**
   ```bash
   python run.py URL --profile temporal
   ```

3. **Verificar instalación de Chrome:**
   ```bash
   # Verificar que Chrome esté instalado
   google-chrome --version  # Linux
   # o visitar chrome://version en Chrome
   ```

</details>

<details>
<summary><strong>📁 "Archivos muy pequeños o vacíos"</strong></summary>

**Síntomas:** Archivos HTML de menos de 1KB

**Soluciones:**
1. **Usar perfil con sesión activa:**
   ```bash
   python run.py URL --profile "Tu-Perfil-Con-GitHub-Logueado"
   ```

2. **Aumentar delay para repositorios grandes:**
   ```bash
   python run.py URL --delay 15
   ```

3. **Verificar acceso al repositorio:**
   - Abre el repositorio manualmente en Chrome
   - Verifica que puedes acceder normalmente
   - Para repos privados, asegúrate de estar logueado

</details>

<details>
<summary><strong>⚠️ "SingleFile no funciona"</strong></summary>

**Síntomas:** Errores relacionados con SingleFile

**Soluciones:**
1. **Instalar Node.js y SingleFile CLI:**
   ```bash
   # Instalar Node.js desde https://nodejs.org
   npm install -g single-file-cli
   ```

2. **Verificar instalación:**
   ```bash
   single-file --help
   ```

3. **Usar descarga automática:**
   ```bash
   # Si Node.js no está disponible, SingleFile se descarga automáticamente
   # Solo ejecuta normalmente
   python run.py URL
   ```

</details>

### 🧪 Scripts de Diagnóstico

```bash
# Probar configuración de Chrome
python test/test_chrome.py

# Probar SingleFile
python test/test_singlefile.py

# Reparar ChromeDriver
python test/fix_chromedriver.py
```

### 📞 Obtener Ayuda

Si tienes problemas:

1. **Revisa los logs** durante la ejecución
2. **Ejecuta las pruebas de diagnóstico**
3. **Consulta la documentación detallada** en `docs/`
4. **Abre un issue** en GitHub con:
   - Sistema operativo y versión
   - Versión de Python: `python --version`
   - Versión de Chrome: `chrome://version`
   - Logs completos del error
   - URL del repositorio que intentas descargar

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! 🎉

### 🚀 Cómo Contribuir

1. **🍴 Fork** el repositorio
2. **🌿 Crear** una rama: `git checkout -b feature/nueva-funcionalidad`
3. **💻 Hacer** cambios y commits: `git commit -m 'Añadir nueva funcionalidad'`
4. **📤 Push**: `git push origin feature/nueva-funcionalidad`
5. **🔄 Crear** un Pull Request

### 🐛 Reportar Bugs

Usa [GitHub Issues](https://github.com/tu-usuario/tu-repo/issues) con:

- **🖥️ Sistema operativo** y versión
- **🐍 Versión de Python**: `python --version`
- **🌐 Versión de Chrome**: `chrome://version`
- **📝 Pasos** para reproducir el error
- **📋 Logs** completos del error
- **🔗 URL** del repositorio que causa problemas

### 💡 Sugerir Funcionalidades

¿Tienes ideas para mejorar la herramienta?

- **📊 Analytics**: Estadísticas de actividad del repositorio
- **🔍 Búsqueda**: Índice de búsqueda en archivos offline
- **📱 Mobile**: Versión optimizada para móviles
- **🎨 Themes**: Temas personalizables para la navegación
- **🔄 Sync**: Sincronización incremental de cambios

## 🏆 Reconocimientos

### 🛠️ Tecnologías Utilizadas

- **[Selenium](https://selenium.dev/)** - Automatización de navegadores
- **[SingleFile](https://github.com/gildas-lormeau/SingleFile)** - Captura de páginas web
- **[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)** - Parsing HTML
- **[ChromeDriver](https://chromedriver.chromium.org/)** - Control de Chrome
- **[webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager)** - Gestión automática de drivers

### 👥 Inspiración

Este proyecto fue inspirado por la necesidad de:
- Acceso offline a documentación técnica
- Análisis de proyectos sin dependencia de internet
- Archivo permanente de decisiones técnicas en issues
- Investigación académica sobre desarrollo de software

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

```
MIT License

Copyright (c) 2024 GitHub Offline Downloader

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**⭐ Si este proyecto te resulta útil, ¡dale una estrella! ⭐**

[🐛 Reportar Bug](https://github.com/tu-usuario/tu-repo/issues) • [💡 Sugerir Feature](https://github.com/tu-usuario/tu-repo/discussions) • [💬 Discusiones](https://github.com/tu-usuario/tu-repo/discussions)

---

**Hecho con ❤️ para la comunidad de desarrolladores**

*Última actualización: Enero 2024*

</div>
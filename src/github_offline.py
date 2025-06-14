import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
from .config import Config
from .github_parser import GitHubParser
from .offline_navigator import OfflineNavigator

class GitHubOfflineAutomation:
    def __init__(self, github_url, profile=None, headless=None, download_delay=None):
        print("DEBUG: Iniciando constructor GitHubOfflineAutomation.", flush=True)
        self.github_url = github_url
        self.repo_info = GitHubParser.parse_repo_url(github_url)
        self.repo_name = f"{self.repo_info['owner']}_{self.repo_info['repo']}-offline"
        
        # 🆕 NUEVA FUNCIONALIDAD: Selección de perfil de Chrome
        if profile is None:
            from .chrome_user_selector import select_chrome_profile
            print("\n" + "="*70)
            print("🔧 CONFIGURACIÓN DE PERFIL DE CHROME")
            print("="*70)
            print("Para descargar el repositorio, necesitamos configurar qué perfil de Chrome usar.")
            print("Esto permite usar tus sesiones activas de GitHub si es necesario.")
            
            selected_profile, chrome_args = select_chrome_profile()
            
            if selected_profile:
                self.selected_profile = selected_profile
                self.chrome_profile_args = chrome_args
                print(f"✅ Configuración completada: {selected_profile['display_name']}")
            else:
                print("⚠️ Usando configuración temporal por defecto")
                self.selected_profile = None
                self.chrome_profile_args = []
        else:
            # Usar perfil especificado manualmente
            self.selected_profile = {'name': profile, 'display_name': profile}
            self.chrome_profile_args = []
        
        self.headless = headless if headless is not None else Config.DEFAULT_HEADLESS
        self.download_delay = download_delay or Config.DEFAULT_DOWNLOAD_DELAY
        self.driver = None
        self.content_structure = {}
        self.base_path = os.path.join(Config.BASE_DOWNLOAD_DIR, self.repo_name)
        
        print("DEBUG: Constructor GitHubOfflineAutomation finalizado. Llamando init_driver...", flush=True)
        # Esta llamada es importante: si falla aquí, los prints de download_page no saldrán
        self.driver = self.init_driver() 
        print("DEBUG: Driver inicializado en constructor.", flush=True)

    def get_correct_chromedriver_path(self):
        """
        Obtiene la ruta correcta del chromedriver.exe, corrigiendo el bug de webdriver_manager
        que a veces devuelve la ruta al archivo THIRD_PARTY_NOTICES en lugar del ejecutable.
        """
        try:
            # Obtener la ruta que devuelve webdriver_manager
            manager_path = ChromeDriverManager().install()
            print(f"DEBUG: webdriver_manager devuelve: {manager_path}", flush=True)
            
            # Si la ruta termina en chromedriver.exe y existe, usarla directamente
            if manager_path.endswith('chromedriver.exe') and os.path.exists(manager_path):
                print("DEBUG: ✅ webdriver_manager devolvió la ruta correcta", flush=True)
                return manager_path
            
            # Si no, buscar el chromedriver.exe real en el directorio
            directory = os.path.dirname(manager_path)
            chromedriver_exe = os.path.join(directory, 'chromedriver.exe')
            
            if os.path.exists(chromedriver_exe):
                print(f"DEBUG: ✅ Encontrado chromedriver.exe en: {chromedriver_exe}", flush=True)
                return chromedriver_exe
            
            # Buscar recursivamente si no está en el directorio inmediato
            base_dir = os.path.dirname(directory)
            for root, dirs, files in os.walk(base_dir):
                if 'chromedriver.exe' in files:
                    chromedriver_exe = os.path.join(root, 'chromedriver.exe')
                    print(f"DEBUG: ✅ Encontrado chromedriver.exe recursivamente en: {chromedriver_exe}", flush=True)
                    return chromedriver_exe
            
            # Si llegamos aquí, no pudimos encontrar el ejecutable
            raise FileNotFoundError(f"No se pudo encontrar chromedriver.exe en {directory} o subdirectorios")
            
        except Exception as e:
            print(f"DEBUG: ❌ Error obteniendo ChromeDriver: {e}", flush=True)
            raise

    def init_driver(self):
        """Inicializa el controlador de Selenium con las opciones configuradas"""
        chrome_options = Options()
        
        # 🔧 ARGUMENTOS BÁSICOS MEJORADOS PARA ESTABILIDAD
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # Acelera la carga
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=MediaRouter") # Evita warnings
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # 🆕 ARGUMENTOS ADICIONALES PARA EVITAR DEVTOOLSACTIVEPORT ERROR
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=0")  # Puerto dinámico
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-background-mode")
        
        # Suprimir logs de Chrome
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--log-level=3")  # Suprimir logs
        
        # 🎯 USAR PERFIL SELECCIONADO POR EL USUARIO (con copia segura)
        if hasattr(self, 'chrome_profile_args') and self.chrome_profile_args:
            print(f"DEBUG: 🎯 Usando perfil seleccionado: {self.selected_profile['display_name']}", flush=True)
            for arg in self.chrome_profile_args:
                chrome_options.add_argument(arg)
                print(f"DEBUG: Argumento de perfil: {arg}", flush=True)
        else:
            print("DEBUG: ⚠️ Usando perfil temporal (sin perfil personalizado)", flush=True)
            import tempfile
            temp_profile = tempfile.mkdtemp(prefix="chrome_temp_")
            chrome_options.add_argument(f"--user-data-dir={temp_profile}")
        
        # 🔧 MODO HEADLESS MEJORADO
        if self.headless:
            print("DEBUG: Modo headless activado (nueva sintaxis)", flush=True)
            chrome_options.add_argument("--headless=new")  # Nueva sintaxis más estable
        else:
            print("DEBUG: Modo headless desactivado - Chrome se abrirá visualmente", flush=True)
        
        # Usar nuestra función corregida para obtener la ruta del ChromeDriver
        chromedriver_path = self.get_correct_chromedriver_path()
        service = Service(chromedriver_path)
        
        print(f"DEBUG: Iniciando ChromeDriver desde: {chromedriver_path}", flush=True)
        
        # 🆕 INTENTOS MÚLTIPLES CON MANEJO DE ERRORES ROBUSTO
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                print(f"DEBUG: Intento {attempt}/{max_attempts} de inicialización de Chrome", flush=True)
                
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
                
                print("DEBUG: ✅ ChromeDriver iniciado exitosamente", flush=True)
                
                # Verificar que Chrome está funcionando
                driver.get("about:blank")
                print("DEBUG: ✅ Chrome respondiendo correctamente", flush=True)
                
                return driver
                
            except Exception as e:
                print(f"DEBUG: ❌ Intento {attempt} falló: {type(e).__name__}: {e}", flush=True)
                
                if attempt < max_attempts:
                    print(f"DEBUG: 🔄 Reintentando en 2 segundos...", flush=True)
                    time.sleep(2)
                    
                    # Para el siguiente intento, usar perfil completamente temporal
                    if attempt == 2 and hasattr(self, 'chrome_profile_args'):
                        print("DEBUG: 🔄 Fallback: usando perfil temporal para el siguiente intento", flush=True)
                        chrome_options = Options()
                        # Re-aplicar argumentos básicos
                        for arg in ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu", 
                                   "--disable-extensions", "--remote-debugging-port=0", "--no-first-run"]:
                            chrome_options.add_argument(arg)
                        
                        import tempfile
                        temp_profile = tempfile.mkdtemp(prefix="chrome_fallback_")
                        chrome_options.add_argument(f"--user-data-dir={temp_profile}")
                        
                        if self.headless:
                            chrome_options.add_argument("--headless=new")
                else:
                    print("DEBUG: ❌ Todos los intentos fallaron", flush=True)
                    raise Exception(f"No se pudo inicializar Chrome después de {max_attempts} intentos. Último error: {e}")
        
        # Este punto no debería alcanzarse nunca
        raise Exception("Error inesperado en la inicialización de Chrome")

    def get_github_issues_pagination_info(self, url):
        """
        Obtiene información específica de paginación para GitHub Issues/PRs
        """
        if not self.driver:
            self.driver = self.init_driver()
            
        print(f"DEBUG: Navegando a {url} para contar páginas de issues", flush=True)
        
        try:
            self.driver.get(url)
            
            # Esperar a que cargue la página
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Buscar contadores específicos de GitHub Issues (Open/Closed)
            try:
                # Selectores específicos para GitHub Issues
                issue_counters = self.driver.find_elements(By.CSS_SELECTOR, 
                    'a[data-tab-item*="issues-tab"], .UnderlineNav-item[href*="/issues"], .js-selected-navigation-item')
                
                for counter in issue_counters:
                    # Buscar el texto que contiene números
                    counter_text = counter.get_attribute('textContent') or counter.text
                    print(f"DEBUG: Texto encontrado en contador: '{counter_text.strip()}'", flush=True)
                    
                    # Buscar el span con la clase Counter que contiene el número real
                    counter_span = counter.find_element(By.CSS_SELECTOR, '.Counter') if counter else None
                    if counter_span:
                        number_text = counter_span.text.strip()
                        print(f"DEBUG: Número de issues encontrado: {number_text}", flush=True)
                        if number_text.isdigit():
                            total_issues = int(number_text)
                            # GitHub muestra 25 issues por página por defecto
                            total_pages = (total_issues + 24) // 25  # Redondear hacia arriba
                            print(f"DEBUG: Total issues: {total_issues}, páginas calculadas: {total_pages}", flush=True)
                            return total_pages
                            
            except Exception as e:
                print(f"DEBUG: Error buscando contadores específicos: {e}", flush=True)
            
            # Método alternativo: buscar paginación directa
            try:
                # Buscar la paginación en la parte inferior
                pagination_selectors = [
                    '.paginate-container',
                    '.pagination', 
                    'nav[aria-label*="Pagination"]',
                    'nav[aria-label*="pagination"]'
                ]
                
                for selector in pagination_selectors:
                    try:
                        pagination = self.driver.find_element(By.CSS_SELECTOR, selector)
                        print(f"DEBUG: Encontrada paginación con selector: {selector}", flush=True)
                        
                        # Buscar números de página
                        page_links = pagination.find_elements(By.CSS_SELECTOR, 'a, span')
                        max_page = 1
                        
                        for link in page_links:
                            text = link.text.strip()
                            print(f"DEBUG: Texto en paginación: '{text}'", flush=True)
                            
                            # Buscar números que sean páginas válidas
                            if text.isdigit():
                                page_num = int(text)
                                if page_num > max_page and page_num < 1000:  # Sanity check
                                    max_page = page_num
                        
                        print(f"DEBUG: Número máximo de páginas encontrado: {max_page}", flush=True)
                        return max_page if max_page > 1 else 1
                        
                    except:
                        continue
                        
            except Exception as e:
                print(f"DEBUG: Error buscando paginación: {e}", flush=True)
            
            print("DEBUG: No se encontró paginación, asumiendo 1 página", flush=True)
            return 1
                
        except Exception as e:
            print(f"DEBUG: Error general navegando a la página: {e}", flush=True)
            return 1

    def get_issue_links_from_page(self, url):
        """
        Obtiene todos los enlaces de issues/PRs individuales de una página de listado
        """
        if not self.driver:
            self.driver = self.init_driver()
            
        print(f"DEBUG: Obteniendo enlaces de issues desde: {url}", flush=True)
        
        try:
            self.driver.get(url)
            
            # Esperar a que carguen los issues
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Selectores para enlaces de issues/PRs individuales en GitHub
            issue_link_selectors = [
                'a[data-hovercard-url*="/issues/"][data-hovercard-url*="/hovercard"]',
                'a[href*="/issues/"][class*="Link"]',
                'a[href*="/pull/"][class*="Link"]',
                '.js-navigation-open[href*="/issues/"]',
                '.js-navigation-open[href*="/pull/"]'
            ]
            
            issue_links = []
            
            for selector in issue_link_selectors:
                try:
                    links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for link in links:
                        href = link.get_attribute('href')
                        if href and ('/issues/' in href or '/pull/' in href):
                            # Evitar duplicados y enlaces que no sean issues/PRs individuales
                            if href not in issue_links and not href.endswith('/issues') and not href.endswith('/pulls'):
                                issue_links.append(href)
                                print(f"DEBUG: Enlace de issue encontrado: {href}", flush=True)
                    
                    if issue_links:
                        break  # Si encontramos enlaces con este selector, no necesitamos los otros
                        
                except Exception as e:
                    print(f"DEBUG: Error con selector {selector}: {e}", flush=True)
                    continue
            
            print(f"DEBUG: Total de enlaces de issues encontrados: {len(issue_links)}", flush=True)
            return issue_links
            
        except Exception as e:
            print(f"DEBUG: Error obteniendo enlaces de issues: {e}", flush=True)
            return []

    def get_release_links_from_page(self, url):
        """
        Obtiene todos los enlaces de releases individuales de una página de listado
        """
        if not self.driver:
            self.driver = self.init_driver()
            
        print(f"DEBUG: Obteniendo enlaces de releases desde: {url}", flush=True)
        
        try:
            self.driver.get(url)
            
            # Esperar a que carguen los releases
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Selectores para enlaces de releases individuales
            release_link_selectors = [
                'a[href*="/releases/tag/"]',
                '.release-entry a[href*="/releases/tag/"]',
                '.Box-row a[href*="/releases/tag/"]',
                '[data-hovercard-url*="/releases/tag/"]'
            ]
            
            release_links = []
            
            for selector in release_link_selectors:
                try:
                    links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for link in links:
                        href = link.get_attribute('href')
                        if href and '/releases/tag/' in href:
                            if href not in release_links:
                                release_links.append(href)
                                print(f"DEBUG: Enlace de release encontrado: {href}", flush=True)
                    
                    if release_links:
                        break  # Si encontramos enlaces con este selector, no necesitamos los otros
                        
                except Exception as e:
                    print(f"DEBUG: Error con selector {selector}: {e}", flush=True)
                    continue
            
            print(f"DEBUG: Total de enlaces de releases encontrados: {len(release_links)}", flush=True)
            return release_links
            
        except Exception as e:
            print(f"DEBUG: Error obteniendo enlaces de releases: {e}", flush=True)
            return []

    def get_tag_links_from_page(self, url):
        """
        Obtiene todos los enlaces de tags individuales de una página de listado
        """
        if not self.driver:
            self.driver = self.init_driver()
            
        print(f"DEBUG: Obteniendo enlaces de tags desde: {url}", flush=True)
        
        try:
            self.driver.get(url)
            
            # Esperar a que carguen los tags
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Selectores para enlaces de tags individuales
            tag_link_selectors = [
                'a[href*="/tree/"][class*="Link"]',
                'a[href*="/releases/tag/"]',  # Tags también pueden aparecer en releases
                '.Box-row a[href*="/tree/"]',
                '.js-navigation-open[href*="/tree/"]'
            ]
            
            tag_links = []
            
            for selector in tag_link_selectors:
                try:
                    links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for link in links:
                        href = link.get_attribute('href')
                        if href and ('/tree/' in href or '/releases/tag/' in href):
                            # Evitar enlaces que no sean tags (como ramas principales)
                            if not any(branch in href for branch in ['/tree/main', '/tree/master', '/tree/develop']):
                                if href not in tag_links:
                                    tag_links.append(href)
                                    print(f"DEBUG: Enlace de tag encontrado: {href}", flush=True)
                    
                    if tag_links:
                        break
                        
                except Exception as e:
                    print(f"DEBUG: Error con selector {selector}: {e}", flush=True)
                    continue
            
            print(f"DEBUG: Total de enlaces de tags encontrados: {len(tag_links)}", flush=True)
            return tag_links
            
        except Exception as e:
            print(f"DEBUG: Error obteniendo enlaces de tags: {e}", flush=True)
            return []

    def download_releases_section(self, section_type, base_url):
        """Descarga releases con sus releases individuales"""
        # Crear estructura de directorios
        section_dir = os.path.join(self.base_path, section_type)
        os.makedirs(section_dir, exist_ok=True)
        
        # Crear directorio para releases individuales
        individual_dir = os.path.join(section_dir, 'individual')
        os.makedirs(individual_dir, exist_ok=True)
        
        # Para releases, generalmente hay pocas páginas
        total_pages = self.get_github_issues_pagination_info(base_url)
        print(f"🔍 {section_type}: {total_pages} páginas encontradas")
        
        all_release_links = []
        
        # Descargar cada página de listado Y recopilar enlaces de releases individuales
        for page in tqdm(range(1, total_pages + 1), desc=f"{section_type} páginas"):
            page_url = GitHubParser.get_paginated_url(base_url, page)
            filename = f"page-{page}.html"
            filepath = os.path.join(section_dir, filename)
            
            # Descargar la página de listado
            self.download_page(page_url, filepath)
            
            # Obtener enlaces de releases individuales de esta página
            release_links = self.get_release_links_from_page(page_url)
            all_release_links.extend(release_links)
            
            time.sleep(self.download_delay)
        
        # Eliminar duplicados
        unique_release_links = list(set(all_release_links))
        print(f"📋 Encontrados {len(unique_release_links)} releases únicos")
        
        # Descargar cada release individual
        for i, release_url in enumerate(tqdm(unique_release_links, desc=f"{section_type} individuales"), 1):
            try:
                # Extraer tag del release de la URL de forma simple
                if '/releases/tag/' in release_url:
                    tag_name = release_url.split('/releases/tag/')[-1].split('?')[0].split('#')[0]
                else:
                    tag_name = f"release-{i}"
                
                # Normalizar nombre del tag para archivo
                normalized_tag = tag_name.replace('/', '_').replace('\\', '_').replace(':', '_')
                normalized_tag = normalized_tag.replace('<', '_').replace('>', '_').replace('|', '_')
                normalized_tag = normalized_tag.replace('"', '_').replace('?', '_').replace('*', '_')
                
                filename = f"release-{normalized_tag}.html"
                filepath = os.path.join(individual_dir, filename)
                
                self.download_page(release_url, filepath)
                time.sleep(self.download_delay)
                
            except Exception as e:
                print(f"❌ Error descargando release {release_url}: {e}", flush=True)
                continue
        
        # Registrar en estructura de contenido
        self.content_structure.setdefault(section_type, []).append({
            "name": f"{section_type.capitalize()}",
            "count": total_pages,
            "individual_count": len(unique_release_links),
            "first_page": f"{section_type}/page-1.html"
        })

    def download_tags_section(self, section_type, base_url):
        """Descarga tags con sus tags individuales"""
        # Crear estructura de directorios
        section_dir = os.path.join(self.base_path, section_type)
        os.makedirs(section_dir, exist_ok=True)
        
        # Crear directorio para tags individuales
        individual_dir = os.path.join(section_dir, 'individual')
        os.makedirs(individual_dir, exist_ok=True)
        
        # Para tags, generalmente hay pocas páginas
        total_pages = self.get_github_issues_pagination_info(base_url)
        print(f"🔍 {section_type}: {total_pages} páginas encontradas")
        
        all_tag_links = []
        
        # Descargar cada página de listado Y recopilar enlaces de tags individuales
        for page in tqdm(range(1, total_pages + 1), desc=f"{section_type} páginas"):
            # Construcción manual de URL paginada (sin dependencia de GitHubParser)
            separator = '&' if '?' in base_url else '?'
            page_url = f"{base_url}{separator}page={page}"
            
            filename = f"page-{page}.html"
            filepath = os.path.join(section_dir, filename)
            
            # Descargar la página de listado
            self.download_page(page_url, filepath)
            
            # Obtener enlaces de tags individuales de esta página
            tag_links = self.get_tag_links_from_page(page_url)
            all_tag_links.extend(tag_links)
            
            time.sleep(self.download_delay)
        
        # Eliminar duplicados
        unique_tag_links = list(set(all_tag_links))
        print(f"📋 Encontrados {len(unique_tag_links)} tags únicos")
        
        # Descargar cada tag individual
        for i, tag_url in enumerate(tqdm(unique_tag_links, desc=f"{section_type} individuales"), 1):
            try:
                # Extraer nombre del tag de la URL de forma simple
                if '/releases/tag/' in tag_url:
                    tag_name = tag_url.split('/releases/tag/')[-1].split('?')[0].split('#')[0]
                elif '/tree/' in tag_url:
                    tag_name = tag_url.split('/tree/')[-1].split('?')[0].split('#')[0]
                else:
                    tag_name = f"tag-{i}"
                
                # Normalizar nombre del tag para archivo
                normalized_tag = tag_name.replace('/', '_').replace('\\', '_').replace(':', '_')
                normalized_tag = normalized_tag.replace('<', '_').replace('>', '_').replace('|', '_')
                normalized_tag = normalized_tag.replace('"', '_').replace('?', '_').replace('*', '_')
                
                filename = f"tag-{normalized_tag}.html"
                filepath = os.path.join(individual_dir, filename)
                
                self.download_page(tag_url, filepath)
                time.sleep(self.download_delay)
                
            except Exception as e:
                print(f"❌ Error descargando tag {tag_url}: {e}", flush=True)
                continue
        
        # Registrar en estructura de contenido
        self.content_structure.setdefault(section_type, []).append({
            "name": f"{section_type.capitalize()}",
            "count": total_pages,
            "individual_count": len(unique_tag_links),
            "first_page": f"{section_type}/page-1.html"
        })

    def download_section(self, section_type, base_url, state=None):
        """Descarga todas las páginas de una sección Y los issues/PRs individuales"""
        # Crear estructura de directorios
        section_dir = os.path.join(self.base_path, section_type)
        if state:
            section_dir = os.path.join(section_dir, state)
        
        os.makedirs(section_dir, exist_ok=True)
        
        # Crear directorio para issues individuales
        individual_dir = os.path.join(section_dir, 'individual')
        os.makedirs(individual_dir, exist_ok=True)
        
        # Obtener número total de páginas usando método específico de GitHub
        total_pages = self.get_github_issues_pagination_info(base_url)
        print(f"🔍 {section_type}/{state or 'main'}: {total_pages} páginas encontradas")
        
        all_issue_links = []
        
        # Descargar cada página de listado Y recopilar enlaces de issues individuales
        for page in tqdm(range(1, total_pages + 1), desc=f"{section_type}-{state} páginas"):
            page_url = GitHubParser.get_paginated_url(base_url, page)
            filename = f"page-{page}.html"
            filepath = os.path.join(section_dir, filename)
            
            # Descargar la página de listado
            self.download_page(page_url, filepath)
            
            # Obtener enlaces de issues individuales de esta página
            issue_links = self.get_issue_links_from_page(page_url)
            all_issue_links.extend(issue_links)
            
            time.sleep(self.download_delay)
        
        # Eliminar duplicados
        unique_issue_links = list(set(all_issue_links))
        print(f"📋 Encontrados {len(unique_issue_links)} issues únicos en {section_type}/{state or 'main'}")
        
        # Descargar cada issue/PR individual
        for i, issue_url in enumerate(tqdm(unique_issue_links, desc=f"{section_type}-{state} issues"), 1):
            try:
                # Extraer número del issue de la URL
                issue_number = issue_url.split('/')[-1]
                filename = f"issue-{issue_number}.html"
                filepath = os.path.join(individual_dir, filename)
                
                self.download_page(issue_url, filepath)
                time.sleep(self.download_delay)
                
            except Exception as e:
                print(f"❌ Error descargando issue {issue_url}: {e}", flush=True)
                continue
        
        # Registrar en estructura de contenido
        section_key = section_type
        if state:
            section_key = f"{section_type}_{state}"
        
        self.content_structure.setdefault(section_key, []).append({
            "name": f"{section_type.capitalize()}",
            "state": state,
            "count": total_pages,
            "individual_count": len(unique_issue_links),
            "first_page": f"{section_type}/{state or ''}/page-1.html" if state else f"{section_type}/page-1.html"
        })

    def download_page(self, url, output_path):
        """Descarga una página usando SingleFile CLI - VERSIÓN CORREGIDA PARA GITHUB"""
        print(f"DEBUG: Preparando comando SingleFile para URL: {url}", flush=True)
        print(f"DEBUG: Ruta de salida: {output_path}", flush=True)

        # Asegurar que el directorio de salida existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # ✅ CONFIGURACIÓN CORREGIDA: Sin headless para GitHub
        singlefile_exe_path = Config.SINGLEFILE_PATH
        
        # ✅ COMANDO CORREGIDO: Argumentos posicionales + tiempo de espera mayor
        cmd = [
            singlefile_exe_path,
            url,
            output_path,  # Argumento posicional, no --output
            "--browser-wait-delay=8000",  # Tiempo suficiente para GitHub
            f"--browser-executable-path={self.get_chrome_path()}"
        ]
        
        # ❌ REMOVIDOS: Los siguientes parámetros causan archivos vacíos en GitHub
        # "--browser-headless=true",  # ← Este era el problema principal
        # "--browser-wait-until=networkidle0",  # ← Parámetro problemático
        
        print(f"DEBUG: ✅ Comando SingleFile corregido: {' '.join(cmd)}", flush=True)
        print("DEBUG: ⚠️ NOTA: Chrome se abrirá visualmente para evitar detección de bot de GitHub", flush=True)

        try:
            # Usar subprocess.run para mejor control
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
                text=True
            )

            print(f"DEBUG: SingleFile return code: {result.returncode}", flush=True)
            
            if result.stderr:
                print(f"DEBUG: SingleFile stderr: {result.stderr[:200]}", flush=True)

            if result.returncode != 0:
                print(f"⚠️ Error descargando {url}. Código de retorno: {result.returncode}", flush=True)
            else:
                # Verificar que el archivo se haya creado y tenga contenido
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    if file_size > 1000:  # Archivo significativo
                        print(f"✅ Descargado exitosamente: {os.path.basename(output_path)} ({file_size} bytes)", flush=True)
                    elif file_size > 0:
                        print(f"⚠️ Archivo pequeño descargado: {os.path.basename(output_path)} ({file_size} bytes)", flush=True)
                    else:
                        print(f"❌ Archivo vacío descargado: {os.path.basename(output_path)}", flush=True)
                else:
                    print(f"❌ Archivo no fue creado: {output_path}", flush=True)
                
        except subprocess.TimeoutExpired:
            print(f"⌛ Tiempo de espera agotado para {url}", flush=True)
        except Exception as e:
            print(f"❌ Error ejecutando SingleFile: {type(e).__name__}: {e}", flush=True)

    def get_chrome_path(self):
        """Obtiene la ruta del ejecutable de Chrome según el SO"""
        if os.name == 'nt':  # Windows
            return "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        elif os.uname().sysname == 'Darwin':  # macOS
            return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        else:  # Linux
            return "/usr/bin/google-chrome"

    def run(self):
        """Ejecuta el proceso completo de descarga"""
        try:
            print(f"🚀 Iniciando descarga de: {self.repo_name}")
            print(f"📁 Los archivos se guardarán en: {self.base_path}")
            print("⚠️ IMPORTANTE: Chrome se abrirá visualmente durante las descargas (necesario para GitHub)")
            
            # Crear directorio base
            os.makedirs(self.base_path, exist_ok=True)
            
            # Inicializar driver si es necesario para paginación
            if not self.driver:
                self.driver = self.init_driver()
            
            # Obtener URLs de contenido
            content_urls = GitHubParser.get_content_urls(self.repo_info)
            
            # Descargar página principal
            print("⬇️ Descargando página principal...")
            main_page_path = os.path.join(self.base_path, "index.html")
            self.download_page(content_urls['home'], main_page_path)
            
            # Verificar que se descargó la página principal
            if os.path.exists(main_page_path) and os.path.getsize(main_page_path) > 1000:
                print(f"✅ Página principal descargada correctamente: {main_page_path}")
            else:
                print(f"⚠️ Problema con la descarga de la página principal")
            
            # Descargar secciones paginadas (con issues individuales)
            sections = [
                ('issues', content_urls['issues_open'], 'open'),
                ('issues', content_urls['issues_closed'], 'closed'),
                ('pulls', content_urls['pulls_open'], 'open'),
                ('pulls', content_urls['pulls_closed'], 'closed')
            ]
            
            for section, url, state in sections:
                print(f"\n🔄 Procesando sección: {section}/{state}")
                self.download_section(section, url, state)
            
            # 🆕 DESCARGAR RELEASES Y TAGS
            print(f"\n🔄 Procesando releases...")
            self.download_releases_section('releases', content_urls['releases'])
            
            print(f"\n🔄 Procesando tags...")  
            self.download_tags_section('tags', content_urls['tags'])
            
            # Descargar otras secciones (sin issues individuales)
            for section in ['wiki', 'projects', 'insights']:
                if section in content_urls:
                    print(f"\n🔄 Descargando sección: {section}")
                    # Para estas secciones, usar el método simple sin issues individuales
                    self.download_simple_section(section, content_urls[section])
            
            # Reescribir enlaces para navegación offline
            print("\n🔗 Reescribiendo enlaces para navegación offline...")
            from .link_rewriter import OfflineLinkRewriter
            
            link_rewriter = OfflineLinkRewriter(self.base_path, self.repo_info)
            total_files, total_links = link_rewriter.rewrite_all_links()
            
            # Crear archivo de debug (opcional)
            link_rewriter.create_link_map_debug()
            
            # Generar navegación offline
            print("\n🧭 Generando índice de navegación...")
            OfflineNavigator.generate_navigation_index(
                self.repo_name,
                self.content_structure,
                self.base_path
            )
            
            print(f"\n✅ ¡Descarga completada! Repositorio disponible en:\n{self.base_path}")
            print(f"🔗 Enlaces reescritos: {total_links} en {total_files} archivos")
            
            # Mostrar resumen de archivos descargados
            print("\n📊 Resumen de descarga:")
            total_files = 0
            total_size = 0
            for root, dirs, files in os.walk(self.base_path):
                if files:
                    rel_path = os.path.relpath(root, self.base_path)
                    if rel_path == ".":
                        rel_path = "/"
                    
                    section_size = sum(os.path.getsize(os.path.join(root, f)) for f in files if os.path.exists(os.path.join(root, f)))
                    total_files += len(files)
                    total_size += section_size
                    
                    print(f"  📁 {rel_path}: {len(files)} archivo(s) ({section_size // 1024} KB)")
            
            print(f"\n📈 Total: {total_files} archivos, {total_size // (1024*1024)} MB")
            
        except Exception as e:
            print(f"❌ Error crítico: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                print("DEBUG: Cerrando driver...", flush=True)
                self.driver.quit()

    def download_simple_section(self, section_type, base_url):
        """Descarga secciones simples sin issues individuales (wiki, projects, etc.)"""
        # Crear estructura de directorios
        section_dir = os.path.join(self.base_path, section_type)
        os.makedirs(section_dir, exist_ok=True)
        
        # Para estas secciones, generalmente solo hay una página o muy pocas
        total_pages = self.get_github_issues_pagination_info(base_url)
        print(f"🔍 {section_type}: {total_pages} páginas encontradas")
        
        # Descargar cada página
        for page in tqdm(range(1, total_pages + 1), desc=f"{section_type}"):
            page_url = GitHubParser.get_paginated_url(base_url, page)
            filename = f"page-{page}.html"
            filepath = os.path.join(section_dir, filename)
            
            self.download_page(page_url, filepath)
            time.sleep(self.download_delay)
        
        # Registrar en estructura de contenido
        self.content_structure.setdefault(section_type, []).append({
            "name": f"{section_type.capitalize()}",
            "count": total_pages,
            "first_page": f"{section_type}/page-1.html"
        })
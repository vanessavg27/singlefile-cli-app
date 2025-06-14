#!/usr/bin/env python3
"""
Módulo para reescribir enlaces en archivos HTML descargados
Convierte enlaces de GitHub online a navegación offline local
VERSIÓN DEFINITIVA Y OPTIMIZADA CON RELEASES Y TAGS
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class OfflineLinkRewriter:
    """
    Reescribe enlaces en archivos HTML descargados para navegación offline completa
    """
    
    def __init__(self, base_path, repo_info):
        self.base_path = Path(base_path)
        self.repo_info = repo_info
        self.github_base_url = f"https://github.com/{repo_info['owner']}/{repo_info['repo']}"
        
        # 🎯 PATRONES OPTIMIZADOS CON RELEASES Y TAGS
        self.url_patterns = [
            # Issues individuales
            (re.compile(r'/issues/(\d+)(?:[/#?].*)?$'), self._resolve_issue_path),
            
            # Pull requests individuales
            (re.compile(r'/pull/(\d+)(?:[/#?].*)?$'), self._resolve_pull_path),
            
            # 🆕 RELEASES INDIVIDUALES
            (re.compile(r'/releases/tag/([^/#?]+)(?:[/#?].*)?$'), self._resolve_release_path),
            
            # 🆕 TAGS INDIVIDUALES  
            (re.compile(r'/tree/([^/#?]+)(?:[/#?].*)?$'), self._resolve_tag_path),
            
            # Páginas de listado con paginación
            (re.compile(r'/issues\?.*page=(\d+)'), lambda m, _: f'issues/open/page-{m.group(1)}.html'),
            (re.compile(r'/pulls\?.*page=(\d+)'), lambda m, _: f'pulls/open/page-{m.group(1)}.html'),
            (re.compile(r'/releases\?.*page=(\d+)'), lambda m, _: f'releases/page-{m.group(1)}.html'),
            (re.compile(r'/tags\?.*page=(\d+)'), lambda m, _: f'tags/page-{m.group(1)}.html'),
            
            # Páginas de listado por estado
            (re.compile(r'/issues\?.*state=closed'), lambda m, _: 'issues/closed/page-1.html'),
            (re.compile(r'/issues\?.*state=open'), lambda m, _: 'issues/open/page-1.html'),
            (re.compile(r'/pulls\?.*state=closed'), lambda m, _: 'pulls/closed/page-1.html'),
            (re.compile(r'/pulls\?.*state=open'), lambda m, _: 'pulls/open/page-1.html'),
            
            # Páginas de listado simples
            (re.compile(r'/issues/?$'), lambda m, _: 'issues/open/page-1.html'),
            (re.compile(r'/pulls/?$'), lambda m, _: 'pulls/open/page-1.html'),
            (re.compile(r'/releases/?$'), lambda m, _: 'releases/page-1.html'),
            (re.compile(r'/tags/?$'), lambda m, _: 'tags/page-1.html'),
            
            # Página principal del repositorio
            (re.compile(r'^/?(?:#.*)?$'), lambda m, _: 'index.html'),
            (re.compile(r'/tree/(?:main|master)(?:[/#?].*)?$'), lambda m, _: 'index.html'),
            
            # Otras secciones
            (re.compile(r'/wiki/?$'), lambda m, _: 'wiki/page-1.html'),
            (re.compile(r'/projects/?$'), lambda m, _: 'projects/page-1.html'),
            (re.compile(r'/pulse/?$'), lambda m, _: 'insights/page-1.html'),
            (re.compile(r'/insights/?'), lambda m, _: 'insights/page-1.html'),
        ]
    
    def _resolve_issue_path(self, match, current_file):
        """Encuentra la ruta local de un issue específico"""
        issue_number = match.group(1)
        return self._find_local_file(issue_number, 'issues')
    
    def _resolve_pull_path(self, match, current_file):
        """Encuentra la ruta local de un pull request específico"""
        issue_number = match.group(1)
        return self._find_local_file(issue_number, 'pulls')
    
    def _resolve_release_path(self, match, current_file):
        """Encuentra la ruta local de un release específico"""
        tag_name = match.group(1)
        return self._find_local_release_file(tag_name)
    
    def _resolve_tag_path(self, match, current_file):
        """Encuentra la ruta local de un tag específico"""
        tag_name = match.group(1)
        # Evitar que las ramas principales se traten como tags
        if tag_name.lower() in ['main', 'master', 'develop', 'dev']:
            return 'index.html'
        return self._find_local_tag_file(tag_name)
    
    def _resolve_release_path(self, match, current_file):
        """Encuentra la ruta local de un release específico"""
        tag_name = match.group(1)
        return self._find_local_release_file(tag_name)
    
    def _resolve_tag_path(self, match, current_file):
        """Encuentra la ruta local de un tag específico"""
        tag_name = match.group(1)
        # Evitar que las ramas principales se traten como tags
        if tag_name.lower() in ['main', 'master', 'develop', 'dev']:
            return 'index.html'
        return self._find_local_tag_file(tag_name)
    
    def _find_local_file(self, issue_number, section_type):
        """
        Busca un archivo de issue/PR por su número en ambos estados (open/closed)
        """
        filename = f"issue-{issue_number}.html"
        
        # Buscar en orden de prioridad: open primero, luego closed
        search_paths = [
            (section_type, 'open', 'individual', filename),
            (section_type, 'closed', 'individual', filename),
        ]
        
        for path_parts in search_paths:
            local_path = self.base_path.joinpath(*path_parts)
            if local_path.exists():
                return str(Path(*path_parts))
        
        # Si no se encuentra, usar ruta por defecto (open)
        return str(Path(section_type) / 'open' / 'individual' / filename)
    
    def _find_local_release_file(self, tag_name):
        """
        Busca un archivo de release por su tag
        """
        normalized_tag = self._normalize_tag_name(tag_name)
        filename = f"release-{normalized_tag}.html"
        
        # Buscar en el directorio de releases
        local_path = self.base_path / 'releases' / 'individual' / filename
        if local_path.exists():
            return str(Path('releases') / 'individual' / filename)
        
        # Si no se encuentra, usar ruta por defecto
        return str(Path('releases') / 'individual' / filename)
    
    def _find_local_tag_file(self, tag_name):
        """
        Busca un archivo de tag por su nombre
        """
        normalized_tag = self._normalize_tag_name(tag_name)
        filename = f"tag-{normalized_tag}.html"
        
        # Buscar en el directorio de tags
        local_path = self.base_path / 'tags' / 'individual' / filename
        if local_path.exists():
            return str(Path('tags') / 'individual' / filename)
        
        # Si no se encuentra, usar ruta por defecto
        return str(Path('tags') / 'individual' / filename)
    
    def _normalize_tag_name(self, tag_name):
        """
        Normaliza nombres de tags para usarlos como nombres de archivo
        """
        if not tag_name:
            return "unknown"
        
        # Reemplazar caracteres problemáticos para nombres de archivo
        normalized = tag_name.replace('/', '_').replace('\\', '_').replace(':', '_')
        normalized = normalized.replace('<', '_').replace('>', '_').replace('|', '_')
        normalized = normalized.replace('"', '_').replace('?', '_').replace('*', '_')
        
        return normalized
    
    def _find_local_release_file(self, tag_name):
        """
        Busca un archivo de release por su tag
        """
        normalized_tag = self._normalize_tag_name(tag_name)
        filename = f"release-{normalized_tag}.html"
        
        # Buscar en el directorio de releases
        local_path = self.base_path / 'releases' / 'individual' / filename
        if local_path.exists():
            return str(Path('releases') / 'individual' / filename)
        
        # Si no se encuentra, usar ruta por defecto
        return str(Path('releases') / 'individual' / filename)
    
    def _find_local_tag_file(self, tag_name):
        """
        Busca un archivo de tag por su nombre
        """
        normalized_tag = self._normalize_tag_name(tag_name)
        filename = f"tag-{normalized_tag}.html"
        
        # Buscar en el directorio de tags
        local_path = self.base_path / 'tags' / 'individual' / filename
        if local_path.exists():
            return str(Path('tags') / 'individual' / filename)
        
        # Si no se encuentra, usar ruta por defecto
        return str(Path('tags') / 'individual' / filename)
    
    def _normalize_tag_name(self, tag_name):
        """
        Normaliza nombres de tags para usarlos como nombres de archivo
        """
        if not tag_name:
            return "unknown"
        
        # Reemplazar caracteres problemáticos para nombres de archivo
        normalized = tag_name.replace('/', '_').replace('\\', '_').replace(':', '_')
        normalized = normalized.replace('<', '_').replace('>', '_').replace('|', '_')
        normalized = normalized.replace('"', '_').replace('?', '_').replace('*', '_')
        
        return normalized
    
    def _should_process_url(self, url):
        """
        Determina si una URL debe ser procesada para reescritura
        """
        if not url or not isinstance(url, str):
            return False
        
        # Ignorar tipos de enlaces que no deben modificarse
        ignore_prefixes = ('#', 'mailto:', 'javascript:', 'data:', 'tel:', 'ftp:')
        if url.startswith(ignore_prefixes):
            return False
        
        # Ignorar URLs muy cortas o con caracteres especiales problemáticos
        if len(url.strip()) < 2:
            return False
        
        return True
    
    def rewrite_github_url(self, url, current_file_path):
        """
        Convierte una URL de GitHub a una ruta local relativa
        CON MANEJO ROBUSTO DE ERRORES Y CASOS ESPECIALES
        """
        if not self._should_process_url(url):
            return url
        
        original_url = url.strip()
        
        # Normalizar URL - convertir URLs absolutas a rutas relativas
        fragment = ""
        if url.startswith('http'):
            try:
                parsed = urlparse(url)
                if parsed.netloc != 'github.com':
                    return url  # URL externa, no modificar
                url_path = parsed.path
                fragment = f"#{parsed.fragment}" if parsed.fragment else ""
            except Exception:
                return url  # URL mal formada
        elif url.startswith('/'):
            url_path = url.split('#')[0]  # Remover fragmentos para procesamiento
            if '#' in url:
                fragment = f"#{url.split('#', 1)[1]}"
        else:
            return url  # URL relativa, no modificar
        
        # Verificar si pertenece al repositorio correcto
        repo_prefix = f"/{self.repo_info['owner']}/{self.repo_info['repo']}"
        if not url_path.startswith(repo_prefix):
            return url
        
        # Remover prefijo del repositorio
        relative_path = url_path[len(repo_prefix):]
        
        # 🔧 APLICAR PATRONES CON MANEJO DE ERRORES ROBUSTO
        for pattern, resolver in self.url_patterns:
            try:
                match = pattern.search(relative_path)
                if match:
                    if callable(resolver):
                        local_path = resolver(match, current_file_path)
                    else:
                        local_path = resolver
                    
                    # Calcular ruta relativa desde el archivo actual
                    return self._calculate_relative_path(
                        local_path, current_file_path, fragment
                    )
                        
            except Exception as e:
                print(f"DEBUG: Error en patrón {pattern.pattern} para URL {original_url}: {e}", flush=True)
                continue
        
        # 🆕 CASOS ESPECIALES PARA PÁGINA PRINCIPAL
        if relative_path in ['', '/', '#start-of-content'] or relative_path.startswith('#'):
            return self._calculate_relative_path('index.html', current_file_path, fragment)
        
        # Si no coincide con ningún patrón, devolver URL original
        return url
    
    def _calculate_relative_path(self, local_path, current_file_path, fragment=""):
        """
        Calcula la ruta relativa desde el archivo actual al archivo objetivo
        """
        try:
            current_dir = Path(current_file_path).parent
            target_path = self.base_path / local_path
            
            # Verificar si el archivo objetivo existe
            if target_path.exists():
                relative_to_current = os.path.relpath(target_path, self.base_path / current_dir)
                result = relative_to_current.replace('\\', '/') + fragment
                return result
            else:
                # Si el archivo no existe, usar la ruta calculada de todas formas
                relative_to_current = os.path.relpath(target_path, self.base_path / current_dir)
                result = relative_to_current.replace('\\', '/') + fragment
                return result
                
        except Exception as e:
            print(f"DEBUG: Error calculando ruta relativa: {e}", flush=True)
            # Fallback: usar ruta simple
            return str(local_path).replace('\\', '/') + fragment
    
    def process_html_file(self, file_path):
        """
        Procesa un archivo HTML y reescribe enlaces de GitHub
        CON PROCESAMIENTO OPTIMIZADO Y ESTADÍSTICAS DETALLADAS
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Verificar que el archivo tiene contenido HTML válido
            if not content.strip() or '<html' not in content.lower():
                print(f"⚠️ Archivo sin contenido HTML válido: {file_path}", flush=True)
                return 0
            
            # Usar parser más permisivo para HTML de GitHub
            soup = BeautifulSoup(content, 'html.parser')
            
            relative_file_path = Path(file_path).relative_to(self.base_path)
            links_modified = 0
            links_processed = 0
            github_links_found = 0
            
            # Procesar enlaces <a href="...">
            for link in soup.find_all('a', href=True):
                original_href = link['href']
                links_processed += 1
                
                # Contar enlaces de GitHub
                if 'github.com' in original_href or original_href.startswith('/'):
                    github_links_found += 1
                
                try:
                    new_href = self.rewrite_github_url(original_href, relative_file_path)
                    
                    if new_href != original_href:
                        link['href'] = new_href
                        links_modified += 1
                        
                        # Mostrar ejemplos de enlaces modificados
                        if links_modified <= 2:
                            print(f"  🔗 {original_href} → {new_href}", flush=True)
                        elif links_modified == 3:
                            print(f"  🔗 ... y más enlaces", flush=True)
                            
                except Exception as e:
                    print(f"DEBUG: Error procesando enlace {original_href}: {e}", flush=True)
                    continue
            
            # Procesar formularios si los hay
            for form in soup.find_all('form', action=True):
                original_action = form['action']
                try:
                    new_action = self.rewrite_github_url(original_action, relative_file_path)
                    
                    if new_action != original_action:
                        form['action'] = new_action
                        links_modified += 1
                except Exception as e:
                    print(f"DEBUG: Error procesando formulario {original_action}: {e}", flush=True)
                    continue
            
            # Guardar archivo solo si se modificó
            if links_modified > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                
                print(f"✅ {links_modified}/{github_links_found} enlaces GitHub reescritos en {relative_file_path.name}", flush=True)
            else:
                if github_links_found > 0:
                    print(f"ℹ️ {github_links_found} enlaces GitHub encontrados pero no modificados en {relative_file_path.name}", flush=True)
                else:
                    print(f"ℹ️ No se encontraron enlaces GitHub en {relative_file_path.name}", flush=True)
            
            return links_modified
            
        except Exception as e:
            print(f"❌ Error procesando {file_path}: {e}", flush=True)
            return 0
    
    def rewrite_all_links(self):
        """
        Procesa todos los archivos HTML para reescribir enlaces
        CON PROCESAMIENTO INTELIGENTE Y ESTADÍSTICAS COMPLETAS
        """
        print("🔗 Iniciando reescritura de enlaces para navegación offline...", flush=True)
        
        total_files = 0
        total_links = 0
        
        # Encontrar todos los archivos HTML
        html_files = list(self.base_path.glob('**/*.html'))
        
        if not html_files:
            print("⚠️ No se encontraron archivos HTML para procesar", flush=True)
            return 0, 0
        
        # Separar archivos por tipo para procesamiento optimizado
        listing_files = []
        individual_files = []
        other_files = []
        
        for html_file in html_files:
            file_str = str(html_file)
            if 'individual' in file_str:
                individual_files.append(html_file)
            elif any(x in file_str for x in ['page-', 'index.html']):
                listing_files.append(html_file)
            else:
                other_files.append(html_file)
        
        # Procesar en orden lógico: otros, listados, individuales
        processing_order = [
            ("Archivos principales", other_files),
            ("Páginas de listado", listing_files), 
            ("Elementos individuales", individual_files)
        ]
        
        for category_name, file_list in processing_order:
            if file_list:
                print(f"\n📄 Procesando {category_name} ({len(file_list)} archivos)...")
                
                for html_file in file_list:
                    if html_file.is_file():
                        total_files += 1
                        links_modified = self.process_html_file(html_file)
                        total_links += links_modified
        
        print(f"\n📊 Reescritura completada:")
        print(f"  📁 Archivos procesados: {total_files}")
        print(f"  🔗 Enlaces reescritos: {total_links}")
        
        if total_links > 0:
            print(f"  ✅ Navegación offline configurada exitosamente")
        else:
            print(f"  ⚠️ No se reescribieron enlaces - verificar configuración")
        
        return total_files, total_links
    
    def create_link_map_debug(self):
        """
        Crea un archivo de debug con información completa del mapeo
        """
        debug_file = self.base_path / "offline_navigation_debug.txt"
        
        try:
            with open(debug_file, 'w', encoding='utf-8') as f:
                f.write("NAVEGACIÓN OFFLINE - REPORTE COMPLETO\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"Repositorio: {self.github_base_url}\n")
                f.write(f"Directorio local: {self.base_path}\n")
                f.write(f"Fecha de procesamiento: {__import__('datetime').datetime.now()}\n\n")
                
                # Estadísticas de archivos
                html_files = list(self.base_path.glob('**/*.html'))
                f.write(f"ESTADÍSTICAS DE ARCHIVOS:\n")
                f.write("-" * 40 + "\n")
                f.write(f"Total de archivos HTML: {len(html_files)}\n\n")
                
                # Desglose por secciones
                sections = ['issues', 'pulls', 'releases', 'tags', 'wiki', 'projects', 'insights']
                for section in sections:
                    section_path = self.base_path / section
                    if section_path.exists():
                        f.write(f"{section.upper()}:\n")
                        
                        if section in ['issues', 'pulls']:
                            for state in ['open', 'closed']:
                                state_path = section_path / state
                                if state_path.exists():
                                    # Páginas de listado
                                    listing_files = list(state_path.glob('page-*.html'))
                                    f.write(f"  📋 {state} - Listados: {len(listing_files)}\n")
                                    
                                    # Issues individuales
                                    individual_path = state_path / 'individual'
                                    if individual_path.exists():
                                        individual_files = list(individual_path.glob('issue-*.html'))
                                        f.write(f"  📄 {state} - Individuales: {len(individual_files)}\n")
                        elif section in ['releases', 'tags']:
                            # Páginas de listado
                            listing_files = list(section_path.glob('page-*.html'))
                            f.write(f"  📋 Listados: {len(listing_files)}\n")
                            
                            # Individuales
                            individual_path = section_path / 'individual'
                            if individual_path.exists():
                                if section == 'releases':
                                    individual_files = list(individual_path.glob('release-*.html'))
                                else:
                                    individual_files = list(individual_path.glob('tag-*.html'))
                                f.write(f"  📄 Individuales: {len(individual_files)}\n")
                        else:
                            section_files = list(section_path.glob('**/*.html'))
                            f.write(f"  📄 Archivos: {len(section_files)}\n")
                        
                        f.write("\n")
                
                # Patrones de reescritura
                f.write("PATRONES DE REESCRITURA CONFIGURADOS:\n")
                f.write("-" * 40 + "\n")
                for i, (pattern, _) in enumerate(self.url_patterns, 1):
                    f.write(f"{i:2d}. {pattern.pattern}\n")
                
                f.write(f"\n" + "=" * 60 + "\n")
                f.write("Para verificar la navegación offline, abra navigation.html en su navegador.\n")
            
            print(f"📋 Reporte de debug creado: {debug_file.name}", flush=True)
            
        except Exception as e:
            print(f"⚠️ Error creando reporte de debug: {e}", flush=True)
    
    def validate_offline_navigation(self):
        """
        Valida que la navegación offline esté funcionando correctamente
        """
        print("🔍 Validando navegación offline...", flush=True)
        
        issues_found = 0
        critical_files = ['index.html', 'navigation.html']
        
        # Verificar archivos críticos
        for filename in critical_files:
            file_path = self.base_path / filename
            if not file_path.exists():
                print(f"❌ Archivo crítico faltante: {filename}", flush=True)
                issues_found += 1
            else:
                print(f"✅ Archivo crítico encontrado: {filename}", flush=True)
        
        # Verificar estructura de directorios
        expected_dirs = ['issues/open', 'issues/closed', 'pulls/open', 'pulls/closed', 'releases', 'tags']
        for dir_path in expected_dirs:
            full_path = self.base_path / dir_path
            if full_path.exists():
                files_count = len(list(full_path.glob('*.html')))
                print(f"✅ Directorio {dir_path}: {files_count} archivos", flush=True)
            else:
                print(f"⚠️ Directorio opcional faltante: {dir_path}", flush=True)
        
        if issues_found == 0:
            print("🎉 Navegación offline validada exitosamente", flush=True)
        else:
            print(f"⚠️ Se encontraron {issues_found} problemas en la navegación offline", flush=True)
        
        return issues_found == 0
#!/usr/bin/env python3
"""
Generador de navegación offline con soporte completo para releases y tags
"""

import os
from pathlib import Path
from datetime import datetime

class OfflineNavigator:
    """
    Genera páginas de navegación para el contenido offline
    """
    
    @staticmethod
    def generate_navigation_index(repo_name, content_structure, base_path):
        """
        Genera el índice principal de navegación HTML con releases y tags
        """
        navigation_file = os.path.join(base_path, "navigation.html")
        
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 {repo_name} - Navegación Offline</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 40px;
            font-size: 1.1em;
        }}
        
        .navigation-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }}
        
        .nav-section {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            border-left: 5px solid #3498db;
            transition: all 0.3s ease;
        }}
        
        .nav-section:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .nav-section.issues {{ border-left-color: #e74c3c; }}
        .nav-section.pulls {{ border-left-color: #2ecc71; }}
        .nav-section.releases {{ border-left-color: #f39c12; }}
        .nav-section.tags {{ border-left-color: #9b59b6; }}
        .nav-section.other {{ border-left-color: #34495e; }}
        
        .nav-title {{
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .nav-links {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .nav-links li {{
            margin-bottom: 10px;
        }}
        
        .nav-links a {{
            text-decoration: none;
            color: #2c3e50;
            padding: 8px 12px;
            border-radius: 5px;
            display: block;
            transition: all 0.2s ease;
            border: 1px solid transparent;
        }}
        
        .nav-links a:hover {{
            background: #3498db;
            color: white;
            transform: translateX(5px);
        }}
        
        .nav-stats {{
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 10px;
            padding: 10px;
            background: #ecf0f1;
            border-radius: 5px;
        }}
        
        .main-link {{
            background: #3498db;
            color: white !important;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 8px;
            display: block;
            text-decoration: none;
            font-size: 1.1em;
        }}
        
        .main-link:hover {{
            background: #2980b9;
            transform: none;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 {repo_name}</h1>
        <p class="subtitle">Navegación Offline Completa</p>
        
        <a href="index.html" class="main-link">🏠 Página Principal del Repositorio</a>
        
        <div class="navigation-grid">
        """
        
        # Sección de Issues
        if any('issues' in key for key in content_structure.keys()):
            html_content += """
            <div class="nav-section issues">
                <div class="nav-title">🐛 Issues</div>
                <ul class="nav-links">"""
            
            issues_open = content_structure.get('issues_open', [])
            issues_closed = content_structure.get('issues_closed', [])
            
            if issues_open:
                item = issues_open[0]
                html_content += f'<li><a href="issues/open/page-1.html">📋 Issues Abiertos</a></li>'
                if item.get('individual_count', 0) > 0:
                    html_content += f'<li><a href="issues/open/individual/">📄 Issues Individuales ({item["individual_count"]})</a></li>'
            
            if issues_closed:
                item = issues_closed[0]
                html_content += f'<li><a href="issues/closed/page-1.html">✅ Issues Cerrados</a></li>'
                if item.get('individual_count', 0) > 0:
                    html_content += f'<li><a href="issues/closed/individual/">📄 Issues Individuales ({item["individual_count"]})</a></li>'
            
            total_issues = sum(item.get('individual_count', 0) for item in issues_open + issues_closed)
            html_content += f"""
                </ul>
                <div class="nav-stats">📊 Total: {total_issues} issues descargados</div>
            </div>"""
        
        # Sección de Pull Requests
        if any('pulls' in key for key in content_structure.keys()):
            html_content += """
            <div class="nav-section pulls">
                <div class="nav-title">🔄 Pull Requests</div>
                <ul class="nav-links">"""
            
            pulls_open = content_structure.get('pulls_open', [])
            pulls_closed = content_structure.get('pulls_closed', [])
            
            if pulls_open:
                item = pulls_open[0]
                html_content += f'<li><a href="pulls/open/page-1.html">📋 PRs Abiertos</a></li>'
                if item.get('individual_count', 0) > 0:
                    html_content += f'<li><a href="pulls/open/individual/">📄 PRs Individuales ({item["individual_count"]})</a></li>'
            
            if pulls_closed:
                item = pulls_closed[0]
                html_content += f'<li><a href="pulls/closed/page-1.html">✅ PRs Cerrados</a></li>'
                if item.get('individual_count', 0) > 0:
                    html_content += f'<li><a href="pulls/closed/individual/">📄 PRs Individuales ({item["individual_count"]})</a></li>'
            
            total_pulls = sum(item.get('individual_count', 0) for item in pulls_open + pulls_closed)
            html_content += f"""
                </ul>
                <div class="nav-stats">📊 Total: {total_pulls} pull requests descargados</div>
            </div>"""
        
        # 🆕 SECCIÓN DE RELEASES
        if 'releases' in content_structure:
            releases_info = content_structure['releases'][0]
            html_content += f"""
            <div class="nav-section releases">
                <div class="nav-title">🚀 Releases</div>
                <ul class="nav-links">
                    <li><a href="releases/page-1.html">📋 Lista de Releases</a></li>"""
            
            if releases_info.get('individual_count', 0) > 0:
                html_content += f'<li><a href="releases/individual/">📦 Releases Individuales ({releases_info["individual_count"]})</a></li>'
            
            html_content += f"""
                </ul>
                <div class="nav-stats">📊 Total: {releases_info.get('individual_count', 0)} releases descargados</div>
            </div>"""
        
        # 🆕 SECCIÓN DE TAGS
        if 'tags' in content_structure:
            tags_info = content_structure['tags'][0]
            html_content += f"""
            <div class="nav-section tags">
                <div class="nav-title">🏷️ Tags</div>
                <ul class="nav-links">
                    <li><a href="tags/page-1.html">📋 Lista de Tags</a></li>"""
            
            if tags_info.get('individual_count', 0) > 0:
                html_content += f'<li><a href="tags/individual/">🔖 Tags Individuales ({tags_info["individual_count"]})</a></li>'
            
            html_content += f"""
                </ul>
                <div class="nav-stats">📊 Total: {tags_info.get('individual_count', 0)} tags descargados</div>
            </div>"""
        
        # Otras secciones
        other_sections = []
        for section in ['wiki', 'projects', 'insights']:
            if section in content_structure:
                other_sections.append((section, content_structure[section][0]))
        
        if other_sections:
            html_content += """
            <div class="nav-section other">
                <div class="nav-title">📚 Otras Secciones</div>
                <ul class="nav-links">"""
            
            section_icons = {
                'wiki': '📖',
                'projects': '📊', 
                'insights': '📈'
            }
            
            for section, info in other_sections:
                icon = section_icons.get(section, '📄')
                html_content += f'<li><a href="{section}/page-1.html">{icon} {section.capitalize()}</a></li>'
            
            html_content += """
                </ul>
                <div class="nav-stats">🔧 Secciones adicionales del repositorio</div>
            </div>"""
        
        # Cerrar HTML
        html_content += f"""
        </div>
        
        <div class="footer">
            <p>📅 Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>🌐 Navegación offline completa para <strong>{repo_name}</strong></p>
            <p>💡 Todos los enlaces funcionan sin conexión a internet</p>
        </div>
    </div>
</body>
</html>"""
        
        # Escribir archivo
        with open(navigation_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📋 Índice de navegación generado: {navigation_file}")
        
        # 🆕 GENERAR ÍNDICES PARA RELEASES Y TAGS
        OfflineNavigator._generate_releases_index(base_path, content_structure)
        OfflineNavigator._generate_tags_index(base_path, content_structure)
    
    @staticmethod
    def _generate_releases_index(base_path, content_structure):
        """Genera índice específico para releases individuales"""
        releases_individual_dir = os.path.join(base_path, "releases", "individual")
        
        if not os.path.exists(releases_individual_dir):
            return
        
        index_file = os.path.join(releases_individual_dir, "index.html")
        
        # Buscar archivos de releases
        release_files = []
        for file in os.listdir(releases_individual_dir):
            if file.startswith('release-') and file.endswith('.html'):
                tag_name = file[8:-5]  # Remover 'release-' y '.html'
                release_files.append((tag_name, file))
        
        release_files.sort(reverse=True)  # Más recientes primero
        
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Releases Individuales</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #f39c12; }}
        .release-item {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #f39c12; }}
        .release-item a {{ text-decoration: none; color: #2c3e50; font-weight: bold; }}
        .release-item a:hover {{ color: #f39c12; }}
        .back-link {{ background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <a href="../../navigation.html" class="back-link">← Volver a Navegación</a>
    <h1>🚀 Releases Individuales</h1>
    <p>📦 {len(release_files)} releases descargados</p>
    """
        
        for tag_name, filename in release_files:
            html_content += f"""
            <div class="release-item">
                <a href="{filename}">🚀 Release {tag_name}</a>
            </div>"""
        
        html_content += """
</body>
</html>"""
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    @staticmethod
    def _generate_tags_index(base_path, content_structure):
        """Genera índice específico para tags individuales"""
        tags_individual_dir = os.path.join(base_path, "tags", "individual")
        
        if not os.path.exists(tags_individual_dir):
            return
        
        index_file = os.path.join(tags_individual_dir, "index.html")
        
        # Buscar archivos de tags
        tag_files = []
        for file in os.listdir(tags_individual_dir):
            if file.startswith('tag-') and file.endswith('.html'):
                tag_name = file[4:-5]  # Remover 'tag-' y '.html'
                tag_files.append((tag_name, file))
        
        tag_files.sort(reverse=True)  # Más recientes primero
        
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏷️ Tags Individuales</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
        h1 {{ color: #9b59b6; }}
        .tag-item {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #9b59b6; }}
        .tag-item a {{ text-decoration: none; color: #2c3e50; font-weight: bold; }}
        .tag-item a:hover {{ color: #9b59b6; }}
        .back-link {{ background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <a href="../../navigation.html" class="back-link">← Volver a Navegación</a>
    <h1>🏷️ Tags Individuales</h1>
    <p>🔖 {len(tag_files)} tags descargados</p>
    """
        
        for tag_name, filename in tag_files:
            html_content += f"""
            <div class="tag-item">
                <a href="{filename}">🏷️ Tag {tag_name}</a>
            </div>"""
        
        html_content += """
</body>
</html>"""
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
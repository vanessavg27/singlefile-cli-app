#!/usr/bin/env python3
"""
Parser de URLs de GitHub con soporte completo para releases y tags
"""

import re
from urllib.parse import urljoin

class GitHubParser:
    """
    Utilidades para parsear URLs de GitHub y generar URLs de contenido
    """
    
    @staticmethod
    def parse_repo_url(github_url):
        """
        Parsea una URL de repositorio de GitHub y extrae información básica
        """
        # Limpiar URL
        github_url = github_url.strip().rstrip('/')
        
        # Patrón para repositorios de GitHub
        pattern = r'https?://github\.com/([^/]+)/([^/]+)(?:/.*)?'
        match = re.match(pattern, github_url)
        
        if not match:
            raise ValueError(f"URL de GitHub inválida: {github_url}")
        
        owner = match.group(1)
        repo = match.group(2)
        
        return {
            'owner': owner,
            'repo': repo,
            'full_name': f"{owner}/{repo}",
            'base_url': f"https://github.com/{owner}/{repo}"
        }
    
    @staticmethod
    def get_content_urls(repo_info):
        """
        Genera todas las URLs de contenido para un repositorio
        INCLUYENDO RELEASES Y TAGS
        """
        base_url = repo_info['base_url']
        
        urls = {
            # Página principal
            'home': base_url,
            
            # Issues
            'issues_open': f"{base_url}/issues?state=open",
            'issues_closed': f"{base_url}/issues?state=closed",
            
            # Pull Requests
            'pulls_open': f"{base_url}/pulls?state=open", 
            'pulls_closed': f"{base_url}/pulls?state=closed",
            
            # 🆕 RELEASES Y TAGS
            'releases': f"{base_url}/releases",
            'tags': f"{base_url}/tags",
            
            # Otras secciones
            'wiki': f"{base_url}/wiki",
            'projects': f"{base_url}/projects",
            'insights': f"{base_url}/pulse",
        }
        
        return urls
    
    @staticmethod
    def get_paginated_url(base_url, page_number):
        """
        Genera URL paginada para cualquier sección
        """
        separator = '&' if '?' in base_url else '?'
        return f"{base_url}{separator}page={page_number}"
    
    @staticmethod
    def extract_release_tag_from_url(url):
        """
        Extrae el tag de una URL de release individual
        Ejemplo: https://github.com/user/repo/releases/tag/v1.0.0 -> v1.0.0
        """
        pattern = r'/releases/tag/([^/?#]+)'
        match = re.search(pattern, url)
        return match.group(1) if match else None
    
    @staticmethod
    def extract_tag_from_url(url):
        """
        Extrae el tag de una URL de tag individual
        Ejemplo: https://github.com/user/repo/tree/v1.0.0 -> v1.0.0
        """
        # Pueden ser URLs como /tree/tagname o /releases/tag/tagname
        patterns = [
            r'/tree/([^/?#]+)',
            r'/releases/tag/([^/?#]+)',
            r'/tags/([^/?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def is_release_url(url):
        """
        Determina si una URL es de un release individual
        """
        return '/releases/tag/' in url
    
    @staticmethod
    def is_tag_url(url):
        """
        Determina si una URL es de un tag individual
        """
        return any(pattern in url for pattern in ['/tree/', '/tags/']) and '/releases/tag/' not in url
    
    @staticmethod
    def normalize_tag_name(tag_name):
        """
        Normaliza nombres de tags para usarlos como nombres de archivo
        Reemplaza caracteres problemáticos
        """
        if not tag_name:
            return "unknown"
        
        # Reemplazar caracteres problemáticos para nombres de archivo
        normalized = tag_name.replace('/', '_').replace('\\', '_').replace(':', '_')
        normalized = normalized.replace('<', '_').replace('>', '_').replace('|', '_')
        normalized = normalized.replace('"', '_').replace('?', '_').replace('*', '_')
        
        return normalized
    
    @staticmethod
    def generate_release_urls(repo_info):
        """
        Genera URLs específicas para releases
        """
        base_url = repo_info['base_url']
        
        return {
            'releases_list': f"{base_url}/releases",
            'releases_latest': f"{base_url}/releases/latest",
            'tags_list': f"{base_url}/tags"
        }
    
    @staticmethod
    def build_release_individual_url(repo_info, tag_name):
        """
        Construye la URL de un release individual
        """
        base_url = repo_info['base_url']
        return f"{base_url}/releases/tag/{tag_name}"
    
    @staticmethod
    def build_tag_individual_url(repo_info, tag_name):
        """
        Construye la URL de un tag individual (árbol de archivos)
        """
        base_url = repo_info['base_url']
        return f"{base_url}/tree/{tag_name}"
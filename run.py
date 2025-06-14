#!/usr/bin/env python3
import argparse
from src.github_offline import GitHubOfflineAutomation
import sys # Añade esta importación

def main():
    print("DEBUG: Iniciando script run.py.", flush=True) # <-- NUEVO PRINT
    parser = argparse.ArgumentParser(description='GitHub Offline Automation')
    parser.add_argument('url', help='URL del repositorio de GitHub')
    parser.add_argument('--profile', help='Nombre del perfil de Chrome a usar')
    parser.add_argument('--headless', action='store_true', help='Ejecutar en modo headless')
    parser.add_argument('--delay', type=float, default=3.0, help='Retardo entre descargas en segundos')
    
    args = parser.parse_args()
    
    automation = GitHubOfflineAutomation(
        args.url,
        profile=args.profile,
        headless=args.headless,
        download_delay=args.delay
    )
    automation.run()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Selector de usuarios/perfiles de Chrome para la descarga
Permite elegir qué perfil usar antes de iniciar el proceso
"""

import os
import json
from pathlib import Path

class ChromeUserSelector:
    """
    Permite seleccionar qué perfil de Chrome usar para la descarga
    """
    
    def __init__(self):
        self.chrome_user_data_dir = self._get_chrome_user_data_dir()
        self.available_profiles = []
    
    def _get_chrome_user_data_dir(self):
        """Obtiene el directorio de datos de usuario de Chrome según el SO"""
        if os.name == 'nt':  # Windows
            base_path = os.path.expanduser(r'~\AppData\Local\Google\Chrome\User Data')
        elif os.uname().sysname == 'Darwin':  # macOS
            base_path = os.path.expanduser('~/Library/Application Support/Google/Chrome')
        else:  # Linux
            base_path = os.path.expanduser('~/.config/google-chrome')
        
        return Path(base_path)
    
    def scan_chrome_profiles(self):
        """
        Escanea y encuentra todos los perfiles de Chrome disponibles
        """
        profiles = []
        
        if not self.chrome_user_data_dir.exists():
            print(f"❌ Directorio de Chrome no encontrado: {self.chrome_user_data_dir}")
            return profiles
        
        print(f"🔍 Escaneando perfiles en: {self.chrome_user_data_dir}")
        
        # Buscar perfil por defecto
        default_profile = self.chrome_user_data_dir / "Default"
        print(default_profile)
        if default_profile.exists():
            profile_info = self._get_profile_info(default_profile, "Default")
            if profile_info:
                profiles.append(profile_info)
        # Buscar otros perfiles (Profile 1, Profile 2, etc.)
        for profile_dir in self.chrome_user_data_dir.iterdir():
            if profile_dir.is_dir() and profile_dir.name.startswith("Profile "):
                print(f"Directory: {profile_dir.name}")
                profile_info = self._get_profile_info(profile_dir, profile_dir.name)
                if profile_info:
                    profiles.append(profile_info)
        print("Perfiles causita:",profiles)
        self.available_profiles = profiles
        return profiles
    
    def _get_profile_info(self, profile_path, profile_name):
        """
        Obtiene información detallada de un perfil específico
        """
        try:
            # Leer archivo de preferencias para obtener el nombre del usuario
            prefs_file = profile_path / "Preferences"
            
            profile_info = {
                'name': profile_name,
                'path': str(profile_path),
                'display_name': profile_name,
                'email': 'No disponible',
                'last_used': 'Desconocido',
                'is_default': profile_name == "Default"
            }
            
            if prefs_file.exists():
                try:
                    with open(prefs_file, 'r', encoding='utf-8') as f:
                        prefs = json.load(f)
                    
                    # Extraer nombre de usuario si está disponible
                    if 'profile' in prefs:
                        profile_data = prefs['profile']
                        
                        # Nombre del perfil
                        if 'name' in profile_data:
                            profile_info['display_name'] = profile_data['name']
                        
                        # Email asociado (si está logueado en Google)
                        if 'google_services' in profile_data:
                            google_services = profile_data['google_services']
                            if 'username' in google_services:
                                profile_info['email'] = google_services['username']
                    
                    # Información de cuenta de Google si está disponible
                    if 'account_info' in prefs:
                        accounts = prefs['account_info']
                        if accounts:

                            if isinstance(accounts, dict):
                                first_account = list(accounts.values())[0]
                            elif isinstance(accounts, list):
                                first_account = accounts[0]
                            if 'email' in first_account:
                                profile_info['email'] = first_account['email']
                
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"DEBUG: Error leyendo preferencias de {profile_name}: {e}")
            
            # Verificar si tiene historial (indicador de uso)
            history_file = profile_path / "History"
            if history_file.exists():
                stat = history_file.stat()
                import datetime
                last_modified = datetime.datetime.fromtimestamp(stat.st_mtime)
                profile_info['last_used'] = last_modified.strftime("%Y-%m-%d %H:%M")
            
            return profile_info
            
        except Exception as e:
            print(f"DEBUG: Error obteniendo info de {profile_name}: {e}")
            return None
    
    def display_profiles_menu(self):
        """
        Muestra un menú interactivo para seleccionar perfil
        """
        profiles = self.scan_chrome_profiles()
        
        if not profiles:
            print("❌ No se encontraron perfiles de Chrome")
            print("💡 Asegúrate de que Chrome esté instalado y se haya usado al menos una vez")
            return None
        
        print("\n" + "="*80)
        print("🌐 SELECTOR DE PERFIL DE CHROME")
        print("="*80)
        
        print(f"📁 Directorio de Chrome: {self.chrome_user_data_dir}")
        print(f"📊 Perfiles encontrados: {len(profiles)}\n")
        
        # Mostrar lista de perfiles
        for i, profile in enumerate(profiles, 1):
            print(f"{i}. 👤 {profile['display_name']}")
            print(f"   📧 Email: {profile['email']}")
            print(f"   📁 Carpeta: {profile['name']}")
            print(f"   🕒 Último uso: {profile['last_used']}")
            if profile['is_default']:
                print("   ⭐ Perfil por defecto")
            print()
        
        # Agregar opción para perfil temporal
        print(f"{len(profiles) + 1}. 🔒 Usar perfil temporal (sin datos personales)")
        print("   📧 Sin sesiones guardadas")
        print("   📁 Directorio temporal")
        print("   🕒 Solo para esta sesión")
        print()
        
        # Solicitar selección
        while True:
            try:
                choice = input(f"👉 Selecciona un perfil (1-{len(profiles) + 1}): ").strip()
                
                if choice.isdigit():
                    choice_num = int(choice)
                    
                    if 1 <= choice_num <= len(profiles):
                        selected_profile = profiles[choice_num - 1]
                        print(f"\n✅ Perfil seleccionado: {selected_profile['display_name']}")
                        print(f"📧 Email: {selected_profile['email']}")
                        print(f"📁 Ruta: {selected_profile['path']}")
                        return selected_profile
                    
                    elif choice_num == len(profiles) + 1:
                        print("\n✅ Usando perfil temporal")
                        print("🔒 Se creará un perfil limpio sin datos personales")
                        return {'name': 'Temporal', 'path': None, 'display_name': 'Perfil Temporal'}
                    
                    else:
                        print(f"❌ Opción inválida. Ingresa un número entre 1 y {len(profiles) + 1}")
                
                else:
                    print("❌ Por favor ingresa un número válido")
                    
            except KeyboardInterrupt:
                print("\n\n❌ Operación cancelada por el usuario")
                return None
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def get_chrome_args_for_profile(self, selected_profile):
        """
        Genera argumentos de Chrome para el perfil seleccionado
        CON COPIA SEGURA PARA EVITAR CONFLICTOS
        """
        if not selected_profile or selected_profile['path'] is None:
            # Perfil temporal limpio
            import tempfile
            temp_dir = tempfile.mkdtemp(prefix="chrome_temp_github_")
            print(f"📁 Creando perfil temporal limpio en: {temp_dir}")
            return [f"--user-data-dir={temp_dir}"]
        
        # 🔧 SOLUCIÓN: Crear copia segura del perfil existente
        return self._create_safe_profile_copy(selected_profile)
    
    def _create_safe_profile_copy(self, selected_profile):
        """
        Crea una copia segura del perfil para evitar conflictos con Chrome abierto
        """
        import tempfile
        import shutil
        
        try:
            profile_name = selected_profile['name']
            original_profile_path = Path(selected_profile['path'])
            
            print(f"🔄 Creando copia segura del perfil: {profile_name}")
            
            # Crear directorio temporal para la copia
            temp_base_dir = tempfile.mkdtemp(prefix=f"chrome_profile_github_{profile_name}_")
            temp_profile_path = Path(temp_base_dir) / profile_name
            
            print(f"📂 Copiando perfil desde: {original_profile_path}")
            print(f"📂 Hacia directorio temporal: {temp_profile_path}")
            
            # Copiar perfil completo (esto puede tomar unos segundos)
            print("⏳ Copiando archivos del perfil... (esto puede tardar un momento)")
            
            # Copiar con manejo de errores robusto
            self._safe_copy_profile(original_profile_path, temp_profile_path)
            
            print(f"✅ Copia del perfil completada exitosamente")
            print(f"🔒 Chrome usará la copia aislada, sin afectar tu perfil original")
            
            # Configurar argumentos de Chrome para usar la copia
            chrome_args = [
                f"--user-data-dir={temp_base_dir}",
                f"--profile-directory={profile_name}",
                # Argumentos adicionales para estabilidad
                "--no-first-run",
                "--disable-default-apps",
                "--disable-background-mode",
                "--disable-background-timer-throttling"
            ]
            
            return chrome_args
            
        except Exception as e:
            print(f"❌ Error creando copia del perfil: {e}")
            print("🔄 Fallback: usando perfil temporal limpio")
            
            # Fallback a perfil temporal
            temp_dir = tempfile.mkdtemp(prefix="chrome_fallback_github_")
            return [f"--user-data-dir={temp_dir}"]
    
    def _safe_copy_profile(self, source, destination):
        """
        Copia el perfil de Chrome de manera segura, excluyendo archivos problemáticos
        """
        import shutil
        import os
        
        # Archivos/carpetas que pueden causar problemas y se pueden omitir
        exclude_patterns = {
            'SingletonLock', 'SingletonSocket', 'SingletonCookie',
            'lockfile', '.lock', 'LOCK',
            'LOG', 'LOG.old', 
            'chrome_debug.log',
            'DevToolsActivePort',
            'temp', 'tmp',
            'CrashpadMetrics-active.pma',
            'chrome_shutdown_ms.txt'
        }
        
        def should_exclude(path):
            """Determina si un archivo/carpeta debe excluirse"""
            name = os.path.basename(path)
            return any(pattern in name for pattern in exclude_patterns)
        
        def copy_with_exclusions(src, dst):
            """Copia recursiva con exclusiones"""
            try:
                os.makedirs(dst, exist_ok=True)
                
                for item in os.listdir(src):
                    src_path = os.path.join(src, item)
                    dst_path = os.path.join(dst, item)
                    
                    if should_exclude(src_path):
                        continue  # Saltar archivos problemáticos
                    
                    try:
                        if os.path.isdir(src_path):
                            copy_with_exclusions(src_path, dst_path)
                        else:
                            shutil.copy2(src_path, dst_path)
                    except (OSError, PermissionError) as e:
                        # Saltar archivos que no se pueden copiar (en uso, etc.)
                        print(f"  ⚠️ Saltando archivo en uso: {item}")
                        continue
                        
            except Exception as e:
                print(f"  ❌ Error copiando directorio {src}: {e}")
        
        # Realizar la copia con exclusiones
        copy_with_exclusions(str(source), str(destination))

# Función de utilidad para usar en el flujo principal
def select_chrome_profile():
    """
    Función principal para seleccionar perfil de Chrome
    Retorna el perfil seleccionado y los argumentos de Chrome
    """
    print("🚀 Configurando perfil de Chrome para la descarga...")
    
    selector = ChromeUserSelector()
    selected_profile = selector.display_profiles_menu()
    
    if selected_profile:
        chrome_args = selector.get_chrome_args_for_profile(selected_profile)
        
        print("\n" + "="*80)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("="*80)
        print(f"👤 Perfil: {selected_profile['display_name']}")
        print(f"🔧 Argumentos Chrome: {len(chrome_args)} configurados")
        print("🌐 Chrome usará este perfil para acceder a GitHub")
        print("="*80)
        
        return selected_profile, chrome_args
    else:
        print("❌ No se seleccionó ningún perfil. Usando configuración por defecto.")
        return None, []

if __name__ == "__main__":
    # Prueba del selector
    print("🧪 MODO DE PRUEBA - Selector de perfiles de Chrome")
    profile, args = select_chrome_profile()
    if profile:
        print(f"\n🎯 RESULTADO:")
        print(f"Perfil seleccionado: {profile['display_name']}")
        print(f"Argumentos de Chrome: {args}")
    else:
        print("❌ No se seleccionó perfil")
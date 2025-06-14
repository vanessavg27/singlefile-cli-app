import os
from pathlib import Path

class Config:
    # Configuración de Chrome
    CHROME_PROFILE_PATH = str(Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data")
    CHROME_PROFILE_NAME = "Default"
    
    # Configuración de SingleFile  C:\Users\vanes\Downloads
    #SINGLEFILE_PATH = os.getenv("SINGLEFILE_PATH", "D:\\scripts\\scripts-github-projects\\singlefile-cli-app\\single-file.exe")
    SINGLEFILE_PATH = os.getenv("SINGLEFILE_PATH", "C:\\Users\\vanes\\Downloads\\single-file.exe")
    # Configuración de descargas y delays
    DOWNLOAD_DELAY = 3  # segundos entre descargas
    DEFAULT_DOWNLOAD_DELAY = 3  # Valor por defecto para download_delay
    
    # Directorio base para descargas
    BASE_DOWNLOAD_DIR = str(Path.home() / "Downloads" / "github-offline")
    
    # Configuración de Selenium
    DEFAULT_HEADLESS = False  # Valor por defecto para headless
    PAGE_LOAD_TIMEOUT = 30  # segundos
    
    @staticmethod
    def get_profile_args():
        return [
            f"--user-data-dir={Config.CHROME_PROFILE_PATH}",
            f"--profile-directory={Config.CHROME_PROFILE_NAME}"
        ]
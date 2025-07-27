import sys
import os

def resource_path(relative_path):
    """Получаем абсолютный путь к ресурсу"""
    try:
        base_path = sys._MEIPASS  # Это специальный атрибут, созданный PyInstaller
    except Exception:
        base_path = os.path.abspath('.')
    
    return os.path.join(base_path, relative_path)
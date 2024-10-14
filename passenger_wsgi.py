import sys
import os

# Añadir el path de tu aplicación
sys.path.insert(0, '/home/jaimepar/backend')

# Establecer el entorno
os.environ['FLASK_ENV'] = 'production'

# Importar tu aplicación Flask
from app import app as application  # Asegúrate de que el nombre "app" coincida con tu Flask app en app.py
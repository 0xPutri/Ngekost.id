import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from backend.env import load_environment

load_environment()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.production')

from backend.wsgi import application
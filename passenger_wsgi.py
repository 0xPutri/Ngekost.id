import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from ngekost_backend.env import load_environment

load_environment()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngekost_backend.settings.production')

from ngekost_backend.wsgi import application
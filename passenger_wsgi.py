import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngekost_backend.settings.production')

from ngekost_backend.wsgi import application
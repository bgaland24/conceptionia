"""
Point d'entrée WSGI pour PythonAnywhere.

Configuration sur PythonAnywhere :
  Source code     : /home/<username>/conception
  Working dir     : /home/<username>/conception
  WSGI file       : /home/<username>/conception/wsgi.py
  Python version  : 3.10+

Variables d'environnement à définir dans l'onglet "Web" > "Environment variables" :
  WIKI_USERNAME = admin
  WIKI_PASSWORD = Xk9#mP2$vL5nQ8@w
"""

import sys
import os

# Ajouter le répertoire du projet au path Python
path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.insert(0, path)

# Charger .env si présent (développement local uniquement)
env_file = os.path.join(path, ".env")
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

from app import app as application  # noqa: E402

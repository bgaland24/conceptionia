# Conception SI Semences

Wiki de conception du SI métier d'Entreprise X — contrôle officiel des semences et plants.

Généré avec [MkDocs + Material](https://squidfunk.github.io/mkdocs-material/), servi via Flask avec authentification.

---

## Lancement en local

### Prérequis

- Python 3.10+
- pip

### Installation (une seule fois)

```bash
git clone https://github.com/bgaland24/conceptionia.git
cd conceptionia

# Installer les dépendances
pip install -r requirements.txt -r requirements-docs.txt

# Créer le wsgi.py local (exclu du git) à partir du modèle
cp wsgi.py.example wsgi.py
# Éditer wsgi.py et renseigner WIKI_USERNAME et WIKI_PASSWORD
```

### Option A — Wiki avec authentification (comportement identique à la prod)

```bash
# Générer le site statique
mkdocs build

# Lancer via wsgi.py (qui porte les credentials)
python wsgi.py
```

Ouvrir **http://127.0.0.1:5000** — login demandé au navigateur.

### Option B — Rechargement automatique sans auth (dev contenu)

```bash
mkdocs serve
```

Ouvrir **http://127.0.0.1:8000** — le site se recharge à chaque modification d'un fichier `docs/`.

---

## Déploiement sur PythonAnywhere

### 1. Cloner le projet

Dans une console Bash PythonAnywhere :

```bash
git clone https://github.com/bgaland24/conceptionia.git
cd conceptionia
```

### 2. Installer les dépendances

```bash
pip install --user -r requirements.txt -r requirements-docs.txt
```

### 3. Générer le site statique

```bash
mkdocs build
```

> À relancer après chaque modification du contenu (`docs/`) ou de `mkdocs.yml`.

### 4. Créer le fichier wsgi.py manuellement

`wsgi.py` est exclu du git car il contient les credentials. Le créer directement sur PythonAnywhere :

```python
import sys, os

path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.insert(0, path)

os.environ["WIKI_USERNAME"] = "admin"
os.environ["WIKI_PASSWORD"] = "le_mot_de_passe"

from app import app as application
```

### 5. Configurer l'application web

Dans l'onglet **Web** de PythonAnywhere :

| Champ | Valeur |
|---|---|
| Source code | `/home/<username>/conceptionia` |
| Working directory | `/home/<username>/conceptionia` |
| WSGI configuration file | `/home/<username>/conceptionia/wsgi.py` |
| Python version | 3.10 (ou supérieur) |

### 6. Recharger l'application

Cliquer sur **Reload** dans l'onglet Web.

Le wiki est accessible à l'URL fournie par PythonAnywhere, protégé par login/mot de passe.

### Mettre à jour le contenu

```bash
cd conceptionia
git pull
mkdocs build
# Puis Reload dans l'onglet Web
```

> `wsgi.py` n'est pas écrasé par `git pull` car il est exclu du git.

---

## Structure du projet

```
conceptionia/
├── app.py                  # App Flask (authentification + service fichiers statiques)
├── wsgi.py                 # Credentials + point d'entrée WSGI (exclu du git)
├── mkdocs.yml              # Configuration du wiki MkDocs
├── requirements.txt        # Dépendances Flask
├── requirements-docs.txt   # Dépendances MkDocs
├── site/                   # Site généré par mkdocs build (exclu du git)
└── docs/                   # Sources du wiki
    ├── index.md
    ├── glossaire.md
    ├── conventions.md
    ├── specs/
    ├── bdd/
    ├── api/
    ├── tests/
    ├── guide-utilisateur/
    └── journal-iterations.md
```

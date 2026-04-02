import os
from functools import wraps
from flask import Flask, request, Response, send_from_directory

app = Flask(__name__, static_folder="site")

# Credentials chargés depuis les variables d'environnement (jamais dans le git)
AUTH_USERNAME = os.environ.get("WIKI_USERNAME", "admin")
AUTH_PASSWORD = os.environ.get("WIKI_PASSWORD", "")


def check_auth(username, password):
    return username == AUTH_USERNAME and password == AUTH_PASSWORD


def authenticate():
    return Response(
        "Accès protégé. Veuillez vous authentifier.",
        401,
        {"WWW-Authenticate": 'Basic realm="Wiki SI Semences"'},
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
@requires_auth
def serve(path):
    site_dir = os.path.join(os.path.dirname(__file__), "site")
    # Servir index.html pour les chemins de dossier
    full_path = os.path.join(site_dir, path)
    if os.path.isdir(full_path):
        path = os.path.join(path, "index.html")
    return send_from_directory(site_dir, path)



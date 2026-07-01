"""
Configuration pytest partagée pour la suite de sécurité (perturbation J3).

But : rendre le package Django `backend/` importable depuis ce dossier
`tests/` (situé à la racine du repo, à côté de `backend/` et `frontend/`),
SANS dépendre d'une base de données. Les tests de prompt injection n'exercent
que la génération de quiz (client mock) et sa validation — deux fonctions
pures qui n'ont besoin que de `django.setup()` pour résoudre les imports
relatifs de l'app `llm`.
"""

import os
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# LLM_BACKEND=mock : jamais d'appel réseau/API en CI (mêmes valeurs que ci.yml).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apocal.settings")
os.environ.setdefault("LLM_BACKEND", "mock")

import django  # noqa: E402 (import après le réglage de sys.path/env, nécessaire)

django.setup()

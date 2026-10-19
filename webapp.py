#!/usr/bin/env python3
"""Point d'entrée de l'interface web locale.

Usage :
    python webapp.py                 # http://127.0.0.1:5000
    python webapp.py --port 8080
    python webapp.py --host 0.0.0.0  # accessible sur le réseau local
"""
from __future__ import annotations

import sys

from agent.web import main

if __name__ == "__main__":
    sys.exit(main())

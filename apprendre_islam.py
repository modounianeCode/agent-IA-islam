#!/usr/bin/env python3
"""Agent IA « Apprendre l'Islam » — point d'entrée CLI.

Usage :
    python apprendre_islam.py              # mode interactif
    python apprendre_islam.py coran 2:255  # commande unique
"""
from __future__ import annotations

import sys

from agent.cli import main

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
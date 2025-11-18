#!/usr/bin/env bash
# macOS/Linux launcher
set -e
echo "Installation des dependances..."
pip install -r requirements.txt
echo "Lancement de l'app..."
streamlit run streamlit_app.py

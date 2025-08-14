@echo off
REM === Aller dans le dossier du projet ===
cd /d "C:\Users\PC1\Downloads\pin-collector"

REM === Créer un venv s'il n'existe pas ===
if not exist ".venv" (
    echo Création de l'environnement virtuel...
    py -3.11 -m venv .venv
)

REM === Activer le venv ===
call .venv\Scripts\activate.bat

REM === Mettre à jour pip ===
python -m pip install --upgrade pip

REM === Installer les dépendances ===
if exist requirements.txt (
    echo Installation des dépendances...
    python -m pip install -r requirements.txt
) else (
    echo [ERREUR] requirements.txt introuvable.
    pause
    exit /b 1
)

REM === Lancer l'application Streamlit ===
echo Lancement de Pin Collector...
python -m streamlit run streamlit_app.py

pause

@echo off
REM Lancer Pin Collector sur Windows
echo Installation des dependances...
pip install -r requirements.txt
echo Lancement de l'app...
streamlit run streamlit_app.py
pause

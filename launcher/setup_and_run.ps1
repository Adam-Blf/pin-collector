# PowerShell script to setup and run Pin Collector
Write-Host "Installation des dependances..."
python -m pip install -r requirements.txt
Write-Host "Lancement de l'app..."
streamlit run streamlit_app.py

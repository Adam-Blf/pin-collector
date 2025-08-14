# Pin Collector • mon petit projet data qui fait le taf

Je veux recenser mes pins sans prise de tête. Une interface claire, des filtres, et surtout je peux importer et exporter en Excel. C’est tout. Le reste est bonus.

## Ce que ça fait
- Table éditable en direct
- Import Excel et export Excel
- Filtres simples — recherche, série, collection, échange oui non
- Sauvegarde locale possible dans `data/pins.xlsx`
- Champs conseillés: name, serie, collection, quantity, state, tradeable, price, tags, notes, image_url

## Lancer en 3 lignes
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
# l’app s’ouvre dans le navigateur
```

Si tu préfères être guidé, ouvre `launcher/index.html` — il y a les boutons copier et des scripts prêts pour Windows PowerShell macOS Linux.

## Format Excel
Tu viens avec ton `.xlsx`. L’app aligne les colonnes manquantes et garde les colonnes en plus. Colonnes de base:
- name
- serie
- collection
- quantity
- state
- tradeable
- price
- tags
- notes
- image_url

Un exemple est dispo: `data/sample_pins.xlsx`

## Structure rapide
```
pin-collector/
  ├─ streamlit_app.py
  ├─ requirements.txt
  ├─ data/
  │  └─ sample_pins.xlsx
  └─ launcher/
     ├─ index.html
     ├─ style.css
     ├─ app.js
     ├─ start_windows.bat
     ├─ setup_and_run.ps1
     └─ start_unix.sh
```

## Roadmap perso
- miniatures pour les images
- export CSV
- multi collections
- thème custom

## Licence
MIT. Fais en bon usage.

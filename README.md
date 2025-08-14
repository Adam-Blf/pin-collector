# Pin Collector • projet data simple et clean

Un petit projet pour recenser ma collection de pins avec une interface visuelle.
Objectif: j’édite ma base tranquille, je filtre, j’importe depuis Excel, j’exporte vers Excel. Rien de compliqué. Juste utile.

## Ce que ça fait
- Table éditable en direct
- Import d’un fichier Excel
- Export de la table au format Excel
- Recherche, filtres rapides, tris
- Champs clés: nom, série, collection, quantité, état, échange, prix, tags, notes, image_url
- Sauvegarde locale possible dans `data/pins.xlsx`

## Lancer le projet
1. Crée un venv si tu veux
2. Installe les deps  
```bash
pip install -r requirements.txt
```
3. Lance l’app  
```bash
streamlit run streamlit_app.py
```

## Format du fichier Excel attendu
Colonnes recommandées:
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

Tu peux ajouter d’autres colonnes. L’app ne casse pas, elle les garde.

## Fichiers
- `streamlit_app.py` l’app
- `data/sample_pins.xlsx` un exemple prêt à charger
- `requirements.txt` dépendances
- `.gitignore` propre

## Roadmap perso
- Images en miniatures
- Export CSV en plus de Excel
- Multi collections
- Mode sombre custom

Si tu veux contribuer, fais un fork et ouvre une PR.

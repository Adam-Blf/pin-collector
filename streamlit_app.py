# Mon app Streamlit pour recenser mes pins
# Objectif: simple, clair, modifiable, exportable en Excel

import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
import datetime as dt

APP_TITLE = "Pin Collector"

# Colonnes de base que je veux toujours voir dans ma table
DEFAULT_COLUMNS = [
    "name",        # nom du pin
    "serie",       # série
    "collection",  # collection
    "quantity",    # quantité possédée
    "state",       # état
    "tradeable",   # dispo pour échange
    "price",       # prix indicatif
    "tags",        # tags libres
    "notes",       # notes perso
    "image_url"    # URL de l'image en ligne pour la miniature
]

# Fichier local optionnel si je veux sauvegarder entre 2 sessions
DATA_PATH = Path("data/pins.xlsx")

# Setup de la page
st.set_page_config(page_title=APP_TITLE, page_icon="📍", layout="wide")
st.title(APP_TITLE)

# Sidebar: import, export, options
with st.sidebar:
    st.subheader("Fichier")
    uploaded = st.file_uploader("Importer un Excel", type=["xlsx"])
    st.write("ou")
    load_local = st.button("Charger `data/pins.xlsx` si dispo")
    st.markdown("---")
    st.subheader("Export")
    export_name = st.text_input("Nom du fichier export", "pins_export.xlsx")
    save_local = st.checkbox("Sauvegarder aussi dans data/pins.xlsx")
    st.markdown("---")
    st.subheader("Aide")
    st.markdown("Colonnes conseillées: " + ", ".join(DEFAULT_COLUMNS))

@st.cache_data(show_spinner=False)
def load_excel(file) -> pd.DataFrame:
    # Je charge un Excel brut et je laisse la normalisation pour après
    return pd.read_excel(file)

def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Je m'assure que mes colonnes de base existent
    for col in DEFAULT_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col not in ["quantity", "price", "tradeable"] else 0

    # Je normalise quelques types pour éviter les surprises
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)
    if "tradeable" in df.columns:
        def _to_bool(x):
            if isinstance(x, str):
                return x.strip().lower() in {"1", "true", "vrai", "yes", "oui", "y"}
            return bool(x)
        df["tradeable"] = df["tradeable"].map(_to_bool)

    # Je remets mes colonnes préférées au début pour l'ordre visuel
    cols = [c for c in DEFAULT_COLUMNS if c in df.columns] + [c for c in df.columns if c not in DEFAULT_COLUMNS]
    return df[cols]

def sanitize_urls(df: pd.DataFrame) -> pd.DataFrame:
    # Je garde uniquement des URLs http(s) valides dans image_url
    if "image_url" in df.columns:
        def _ok(u):
            s = str(u).strip()
            return s if s.startswith("http://") or s.startswith("https://") else ""
        df["image_url"] = df["image_url"].map(_ok)
    return df

def make_sample() -> pd.DataFrame:
    # Petit jeu de données pour tester l'affichage et les miniatures
    data = [
        {
            "name": "Pikachu #001", "serie": "Kanto", "collection": "Starter",
            "quantity": 1, "state": "Neuf", "tradeable": False, "price": 9.9,
            "tags": "jaune, électrique", "notes": "Edition 2024",
            # URL d'exemple publique. A remplacer par mes propres images
            "image_url": "https://raw.githubusercontent.com/streamlit/example-data/main/images/pikachu.png"
        },
        {
            "name": "Bulbasaur #002", "serie": "Kanto", "collection": "Starter",
            "quantity": 2, "state": "Bon", "tradeable": True, "price": 7.5,
            "tags": "plante", "notes": "",
            "image_url": "https://raw.githubusercontent.com/streamlit/example-data/main/images/bulbasaur.png"
        },
        {
            "name": "Eevee #133", "serie": "Kanto", "collection": "Cute",
            "quantity": 1, "state": "Très bon", "tradeable": True, "price": 12.0,
            "tags": "évoli", "notes": "Cadeau",
            "image_url": "https://raw.githubusercontent.com/streamlit/example-data/main/images/eevee.png"
        },
    ]
    return pd.DataFrame(data)

# Chargement des données: upload > local > sample
if uploaded is not None:
    df = load_excel(uploaded)
elif load_local and DATA_PATH.exists():
    df = load_excel(DATA_PATH)
else:
    df = make_sample()

# Normalisation et sécurité basique des URLs
df = ensure_columns(df)
df = sanitize_urls(df)

# Filtres rapides pour piloter l'affichage
st.subheader("Filtres")
cols = st.columns(4)
with cols[0]:
    q = st.text_input("Recherche texte")
with cols[1]:
    serie_filter = st.text_input("Filtre série")
with cols[2]:
    collection_filter = st.text_input("Filtre collection")
with cols[3]:
    tradeable_filter = st.selectbox("Échange", ["Tous", "Oui", "Non"], index=0)

mask = pd.Series([True] * len(df))
if q:
    q_low = q.lower()
    mask &= df.apply(lambda row: any(q_low in str(v).lower() for v in row.values), axis=1)
if serie_filter:
    mask &= df["serie"].astype(str).str.contains(serie_filter, case=False, na=False)
if collection_filter:
    mask &= df["collection"].astype(str).str.contains(collection_filter, case=False, na=False)
if tradeable_filter != "Tous":
    want = tradeable_filter == "Oui"
    mask &= df["tradeable"] == want

df_view = df[mask].copy()

# Tableau éditable avec miniatures directement depuis image_url
st.subheader("Table")
edited = st.data_editor(
    df_view,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "tradeable": st.column_config.CheckboxColumn("Échange"),
        "quantity": st.column_config.NumberColumn("Quantité", min_value=0, step=1),
        "price": st.column_config.NumberColumn("Prix", min_value=0.0, step=0.1),
        "image_url": st.column_config.ImageColumn(
            "Miniature",
            help="URL http(s) d'une image directe png jpg webp"
        ),
    },
    key="editor",
)

# Je répercute les modifs sur le df complet via les index
df.loc[edited.index, :] = edited

# Petit récap utile
st.caption(f"{len(df)} entrées au total • {mask.sum()} visibles après filtres")

# Export Excel
def to_excel_bytes(dataframe: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="pins")
    buffer.seek(0)
    return buffer.getvalue()

excel_bytes = to_excel_bytes(df)

st.download_button(
    label="Télécharger Excel",
    data=excel_bytes,
    file_name=export_name,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# Sauvegarde locale discrète si je souhaite garder l'état
if save_local:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "wb") as f:
        f.write(excel_bytes)
    st.success("Sauvegardé dans data/pins.xlsx")

st.markdown("---")
st.caption("Par Adam Beloucif")

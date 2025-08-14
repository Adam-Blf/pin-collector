# Mon app Streamlit pour recenser mes pins
# Vue cartes avec ajout + edition par carte, export et sauvegarde Excel

import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path

APP_TITLE = "Pin Collector"

DEFAULT_COLUMNS = [
    "name", "serie", "collection", "quantity", "state",
    "tradeable", "price", "tags", "notes", "image_url"
]

DATA_PATH = Path("data/pins.xlsx")

st.set_page_config(page_title=APP_TITLE, page_icon="📍", layout="wide")
st.title(APP_TITLE)

# ===== Sidebar =====
with st.sidebar:
    st.subheader("Fichier")
    uploaded = st.file_uploader("Importer un Excel", type=["xlsx"])
    st.write("ou")
    load_local = st.button("Charger data/pins.xlsx si dispo")

    st.markdown("---")
    st.subheader("Affichage")
    show_table = st.toggle("Mode tableau editable", value=False)
    cols_per_row = st.slider("Cartes par ligne", 1, 4, 3)

    st.markdown("---")
    st.subheader("Export et sauvegarde")
    export_name = st.text_input("Nom du fichier export", "pins_export.xlsx")
    do_download = st.button("Exporter Excel")
    do_save_local = st.button("Enregistrer dans data/pins.xlsx")

# ===== Helpers =====
@st.cache_data(show_spinner=False)
def load_excel(file) -> pd.DataFrame:
    return pd.read_excel(file)

def ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in DEFAULT_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col not in ["quantity", "price", "tradeable"] else 0
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)
    def _to_bool(x):
        if isinstance(x, str):
            return x.strip().lower() in {"1","true","vrai","yes","oui","y"}
        return bool(x)
    df["tradeable"] = df["tradeable"].map(_to_bool)
    cols = [c for c in DEFAULT_COLUMNS if c in df.columns] + [c for c in df.columns if c not in DEFAULT_COLUMNS]
    return df[cols]

def sanitize_urls(df: pd.DataFrame) -> pd.DataFrame:
    def _ok(u):
        s = str(u).strip()
        return s if s.startswith("http://") or s.startswith("https://") else ""
    if "image_url" in df.columns:
        df["image_url"] = df["image_url"].map(_ok)
    return df

def make_sample() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "name": "Pikachu #001", "serie": "Kanto", "collection": "Starter",
            "quantity": 1, "state": "Neuf", "tradeable": False, "price": 9.9,
            "tags": "jaune, electrique", "notes": "Edition 2024",
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
            "quantity": 1, "state": "Tres bon", "tradeable": True, "price": 12.0,
            "tags": "evoli", "notes": "Cadeau",
            "image_url": "https://raw.githubusercontent.com/streamlit/example-data/main/images/eevee.png"
        },
    ])

def to_excel_bytes(dataframe: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="pins")
    buffer.seek(0)
    return buffer.getvalue()

# ===== Chargement =====
if uploaded is not None:
    df = load_excel(uploaded)
elif load_local and DATA_PATH.exists():
    df = load_excel(DATA_PATH)
else:
    df = make_sample()

df = ensure_columns(df)
df = sanitize_urls(df)

# ===== Barre d ajout =====
st.subheader("Ajouter un pin")
with st.expander("Nouveau pin", expanded=False):
    c1, c2, c3 = st.columns(3)
    with c1:
        new_name = st.text_input("Nom", "")
        new_serie = st.text_input("Serie", "")
        new_collection = st.text_input("Collection", "")
    with c2:
        new_quantity = st.number_input("Quantite", min_value=0, step=1, value=0)
        new_state = st.selectbox("Etat", ["Neuf","Tres bon","Bon","Moyen","Use"], index=2)
        new_tradeable = st.radio("Echange", ["Oui","Non"], index=1, horizontal=True)
    with c3:
        new_price = st.number_input("Prix (€)", min_value=0.0, step=0.1, value=0.0)
        new_tags = st.text_input("Tags", "")
        new_image = st.text_input("URL image", "")
    new_notes = st.text_area("Notes", "")

    if st.button("Ajouter"):
        row = {
            "name": new_name.strip(),
            "serie": new_serie.strip(),
            "collection": new_collection.strip(),
            "quantity": int(new_quantity),
            "state": new_state,
            "tradeable": (new_tradeable == "Oui"),
            "price": float(new_price),
            "tags": new_tags.strip(),
            "notes": new_notes.strip(),
            "image_url": new_image.strip() if new_image.startswith(("http://","https://")) else ""
        }
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        st.success("Pin ajoute")

# ===== Filtres =====
st.subheader("Filtres")
fcols = st.columns(4)
with fcols[0]:
    q = st.text_input("Recherche texte")
with fcols[1]:
    serie_filter = st.text_input("Filtre serie")
with fcols[2]:
    collection_filter = st.text_input("Filtre collection")
with fcols[3]:
    tradeable_filter = st.selectbox("Echange", ["Tous","Oui","Non"], index=0)

mask = pd.Series([True] * len(df))
if q:
    q_low = q.lower()
    mask &= df.apply(lambda row: any(q_low in str(v).lower() for v in row.values), axis=1)
if serie_filter:
    mask &= df["serie"].astype(str).str.contains(serie_filter, case=False, na=False)
if collection_filter:
    mask &= df["collection"].astype(str).str.contains(collection_filter, case=False, na=False)
if tradeable_filter != "Tous":
    mask &= df["tradeable"] == (tradeable_filter == "Oui")

df_view = df[mask].copy()

# ===== Affichage =====
if show_table:
    st.subheader("Tableau editable")
    edited = st.data_editor(
        df_view,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "tradeable": st.column_config.CheckboxColumn("Echange"),
            "quantity": st.column_config.NumberColumn("Quantite", min_value=0, step=1),
            "price": st.column_config.NumberColumn("Prix", min_value=0.0, step=0.1),
            "image_url": st.column_config.ImageColumn("Miniature"),
        },
        key="editor",
    )
    df.loc[edited.index, :] = edited

else:
    st.subheader("Collection")
    # CSS
    st.markdown("""
        <style>
        .pin-card { border:1px solid #e5e7eb; border-radius:16px; padding:12px; margin-bottom:20px; background:#fff; box-shadow:0 2px 6px rgba(0,0,0,0.06);}
        .pin-card img { width:100%; border-radius:12px; display:block; object-fit:cover; }
        .pin-info { text-align:left; padding:8px 4px 4px 4px; }
        .pin-title { font-weight:600; font-size:1.05rem; margin:8px 0 6px 0; }
        .pin-meta { margin:2px 0; font-size:0.95rem; }
        .pin-actions { display:flex; gap:8px; margin-top:8px; }
        </style>
    """, unsafe_allow_html=True)

    if "edit_flags" not in st.session_state:
        st.session_state.edit_flags = {}

    cols = st.columns(cols_per_row)
    states = ["Neuf","Tres bon","Bon","Moyen","Use"]

    for i, (idx, row) in enumerate(df_view.iterrows()):
        with cols[i % cols_per_row]:
            st.markdown('<div class="pin-card">', unsafe_allow_html=True)

            img_url = str(row.get("image_url", "") or "").strip()
            if img_url.startswith("http"):
                st.markdown(f'<img src="{img_url}">', unsafe_allow_html=True)
            else:
                st.markdown(
                    '<div style="width:100%;height:220px;border-radius:12px;background:#f1f5f9;display:flex;align-items:center;justify-content:center;color:#94a3b8;">Pas d image</div>',
                    unsafe_allow_html=True
                )

            editing = st.session_state.edit_flags.get(idx, False)

            if not editing:
                # Vue lecture
                st.markdown('<div class="pin-info">', unsafe_allow_html=True)
                st.markdown(f'<div class="pin-title">{row["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="pin-meta"><b>Serie</b>: {row["serie"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="pin-meta"><b>Collection</b>: {row["collection"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="pin-meta"><b>Quantite</b>: {row["quantity"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="pin-meta"><b>Etat</b>: {row["state"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="pin-meta"><b>Echange</b>: {"Oui" if bool(row["tradeable"]) else "Non"}</div>', unsafe_allow_html=True)
                price_txt = f'{float(row["price"]):.2f} €' if str(row["price"]) != "" else "-"
                st.markdown(f'<div class="pin-meta"><b>Prix</b>: {price_txt}</div>', unsafe_allow_html=True)
                if str(row.get("tags","")).strip():
                    st.markdown(f'<div class="pin-meta"><b>Tags</b>: {row["tags"]}</div>', unsafe_allow_html=True)
                if str(row.get("notes","")).strip():
                    st.markdown(f'<div class="pin-meta"><b>Notes</b>: {row["notes"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                if st.button("Editer", key=f"edit_btn_{idx}"):
                    st.session_state.edit_flags[idx] = True

            else:
                # Formulaire edition
                st.markdown('<div class="pin-info">', unsafe_allow_html=True)
                name_val = st.text_input("Nom", value=str(row["name"]), key=f"name_{idx}")
                serie_val = st.text_input("Serie", value=str(row["serie"]), key=f"serie_{idx}")
                collection_val = st.text_input("Collection", value=str(row["collection"]), key=f"collection_{idx}")
                qty_val = st.number_input("Quantite", min_value=0, step=1, value=int(row["quantity"]), key=f"qty_{idx}")
                state_val = st.selectbox("Etat", states, index=(states.index(str(row["state"])) if str(row["state"]) in states else 2), key=f"state_{idx}")
                trade_choice = st.radio("Echange", ["Oui","Non"], index=0 if bool(row["tradeable"]) else 1, horizontal=True, key=f"trade_{idx}")
                price_val = st.number_input("Prix (€)", min_value=0.0, step=0.1, value=float(row["price"]), key=f"price_{idx}")
                tags_val = st.text_input("Tags", value=str(row.get("tags","")), key=f"tags_{idx}")
                notes_val = st.text_area("Notes", value=str(row.get("notes","")), key=f"notes_{idx}")
                img_edit = st.text_input("URL image", value=img_url, key=f"img_{idx}")

                c_save, c_cancel = st.columns(2)
                with c_save:
                    if st.button("Enregistrer", key=f"save_{idx}"):
                        df.loc[idx, "name"] = name_val.strip()
                        df.loc[idx, "serie"] = serie_val.strip()
                        df.loc[idx, "collection"] = collection_val.strip()
                        df.loc[idx, "quantity"] = int(qty_val)
                        df.loc[idx, "state"] = state_val
                        df.loc[idx, "tradeable"] = (trade_choice == "Oui")
                        df.loc[idx, "price"] = float(price_val)
                        df.loc[idx, "tags"] = tags_val.strip()
                        df.loc[idx, "notes"] = notes_val.strip()
                        df.loc[idx, "image_url"] = img_edit.strip() if img_edit.startswith(("http://","https://")) else ""
                        st.session_state.edit_flags[idx] = False
                        st.success("Modifications enregistrees")
                with c_cancel:
                    if st.button("Annuler", key=f"cancel_{idx}"):
                        st.session_state.edit_flags[idx] = False

                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

# ===== Recap =====
st.caption(f"{len(df)} entrees au total • {mask.sum()} visibles apres filtres")

# ===== Export et sauvegarde =====
if do_download:
    st.download_button(
        label="Telecharger maintenant",
        data=to_excel_bytes(df),
        file_name=export_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

if do_save_local:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "wb") as f:
        f.write(to_excel_bytes(df))
    st.success("Sauvegarde dans data/pins.xlsx ok")

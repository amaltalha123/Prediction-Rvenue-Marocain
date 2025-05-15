import streamlit as st
import requests
import time

st.set_page_config(page_title="Prédiction Revenu", page_icon="💰")
st.title("💰 Prédiction du Revenu Annuel au Maroc")

st.markdown("Remplissez les champs suivants pour estimer le revenu annuel d’un individu :")

with st.expander("🧍 Informations personnelles"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Âge", 18, 70, 30)
        experience = st.slider("Années d'expérience", 0, 50, 5)
        sexe = st.selectbox("Sexe", ["Femme", "Homme"])
        langue = st.selectbox("Langue maternelle", ["arab", "amazigh"])
    with col2:
        education = st.selectbox("Niveau d'éducation", ["sans niveau", "fondamental", "secondaire", "supérieur"])
        urbain_rural = st.selectbox("Milieu de résidence", ["Urbain", "Rural"])
        categorie_socio = st.selectbox("Catégorie socioprofessionnelle", ["Groupe 1", "Groupe 2", "Groupe 3", "Groupe 4", "Groupe 5", "Groupe 6"])
        etat_matrimonial = st.selectbox("État matrimonial", ["célibataire", "marié", "divorcé", "veuf"])

with st.expander("🏠 Situation géographique et matérielle"):
    col3, col4 = st.columns(2)
    with col3:
        possession = st.selectbox("Possession de biens", ["Aucun", "Voiture", "Logement", "Terrain"])
        contrat = st.selectbox("Type de contrat", ["CDI", "CDD", "sans contrat"])
    with col4:
        region = st.selectbox("Région", [
            "Béni Mellal-Khénifra", "Casablanca-Settat", "Dakhla-Oued Ed-Dahab", "Drâa-Tafilalet",
            "Fès-Meknès", "Guelmim-Oued Noun", "Laâyoune-Sakia El Hamra", "L’Oriental",
            "Marrakech-Safi", "Rabat-Salé-Kénitra", "Souss-Massa", "Tanger-Tétouan-Al Hoceïma"
        ])

# --- 🔍 Bouton de prédiction ---
st.markdown("---")
col5, col6 = st.columns([1, 4])
with col5:
    if st.button("🔮 Prédire le revenu"):
        user_data = {
            "age": age,
            "experience": experience,
            "sexe": sexe,
            "education": education,
            "urbain_rural": urbain_rural,
            "categorie_socio": categorie_socio,
            "langue": langue,
            "etat_matrimonial": etat_matrimonial,
            "possession": possession,
            "region": region,
            "contrat": contrat
        }

        with st.spinner("⏳ Prédiction en cours..."):
            try:
                start = time.time()
                response = requests.post("http://127.0.0.1:8000/predict", json=user_data)
                response.raise_for_status()
                prediction = response.json()["revenu_annuel"]
                end = time.time()
                st.success(f"💸 Revenu annuel estimé : **{prediction:,.2f} DH**")
                st.caption(f"🕓 Temps de réponse : {end - start:.2f} sec")
            except Exception as e:
                st.error(f"❌ Erreur lors de la prédiction : {e}")


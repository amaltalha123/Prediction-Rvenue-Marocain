import streamlit as st
import requests

st.title("💰 Prédiction du Revenu Annuel")

# Champs à remplir par l'utilisateur
age = st.slider("Âge", 18, 70, 30)
experience = st.slider("Années d'expérience", 0, 50, 5)

sexe = st.selectbox("Sexe", ["Femme", "Homme"])
education = st.selectbox("Niveau d'éducation", ["sans niveau", "fondamental", "secondaire", "supérieur"])
urbain_rural = st.selectbox("Milieu de résidence", ["Urbain", "Rural"])
categorie_socio = st.selectbox("Catégorie socioprofessionnelle", ["Groupe 1", "Groupe 2", "Groupe 3", "Groupe 4", "Groupe 5", "Groupe 6"])
langue = st.selectbox("Langue maternelle", ["arab", "amazigh"])
etat_matrimonial = st.selectbox("État matrimonial", ["célibataire", "marié", "divorcé", "veuf"])
possession = st.selectbox("Possession de biens", ["Aucun", "Voiture", "Logement", "Terrain"])

region = st.selectbox("Région", [
    "Casablanca-Settat", "Dakhla-Oued Ed-Dahab", "Drâa-Tafilalet", "Fès-Meknès",
    "Guelmim-Oued Noun", "Laâyoune-Sakia El Hamra", "L’Oriental", "Marrakech-Safi",
    "Rabat-Salé-Kénitra", "Souss-Massa", "Tanger-Tétouan-Al Hoceïma"
])

contrat = st.selectbox("Type de contrat", ["CDI", "CDD", "sans contrat"])

# Quand on clique sur le bouton "Prédire"
if st.button("Prédire le revenu"):
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

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=user_data)
        response.raise_for_status()
        prediction = response.json()["revenu_annuel"]
        st.success(f"✅ Revenu annuel prédit : {prediction:.2f} DH")
        if st.button("Réinitialiser"):
           st.experimental_rerun()
    except Exception as e:
        st.error(f"❌ Erreur lors de la prédiction : {e}")
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Charger le modèle
model = joblib.load("modele_selection.joblib")

# Définir la structure des données envoyées par l'utilisateur
class InputData(BaseModel):
    age: int
    experience: int
    sexe: str  # "Homme" ou "Femme"
    education: str  # 'sans niveau', 'fondamental', 'secondaire', 'supérieur'
    urbain_rural: str  # "Urbain" ou "Rural"
    categorie_socio: str  # Groupe 1 à Groupe 6
    langue: str  # 'arab' ou 'amazigh'
    etat_matrimonial: str  # 'marié', 'célibataire', 'divorcé', 'veuf'
    possession: str  # 'Voiture', 'Logement', 'Terrain', 'Aucun'
    region: str
    contrat: str  # 'CDI', 'CDD', 'sans contrat'

@app.post("/predict")
def predict(data: InputData):
    # Encodage label
    sexe = 1 if data.sexe.lower() == "homme" else 0
    urbain = 1 if data.urbain_rural.lower() == "urbain" else 0
    langue = 1 if data.langue.lower() == "arab" else 0

    education_map = ['sans niveau', 'fondamental', 'secondaire', 'supérieur']
    education = education_map.index(data.education.lower())

    groupe_map = ['Groupe 1', 'Groupe 2', 'Groupe 3', 'Groupe 4', 'Groupe 5', 'Groupe 6']
    groupe = groupe_map.index(data.categorie_socio)

    # One-hot pour État matrimonial
    etat_marié = 1 if data.etat_matrimonial == "marié" else 0
    etat_veuf = 1 if data.etat_matrimonial == "veuf" else 0
    etat_divorce = 1 if data.etat_matrimonial == "divorcé" else 0

    # One-hot pour Possession de biens
    bien_logement = 1 if data.possession == "Logement" else 0
    bien_terrain = 1 if data.possession == "Terrain" else 0
    bien_voiture = 1 if data.possession == "Voiture" else 0

    # One-hot pour Régions
    all_regions = [
        "Casablanca-Settat", "Dakhla-Oued Ed-Dahab", "Drâa-Tafilalet", "Fès-Meknès",
        "Guelmim-Oued Noun", "Laâyoune-Sakia El Hamra", "L’Oriental", "Marrakech-Safi",
        "Rabat-Salé-Kénitra", "Souss-Massa", "Tanger-Tétouan-Al Hoceïma"
    ]
    region_ohe = [1 if data.region == reg else 0 for reg in all_regions]

    # One-hot pour Type de contrat
    contrat_cdi = 1 if data.contrat == "CDI" else 0
    contrat_sans = 1 if data.contrat == "sans contrat" else 0

    # Construction du vecteur final dans l'ordre attendu
    input_data = np.array([[
        data.age,
        data.experience,
        sexe,
        education,
        urbain,
        groupe,
        langue,
        etat_divorce,
        etat_marié,
        etat_veuf,
        bien_logement,
        bien_terrain,
        bien_voiture,
        *region_ohe,
        contrat_cdi,
        contrat_sans
    ]])

    prediction = model.predict(input_data)
    return {"revenu_annuel": float(prediction[0])}


from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Charger le modèle entraîné
model = joblib.load("modele_selection.joblib")

# Structure des données attendues en entrée
class InputData(BaseModel):
    age: int
    experience: int
    sexe: str
    education: str
    urbain_rural: str
    categorie_socio: str
    langue: str
    etat_matrimonial: str
    possession: str
    region: str
    contrat: str

@app.post("/predict")
def predict(data: InputData):
    # Encodage simple
    sexe = 1 if data.sexe.lower() == "homme" else 0
    urbain = 1 if data.urbain_rural.lower() == "urbain" else 0
    langue = 1 if data.langue.lower() == "arab" else 0

    # Encodage ordonné de l'éducation
    education_map = ['sans niveau', 'fondamental', 'secondaire', 'supérieur']
    education = education_map.index(data.education.lower())

    groupe_map = ['Groupe 1', 'Groupe 2', 'Groupe 3', 'Groupe 4', 'Groupe 5', 'Groupe 6']
    groupe = groupe_map.index(data.categorie_socio)

    # One-hot encodage : état matrimonial
    etat_celib = 1 if data.etat_matrimonial == "célibataire" else 0
    etat_divorce = 1 if data.etat_matrimonial == "divorcé" else 0
    etat_marie = 1 if data.etat_matrimonial == "marié" else 0
    etat_veuf = 1 if data.etat_matrimonial == "veuf" else 0

    # One-hot encodage : possessions
    bien_aucun = 1 if data.possession == "Aucun" else 0
    bien_logement = 1 if data.possession == "Logement" else 0
    bien_terrain = 1 if data.possession == "Terrain" else 0
    bien_voiture = 1 if data.possession == "Voiture" else 0

    # One-hot encodage : régions
    all_regions = [
        "Béni Mellal-Khénifra", "Casablanca-Settat", "Dakhla-Oued Ed-Dahab", "Drâa-Tafilalet",
        "Fès-Meknès", "Guelmim-Oued Noun", "Laâyoune-Sakia El Hamra", "L’Oriental",
        "Marrakech-Safi", "Rabat-Salé-Kénitra", "Souss-Massa", "Tanger-Tétouan-Al Hoceïma"
    ]
    region_ohe = [1 if data.region == reg else 0 for reg in all_regions]

    # One-hot encodage : type de contrat
    contrat_cdd = 1 if data.contrat == "CDD" else 0
    contrat_cdi = 1 if data.contrat == "CDI" else 0
    contrat_sans = 1 if data.contrat == "sans contrat" else 0

    # Construction du vecteur final (31 colonnes)
    input_data = np.array([[
        data.age,
        data.experience,
        sexe,
        education,
        urbain,
        groupe,
        langue,
        etat_celib,
        etat_divorce,
        etat_marie,
        etat_veuf,
        bien_aucun,
        bien_logement,
        bien_terrain,
        bien_voiture,
        *region_ohe,
        contrat_cdd,
        contrat_cdi,
        contrat_sans
    ]])

    # Vérification de la dimension
    if input_data.shape[1] != model.n_features_in_:
        return {"error": f"Le modèle attend {model.n_features_in_} colonnes, mais a reçu {input_data.shape[1]}"}

    # Prédiction
    prediction = model.predict(input_data)
    return {"revenu_annuel": float(prediction[0])}

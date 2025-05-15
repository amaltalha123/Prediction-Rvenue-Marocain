import pandas as pd
import numpy as np

# Configuration des paramètres
n_records = 40000
np.random.seed(42)  # Pour la reproductibilité

# Définition des catégories
sexes = ['Homme', 'Femme']

# Probabilités normalisées pour le niveau d'éducation
total_education = 0.318 + 0.268 + 0.194 + 0.102
education_probs = [0.318 / total_education, 0.268 / total_education, 0.194 / total_education, 0.102 / total_education]

marital_statuses = ['célibataire', 'marié', 'divorcé', 'veuf']
marital_probs = [0.332, 0.583, 0.033, 0.052]  # Somme = 1.000

urban_rural = ['Urbain', 'Rural']

socio_professional_groups = [
    'Groupe 1', 'Groupe 2', 'Groupe 3',
    'Groupe 4', 'Groupe 5', 'Groupe 6'
]
groups_probs = [0.10, 0.15, 0.10, 0.20, 0.25, 0.20]  # Somme = 1.000

possessions = ['Voiture', 'Logement', 'Terrain', 'Aucun']

# Nouvelles catégories
regions_maroc = [
    "Tanger-Tétouan-Al Hoceïma",
    "L’Oriental",
    "Fès-Meknès",
    "Rabat-Salé-Kénitra",
    "Béni Mellal-Khénifra",
    "Casablanca-Settat",
    "Marrakech-Safi",
    "Drâa-Tafilalet",
    "Souss-Massa",
    "Guelmim-Oued Noun",
    "Laâyoune-Sakia El Hamra",
    "Dakhla-Oued Ed-Dahab"
]

types_contrat = ['CDI', 'CDD', 'sans contrat']

langues_maternelles = ['amazigh', 'arab']
langues_probs = [0.1915, 0.8085]

# Génération des données
data = {
    'Identifiant': range(1, n_records + 1),
    'Âge': np.random.randint(18, 70, size=n_records),
    'Sexe': np.random.choice(sexes, size=n_records),
    'Niveau d\'éducation': np.random.choice(['sans niveau', 'fondamental', 'secondaire', 'supérieur'], size=n_records, p=education_probs),
    'État matrimonial': np.random.choice(marital_statuses, size=n_records, p=marital_probs),
    'Urbain/Rural': np.random.choice(urban_rural, size=n_records),
    'Catégorie socioprofessionnelle': np.random.choice(socio_professional_groups, size=n_records, p=groups_probs),
    'Années d\'expérience': np.random.randint(0, 50, size=n_records),
    'Possession de biens':  np.random.choice(possessions, size=n_records),
    'Région': np.random.choice(regions_maroc, size=n_records),
    'Type de contrat': np.random.choice(types_contrat, size=n_records),
    'Langue maternelle': np.random.choice(langues_maternelles, size=n_records, p=langues_probs),
}

df = pd.DataFrame(data)

# Calcul du revenu basé sur les contraintes
def calculate_income(row):
    # Base selon urbain/rural
    if row['Urbain/Rural'] == 'Urbain':
        base_income = 26988
    else:
        base_income = 12862

    # Sexe : homme +10%
    if row['Sexe'] == 'Homme':
        base_income *= 1.10

    # Niveau éducation
    if row['Niveau d\'éducation'] == 'supérieur':
        base_income *= 1.5
    elif row['Niveau d\'éducation'] == 'secondaire':
        base_income *= 1.2
    elif row['Niveau d\'éducation'] == 'fondamental':
        base_income *= 0.9

    # Âge influence revenu
    age = row['Âge']
    if age < 30:
        base_income *= 0.8
    elif age > 60:
        base_income *= 0.9
    else:
        factor = 0.8 + (age - 30) * (0.2 / 30)
        base_income *= factor

    # Années d'expérience
    base_income += row['Années d\'expérience'] * 500

    # Catégorie socioprofessionnelle
    group_factors = {
        'Groupe 1': 2.0,
        'Groupe 2': 1.5,
        'Groupe 3': 1.0,
        'Groupe 4': 0.8,
        'Groupe 5': 0.7,
        'Groupe 6': 0.5
    }
    base_income *= group_factors.get(row['Catégorie socioprofessionnelle'], 1.0)

    # Possession de biens
    possession_factors = {
        'Voiture': 1.15,
        'Logement': 1.10,
        'Terrain': 1.05,
        'Aucun': 1.0,
    }
    base_income *= possession_factors.get(row['Possession de biens'], 1.0)

    # S'assurer revenu minimal
    if base_income < 1000:
        base_income = 1000

    return int(base_income)

df['Revenu annuel (DH)'] = df.apply(calculate_income, axis=1)

# --- Ajout de valeurs manquantes (~2% sur plusieurs colonnes)
for col in ['Niveau d\'éducation', 'État matrimonial', 'Langue maternelle', 'Revenu annuel (DH)']:
    idx_missing = df.sample(frac=0.02, random_state=42).index
    df.loc[idx_missing, col] = np.nan

# --- Ajout de valeurs aberrantes
# Quelques âges aberrants (ex: 5 en dessous 0 et 5 au dessus 120)
idx_age_low = df.sample(n=5, random_state=1).index
idx_age_high = df.sample(n=5, random_state=2).index
df.loc[idx_age_low, 'Âge'] = -5  # âge impossible
df.loc[idx_age_high, 'Âge'] = 150  # âge impossible

# Quelques revenus aberrants (5 très élevés, 5 négatifs) 
idx_rev_high = df.sample(n=5, random_state=3).index
idx_rev_low = df.sample(n=5, random_state=4).index
df.loc[idx_rev_high, 'Revenu annuel (DH)'] = 10_000_000  # valeur extravagante
df.loc[idx_rev_low, 'Revenu annuel (DH)'] = -5000  # valeur négative impossible

# --- Colonnes redondantes (copies ou variations)
df['Âge doublé'] = df['Âge'] * 2
df['Revenu approximatif'] = df['Revenu annuel (DH)'].round(-3)  # arrondi au millier le plus proche

# --- Colonnes non pertinentes (colonne avec identifiants aléatoires, texte aléatoire)
df['Code aléatoire'] = np.random.choice(['X123', 'Y456', 'Z789', 'W000'], size=n_records)

# Export CSV
df.to_csv('dataset_revenu_marocains.csv', index=False, encoding='utf-8-sig')

print("Dataset avec valeurs manquantes, aberrantes, colonnes redondantes et non pertinentes généré avec succès : dataset_revenu_marocains.csv")

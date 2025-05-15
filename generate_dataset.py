import pandas as pd
import numpy as np

# Configuration des paramètres
n_records = 40000
np.random.seed(42)

# Définition des catégories
sexes = ['Homme', 'Femme']
education_probs = [0.318 / (0.318 + 0.268 + 0.194 + 0.102), 0.268 / (0.318 + 0.268 + 0.194 + 0.102),
                   0.194 / (0.318 + 0.268 + 0.194 + 0.102), 0.102 / (0.318 + 0.268 + 0.194 + 0.102)]
marital_statuses = ['célibataire', 'marié', 'divorcé', 'veuf']
marital_probs = [0.332, 0.583, 0.033, 0.052]
urban_rural = ['Urbain', 'Rural']
socio_professional_groups = ['Groupe 1', 'Groupe 2', 'Groupe 3', 'Groupe 4', 'Groupe 5', 'Groupe 6']
groups_probs = [0.10, 0.15, 0.10, 0.20, 0.25, 0.20]
possessions = ['Voiture', 'Logement', 'Terrain', 'Aucun']
regions_maroc = [
    "Tanger-Tétouan-Al Hoceïma", "L’Oriental", "Fès-Meknès", "Rabat-Salé-Kénitra",
    "Béni Mellal-Khénifra", "Casablanca-Settat", "Marrakech-Safi", "Drâa-Tafilalet",
    "Souss-Massa", "Guelmim-Oued Noun", "Laâyoune-Sakia El Hamra", "Dakhla-Oued Ed-Dahab"
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
    'Urbain/Rural': np.random.choice(urban_rural, size=n_records, p=[0.6, 0.4]), 
    'Catégorie socioprofessionnelle': np.random.choice(socio_professional_groups, size=n_records, p=groups_probs),
    'Années d\'expérience': np.random.randint(0, 50, size=n_records),
    'Possession de biens': np.random.choice(possessions, size=n_records),
    'Région': np.random.choice(regions_maroc, size=n_records),
    'Type de contrat': np.random.choice(types_contrat, size=n_records),
    'Langue maternelle': np.random.choice(langues_maternelles, size=n_records, p=langues_probs),
}

df = pd.DataFrame(data)

# Fonction de calcul de revenu
def calculate_income(row):
    base_income = 26988 if row['Urbain/Rural'] == 'Urbain' else 12862

    if row['Sexe'] == 'Homme':
        base_income *= 1.10

    edu = row['Niveau d\'éducation']
    if edu == 'supérieur':
        base_income *= 1.5
    elif edu == 'secondaire':
        base_income *= 1.2
    elif edu == 'fondamental':
        base_income *= 0.9

    age = row['Âge']
    if age < 30:
        base_income *= 0.8
    elif age > 60:
        base_income *= 0.9
    else:
        factor = 0.8 + (age - 30) * (0.2 / 30)
        base_income *= factor

    base_income += row['Années d\'expérience'] * 500

    group_factors = {
        'Groupe 1': 2.0, 'Groupe 2': 1.5, 'Groupe 3': 1.0,
        'Groupe 4': 0.8, 'Groupe 5': 0.7, 'Groupe 6': 0.5
    }
    base_income *= group_factors.get(row['Catégorie socioprofessionnelle'], 1.0)

    possession_factors = {'Voiture': 1.15, 'Logement': 1.10, 'Terrain': 1.05, 'Aucun': 1.0}
    base_income *= possession_factors.get(row['Possession de biens'], 1.0)

    return max(int(base_income), 1000)

df['Revenu annuel (DH)'] = df.apply(calculate_income, axis=1)

# Ajouter des valeurs manquantes (~2%)
for col in ['Niveau d\'éducation', 'État matrimonial', 'Langue maternelle', 'Revenu annuel (DH)']:
    idx_missing = df.sample(frac=0.02, random_state=42).index
    df.loc[idx_missing, col] = np.nan

# Ajouter des valeurs aberrantes
df.loc[df.sample(n=5, random_state=1).index, 'Âge'] = -5
df.loc[df.sample(n=5, random_state=2).index, 'Âge'] = 150
df.loc[df.sample(n=5, random_state=3).index, 'Revenu annuel (DH)'] = 10_000_000
df.loc[df.sample(n=5, random_state=4).index, 'Revenu annuel (DH)'] = -5000

# Colonnes redondantes
df['Âge doublé'] = df['Âge'] * 2
df['Revenu approximatif'] = df['Revenu annuel (DH)'].round(-3)
df['Code aléatoire'] = np.random.choice(['X123', 'Y456', 'Z789', 'W000'], size=n_records)

# --- Ajustement du revenu moyen et des proportions
revenu_cible = 21949
revenus_valides = df['Revenu annuel (DH)'].dropna()
scaling_factor = revenu_cible / revenus_valides.mean()
df['Revenu annuel (DH)'] = df['Revenu annuel (DH)'] * scaling_factor
df['Revenu annuel (DH)'] = df['Revenu annuel (DH)'].round().astype('Int64')

# Ajustement des proportions
def ajuster_proportions(df):
    urbain = df[df['Urbain/Rural'] == 'Urbain']
    rural = df[df['Urbain/Rural'] == 'Rural']
    cible_urbain = int(0.659 * len(urbain))
    cible_rural = int(0.854 * len(rural))
    seuil_urbain = urbain.sort_values(by='Revenu annuel (DH)').iloc[cible_urbain]['Revenu annuel (DH)']
    seuil_rural = rural.sort_values(by='Revenu annuel (DH)').iloc[cible_rural]['Revenu annuel (DH)']
    df.loc[(df['Urbain/Rural'] == 'Urbain') & (df['Revenu annuel (DH)'] > seuil_urbain), 'Revenu annuel (DH)'] += 3000
    df.loc[(df['Urbain/Rural'] == 'Rural') & (df['Revenu annuel (DH)'] > seuil_rural), 'Revenu annuel (DH)'] += 2000
    return df

df = ajuster_proportions(df)

# Export CSV
df.to_csv('dataset_revenu_marocains.csv', index=False, encoding='utf-8-sig')
print("✅ Dataset généré : 'dataset_revenu_marocains.csv'")

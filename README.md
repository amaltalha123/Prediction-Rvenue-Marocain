# Mini-Projet IA : Prédiction du Revenu Annuel des Marocains 🇲🇦

## Objectif
Ce projet a pour but de développer un pipeline complet de Machine Learning en Python afin de prédire le **revenu annuel** des Marocains à partir de données simulées inspirées des statistiques du HCP.

---

## Contenu du projet

### Arborescence
├── generate_dataset.py # Script de génération du dataset synthétique
├── dataset_revenu_marocains.csv # Dataset simulé (~40 000 instances)
├── mini_projet_AI_Noms.ipynb # Notebook complet du mini-projet
├── modele_selection.joblib # Modèle final sauvegardé
├── api.py # API FastAPI exposant le modèle
├── app.py # Application web Streamlit
├── README.md # Ce fichier

## Étapes du projet

### 1. **Génération des données**
- Données réalistes basées sur des statistiques marocaines : âge, sexe, zone géographique, niveau d'éducation, etc.
- Données bruitées volontairement avec :
  - Valeurs manquantes
  - Valeurs aberrantes
  - Colonnes redondantes ou non pertinentes

### 2. **Exploration et préparation**
- Analyse exploratoire (EDA) avec `pandas-profiling`.
- Nettoyage : traitement des valeurs manquantes, aberrantes, doublons.
- Transformation : encodage, normalisation, création/suppression de colonnes.

### 3. **Modélisation**
- Séparation train/test (70/30)
- Modèles utilisés :
  - Régression Linéaire
  - Arbre de Décision
  - Gradient Boosting
- Optimisation des hyperparamètres via `GridSearchCV`
- Métriques : `MAE`, `RMSE`, `R²`

### 4. **Déploiement**
- Sauvegarde du modèle avec `joblib`
- API REST avec `FastAPI`
- Interface utilisateur avec `Streamlit` :
  - Formulaire de saisie des caractéristiques
  - Prédiction du revenu en temps réel

---

## Technologies utilisées
Python 3.x
Numpy, Pandas
Scikit-learn
Matplotlib, Seaborn, ydata_profiling
Joblib
FastAPI
Streamlit

## Installation
1. Cloner le dépôt :
git clone https://github.com/votre-utilisateur/prediction-revenu-maroc.git
cd prediction-revenu-maroc

2. Générer les données :
python generate_dataset.py

3. Lancer l’API :
python -m uvicorn api:app --reload

4. Lancer l’application Streamlit :
streamlit run app.py


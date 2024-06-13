import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
import time
import os
import subprocess

def install():
    command = "pip install joblib"
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    time.sleep(3)  # Wait for the server to start
    return process

try:
    import joblib
except ImportError:
    install_result = install()
    import joblib


from Packing_phishing_model.prediction_model.predict import predict

# Charger le modèle pré-entraîné
classification_pipeline = joblib.load('Packing_phishing_model/prediction_model/trained_models/phishing_url_prediction.pkl')

# Fonction pour télécharger une image depuis une URL
def load_image_from_url(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image

# Fonction pour faire la prédiction
def predict_url(url):
    # Ici, vous devrez extraire les caractéristiques de l'URL et préparer les données
    # Pour l'exemple, nous utiliserons une valeur factice pour la prédiction
    prediction = classification_pipeline.predict([url])[0]
    return prediction

# Titre de l'application
st.title('Phishing Checker')

# Demander à l'utilisateur d'entrer une URL
url = st.text_input('Entrez une URL à vérifier')

# Vérifier si l'utilisateur a soumis une URL
if st.button('Vérifier'):
    # Faire la prédiction
    prediction = predict(url)
    
    # Afficher le résultat en fonction de la prédiction
    if prediction == 0.0:
        st.text("Legitime url")
    elif prediction == 1.0:
        st.text("Phishing url")
    else:
        st.error('Une erreur s\'est produite lors de la prédiction.')


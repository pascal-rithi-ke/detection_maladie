import os, base64, sys
from io import BytesIO

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from pickle import load

import pandas as pd
import joblib

# Ajouter le répertoire de base du projet au chemin de recherche
sys.path.append(os.path.abspath(os.path.join('..')))
from functions_utils.text import *

# Charger le modèle de classification des maladies
model = joblib.load('../model/chatbox_random_forest.pkl')

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "API is running"

@app.route("/processImage", methods=["POST"])
def processImage():
    if request.method == "POST":
        # Get image data from request
        if 'image' in request.files:
            image = request.files['image']
            image_data = image.read()
            
            # Get parameters from request
            format_img = request.args.get('format')

            # Convert binary image data to Base64
            encoded_image = base64.b64encode(image_data).decode('utf-8')
            
            # Save image in DataBase (not implemented in SQL)
            
            # Return response
            return jsonify({
                "message": "L'image a été reçue avec succès",
                "message_test": "TEST",
                "upload_image": "data:image/{};base64,{}".format(format_img, encoded_image),
            })
        else:
            return jsonify({"message": "Aucune image trouvée"})
    else:
        return jsonify({"message": "Method not allowed"})
    
# Chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    app.logger.debug('Request JSON: %s', request.json)  # Log de la requête
    data = request.json
    user_message = data.get('message')
    if user_message:
        bot_response = f"{preprocess_text(user_message)}"
        if bot_response == "":
            bot_response = "Sorry, I don't understand or I don't have a response for that. Can you try again?"
            app.logger.debug('No response found')
        else:
            # Tableau des symptômes connus avec leurs poids correspondants
            df1 = pd.read_csv('../data/cleaned_symptom_severity.csv')
            known_symptoms_array = df1['Symptom']
            symptoms_weights = df1['weight']
            symptoms_array = []
            weights_array = []
            unique_symptoms = set()
            target_count = 17  # Nombre cible de symptômes
            similarity_threshold = 0.9  # Seuil initial de similarité
            word_symptom_mapping = {}  # Dictionnaire pour stocker les associations

            def search_word_similarity(word):
                max_similarity = 0
                max_symptom = ''
                max_weight = 0
                for i, symptom in enumerate(known_symptoms_array):
                    similarity = nlp(word).similarity(nlp(symptom))
                    if similarity > max_similarity:
                        max_similarity = similarity
                        max_symptom = symptom
                        max_weight = symptoms_weights[i]
                return max_symptom, max_similarity, max_weight

            # Fonction pour trouver les symptômes et leurs poids associés jusqu'à atteindre le compte cible
            def find_symptoms(text, threshold):
                new_symptoms = []
                new_weights = []
                for word in text.split():
                    if word in word_symptom_mapping:
                        continue  # Ignorer les mots déjà traités

                    # Rechercher la similarité avec les symptômes connus
                    symptom, similarity, weight = search_word_similarity(word)
                    # Si la similarité est supérieure au seuil et le symptôme est unique
                    if similarity >= threshold and symptom not in unique_symptoms:
                        unique_symptoms.add(symptom)
                        new_symptoms.append(symptom)
                        new_weights.append(weight)
                        word_symptom_mapping[word] = weight  # Enregistrer le poids associé
                return new_symptoms, new_weights

            # Boucle pour ajuster le seuil de similarité jusqu'à obtenir suffisamment de symptômes
            while len(symptoms_array) < target_count and similarity_threshold > 0:
                new_symptoms, new_weights = find_symptoms(bot_response, similarity_threshold)
                symptoms_array.extend(new_symptoms)
                weights_array.extend(new_weights)

                # Synchroniser les poids avec les symptômes après avoir éliminé les doublons
                symptoms_weights_mapping = dict(zip(symptoms_array, weights_array))
                symptoms_array = list(symptoms_weights_mapping.keys())
                weights_array = list(symptoms_weights_mapping.values())

                # Limiter immédiatement le nombre de symptômes à target_count si atteint
                if len(symptoms_array) >= target_count:
                    symptoms_array = symptoms_array[:target_count]  # S'assurer de ne pas dépasser le nombre cible
                    weights_array = weights_array[:target_count]  # S'assurer de ne pas dépasser le nombre cible
                    break  # Sortir de la boucle si la cible est atteinte

                similarity_threshold -= 0.05  # Réduire le seuil de similarité pour obtenir plus de symptômes

            try:
                # Prédictions de la maladie
                disease_predictions = model.predict([weights_array])
                
                # Afficher les probabilités de prédiction
                disease_probabilities = model.predict_proba([weights_array])
                disease_probabilities = disease_probabilities[0]
                disease_probabilities = {disease: probability for disease, probability in zip(model.classes_, disease_probabilities)}
                
                # Afficher les 5 maladies les plus probables
                top_diseases = sorted(disease_probabilities.items(), key=lambda x: x[1], reverse=True)[:5]
                
                if disease_predictions:
                    detected_disease = disease_predictions[0]
                    probable_diseases = [disease for disease, _ in top_diseases if disease != detected_disease]
                    bot_response = f"We have detected {detected_disease} as the illness, and these other conditions ({', '.join(probable_diseases)}) may also correspond to your symptoms."
                else:
                    bot_response = "No diseases detected based on the provided symptoms."
            except ValueError as e:
                app.logger.error(f'Error during prediction: {str(e)}')
                bot_response = "Sorry, I don't understand or I don't have a response for that. Can you try again?"
    else:
        bot_response = "No message received"
        app.logger.debug('No message found in request')

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
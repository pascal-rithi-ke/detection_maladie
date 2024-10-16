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
    
# Chatbot endpoint
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get('message')
    df2 = pd.read_csv("../data/symptom_Description.csv")
    df3 = pd.read_csv("../data/symptom_precaution.csv")
    
    if user_message:
        # Nettoyer et traiter le message utilisateur
        bot_response = process_text(user_message)
        
        if bot_response == "":
            bot_response = "Sorry, I don't understand or I don't have a response for that. Can you try again?"
            app.logger.debug('No response found')
        else:
            # Appeler search_word_similarity pour trouver les symptômes correspondants
            symptoms_ids_or_predictions = search_word_similarity(bot_response)
            
            try:
                # Prédictions de la maladie basées sur les IDs des symptômes ou le texte
                disease_predictions = model.predict([symptoms_ids_or_predictions])
                
                # Obtenir les probabilités de prédiction pour les maladies
                disease_probabilities = model.predict_proba([symptoms_ids_or_predictions])
                disease_probabilities = disease_probabilities[0]
                disease_probabilities = {disease: probability for disease, probability in zip(model.classes_, disease_probabilities)}
                
                # Trier et obtenir les 5 maladies les plus probables
                top_diseases = sorted(disease_probabilities.items(), key=lambda x: x[1], reverse=True)[:5]
                
                if disease_predictions:
                    detected_disease = disease_predictions[0]
                    probable_diseases = [disease for disease, _ in top_diseases if disease != detected_disease]
                    
                    # Récupérer la description et les précautions associées à la maladie détectée
                    disease_description = df2[df2['Disease'] == detected_disease]['Description'].values[0]
                    precautions = df3[df3['Disease'] == detected_disease].values[0]
                    
                    bot_response = (
                        f" TThe detected disease is {detected_disease}. {disease_description}. \n\n"
                        f" Precautions: {', '.join(precautions)} \n\n"
                        f" The other likely diseases are: {', '.join(probable_diseases)}\n\n"
                        f" Here are the probabilities:\n" + 
                        '\n'.join([f'{disease} ({probability:.2f})' for disease, probability in top_diseases])
                    )
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
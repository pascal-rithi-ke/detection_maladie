import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import wordnet

import pandas as pd

# Vérifier et télécharger les ressources NLTK nécessaires
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

# Charger le modèle de langue anglais de SpaCy
nlp = spacy.load("en_core_web_md")

# Define custom stopwords and symptoms keywords
custom_stopwords = set([
    "today", "hi", "hello", "thanks", "thank you", "feel", "feeling", "felt", 
    "like", "feels", "ive", "im", "i'm", "i've", "i", "there", "theres", 
    "day", "week", "month", "come", "comes", "came", "go", "goes", "start", 
    "end", "next", "also", "past", "mild", "slight", "bit", "slightly"
])

symptoms_keywords = set([
    "unwell", "fever", "chill", "sore", "throat", "cough", "dry", "bad",
    "scratchy", "hurt", "swallow", "fatigue", "muscle", "ache", "leg",
    "appetite", "nauseous", "vomit", "nose", "congested", "shortness", 
    "breath", "rash", "skin", "change", "headache"
])

# Add custom stopwords to SpaCy's stopwords
for word in custom_stopwords:
    nlp.Defaults.stop_words.add(word)
    nlp.vocab[word].is_stop = True

def clean_text(text):
    doc = nlp(text)
    filtered_tokens = [
        token.lemma_.lower() for token in doc 
        if not token.is_punct and 
            not token.is_stop and
            not token.like_num and 
            len(token.text) > 2 and
            token.pos_ not in ['PROPN', 'DET'] and
            token.lemma_.lower() in symptoms_keywords
    ]
    return " ".join(filtered_tokens)

# Fonction principale pour traiter le texte
def process_text(text):
    text = clean_text(text)
    return text

# Fonction pour générer un nuage de mots
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=800, background_color='white', stopwords=custom_stopwords, min_font_size=10).generate(text)
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

def search_word_similarity(word):
    df1 = pd.read_csv("../data/cleaned_symptom_severity.csv")
    known_symptoms_array = df1['Symptom'].values
    symptoms_weights = df1['weight'].values
    minimum_similarity_threshold = 0.5
    symptom_similarity_mapping = []

    for symptom, weight in zip(known_symptoms_array, symptoms_weights):
        similarity = nlp(word).similarity(nlp(symptom))
        if similarity > minimum_similarity_threshold:
            symptom_similarity_mapping.append((symptom, similarity, weight))

    # Trier les résultats par similarité décroissante
    symptom_similarity_mapping.sort(key=lambda x: x[1], reverse=True)
    
    # Sélectionner les 17 premiers éléments
    top_17 = symptom_similarity_mapping[:17]
    
    # Extraire les poids des 17 symptômes les plus similaires
    weights = [weight for _, _, weight in top_17]
    
    # Compléter avec des zéros jusqu'à 17 éléments si nécessaire
    while len(weights) < 17:
        weights.append(0)
    
    return weights
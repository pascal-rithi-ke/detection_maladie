import spacy
from spacy.matcher import Matcher
from spacy.lang.en.stop_words import STOP_WORDS

import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Représentation graphique des données
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# Vérifier et télécharger les ressources NLTK nécessaires
required_resources = [
    'punkt', 'stopwords', 'wordnet', 
    'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words', 'tagsets'
]

for resource in required_resources:
    try:
        nltk.data.find(f'corpora/{resource}') if resource in ['punkt', 'stopwords', 'wordnet', 'words'] else nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource)

# Charger le modèle de langue en anglais de Spacy
nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)

# Liste de stopwords personnalisée incluant les expressions composées
custom_stopwords = set(spacy.lang.en.stop_words.STOP_WORDS)
custom_stopwords.update(["today", "I", "I'm", "it's", "there's", "I've", "I'd", "I'll", "I'd", "I'd've", "I'll", "I'll've", "I'm", "I'm'a", "I'm'o", "I'm'a'no", "I'm'o'no", "I've", "I've'a", "I've'o", "I've'a'no", "I've'o'no", "I'd", "I'd'a", "I'd'o", "I'd'a'no", "I'd'o'no", "I'll", "I'll'a", "I'll'o", "I'll'a'no", "I'll'o'no", "I'm", "I'm'a", "I'm'o", "I'm'a'no", "I'm'o'no"])

# Votre liste personnalisée de stopwords
custom_stopwords = set(stopwords.words('english'))
custom_stopwords.update(["hi", "hello", "thanks", "thank you"])

global_stopwords = set(stopwords.words('english'))
global_stopwords.update(custom_stopwords)

# Retirer les verb, pronoun, adverb, adposition, auxillary, conjunction, determiner, interjection, particle, punctuation, symbol, other
def remove_stopwords(text):
    tokens = word_tokenize(text)
    cleaned_tokens = [token for token in tokens if token.lower() not in global_stopwords]
    return ' '.join(cleaned_tokens)

# Fonction pour obtenir la position de wordnet pour le lemmatisation
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

# Fonction pour nettoyer le texte en utilisant spaCy
def clean_text(text):
    doc = nlp(text)
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]
    # Retourner les tokens sous forme de texte

    return ' '.join(tokens)

# Fonction pour lemmatiser le texte
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]
    return ' '.join(lemmatized_tokens)

def preprocess_text(text):
    text = text.lower()
    text = clean_text(text)
    text = lemmatize_text(text)
    text = remove_stopwords(text)
    return text

# Fonction pour générer un nuage de mots
def generate_wordcloud(text):
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = global_stopwords, 
                min_font_size = 10).generate(text)
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.show()
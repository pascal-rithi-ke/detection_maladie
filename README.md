# Detection maladie

# Requierements
* ```pip install -r requirements.txt```

# Back
* ``` cd back```
* ``` virtualenv venv```
* ```python -m venv venv```
* ```source venv/Scripts/activate```
* ```pip install -r requirements.txt```
* ```deactivate```

# Front
* ```cd front```
* ```npm install```
* ```npm run dev```




-----------------------------------


3 Prédictions : 

- Prédiction d'une maladie par la radiographique : Prenons l'exemple du cancer du sein

- Avoir un dataset comprenant des images exclusivement réservé au cancer du sein.
- Avoir un dataset comprenant des images exclusivment réservé a un sein sain.

Nous pouvons soit réalisé la labelisation des seins cancéreux à la main, soit nous pouvons trouver un dataset déjà établi sur lequel nous pouvons travailler directement

 Source des données utilisées :

 https://www.cancerimagingarchive.net/ ( pas encore utilisé )

 https://www.kaggle.com/datasets/awsaf49/cbis-ddsm-breast-cancer-image-dataset

 Dataset comprenant un ensemble d'image de seins présentant des cellules cancéreuses

 Pour, nous allons utiliser un CNN ( réseau neuronal convolutif ) ; voir detection_cancer.py

- Prédiction d'une maladie par chatbot (NLP) 

- Prédiction sur le papier d'une consultation
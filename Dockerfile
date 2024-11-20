# Utiliser une image Python officielle comme image de base
FROM python:3.8-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates

# Installer l'API Kaggle
RUN pip install --no-cache-dir kaggle

# Créer le répertoire pour l'application
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans /app
COPY . /app

# Configurer les identifiants Kaggle depuis la variable d'environnement
ARG KAGGLE_JSON_ENCODED
RUN mkdir /root/.kaggle
RUN echo $KAGGLE_JSON_ENCODED | base64 -d > /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

# Télécharger le modèle depuis Kaggle
RUN kaggle datasets download -d utkarshsaxenadn/weather-classification-resnet152v2 --unzip -f ResNet152V2-Weather-Classification-03.h5

# Exposer les volumes pour les répertoires d'entrée et de sortie
VOLUME ["/input", "/output"]

# Définir les variables d'environnement pour les répertoires d'entrée et de sortie
ENV INPUT_DIR=/input
ENV OUTPUT_DIR=/output

# Lister le contenu de /app pour le débogage
RUN ls -la /app

# Définir la commande à exécuter lorsque le conteneur démarre
CMD ["python", "/app/predict.py", "--input_dir", "/input", "--output_dir", "/output"]



# Utiliser une image Python officielle comme image de base
FROM python:3.8-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates

# Installer l'API Kaggle
RUN pip install --no-cache-dir kaggle

# Créer le répertoire pour l'application
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans /app
COPY . /app

# Configurer les identifiants Kaggle depuis la variable d'environnement
ARG KAGGLE_JSON_ENCODED
RUN mkdir /root/.kaggle
RUN echo $KAGGLE_JSON_ENCODED | base64 -d > /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

# Télécharger le modèle depuis Kaggle
RUN kaggle datasets download -d utkarshsaxenadn/weather-classification-resnet152v2 --unzip -f ResNet152V2-Weather-Classification-03.h5

# Le reste du Dockerfile reste inchangé...

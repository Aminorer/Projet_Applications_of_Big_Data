import os
import shutil
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm
from datetime import datetime
import argparse

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet_v2 import preprocess_input
from tensorflow.keras.models import load_model

# Catégories
class_names = {0: 'cloudy', 1: 'foggy', 2: 'rainy', 3: 'shine', 4: 'sunrise'}

def load_image(path):
    try:
        # Chargement de l'image avec la taille appropriée
        img = load_img(path, target_size=(256, 256))
        img = img_to_array(img)
        # Prétraitement spécifique au modèle ResNet152V2
        img = preprocess_input(img)
        return img
    except Exception as e:
        print(f"Erreur lors du chargement de l'image {path}: {e}")
        return None

def main(input_dir, output_dir):
    # Déplacement des fichiers existants vers le dossier 'old'
    old_dir = os.path.join(output_dir, 'old')
    if not os.path.exists(old_dir):
        os.makedirs(old_dir)
        print(f"Création du dossier {old_dir}")

    # Obtenir la liste des fichiers CSV dans output_predictions
    existing_csv_files = glob(os.path.join(output_dir, 'predictions_*.csv'))
    for file_path in existing_csv_files:
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(old_dir, file_name)
        shutil.move(file_path, dest_path)
        print(f"Déplacement de {file_name} vers {old_dir}")

    image_paths = sorted(glob(os.path.join(input_dir, '*.jpg')))
    print(f"Nombre total d'images: {len(image_paths)}")

    if not image_paths:
        print("Aucune image trouvée dans le répertoire d'entrée.")
        return

    # Lire les prédictions précédentes depuis les fichiers CSV dans le dossier 'old'
    previous_predictions = {}
    csv_files = glob(os.path.join(old_dir, 'predictions_*.csv'))

    if csv_files:
        # Trier les fichiers CSV par date de modification décroissante (le plus récent en premier)
        csv_files.sort(key=os.path.getmtime, reverse=True)
        for csv_file in csv_files:
            df = pd.read_csv(csv_file)
            # Itérer sur les lignes
            for idx, row in df.iterrows():
                image_name = row['image_name']
                prediction_label = row['prediction_label']
                if image_name not in previous_predictions:
                    # Puisque les fichiers sont triés du plus récent au plus ancien,
                    # nous gardons la première occurrence
                    previous_predictions[image_name] = prediction_label

    # Listes pour stocker les résultats
    image_names = []
    prediction_labels = []
    first_analysis_flags = []

    # Listes pour les images à prédire
    images_to_predict = []
    paths_to_predict = []

    # Traitement des images
    for path in tqdm(image_paths, desc="Traitement des images"):
        image_name = os.path.basename(path)
        if image_name in previous_predictions:
            # Image déjà prédite
            prediction_label = previous_predictions[image_name]
            image_names.append(image_name)
            prediction_labels.append(prediction_label)
            first_analysis_flags.append('no')
        else:
            # Image à prédire
            img = load_image(path)
            if img is not None:
                images_to_predict.append(img)
                paths_to_predict.append(image_name)
            else:
                print(f"Échec du chargement de l'image {image_name}")

    # Prédire les images nécessaires
    if images_to_predict:
        images_to_predict = np.array(images_to_predict)
        # Chargement du modèle
        model = load_model('ResNet152V2-Weather-Classification-03.h5')
        # Prédictions
        preds = np.argmax(model.predict(images_to_predict), axis=-1)
        pred_labels = [class_names[pred] for pred in preds]
        # Ajouter les résultats
        image_names.extend(paths_to_predict)
        prediction_labels.extend(pred_labels)
        first_analysis_flags.extend(['yes'] * len(pred_labels))

    if not image_names:
        print("Aucune image à traiter.")
        return

    # Préparation du DataFrame des résultats
    results_df = pd.DataFrame({
        'image_name': image_names,
        'prediction_label': prediction_labels,
        'first_analysis': first_analysis_flags
    })

    # Enregistrement des résultats dans un fichier CSV horodaté
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'predictions_{timestamp}.csv'
    results_df.to_csv(os.path.join(output_dir, output_file), index=False)
    print(f"Prédictions enregistrées dans {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Classification Météo des Images')
    parser.add_argument('--input_dir', type=str, required=True, help="Chemin vers le répertoire des images d'entrée")
    parser.add_argument('--output_dir', type=str, required=True, help="Chemin vers le répertoire de sortie")
    args = parser.parse_args()
    main(args.input_dir, args.output_dir)

# Weather Image Classification with Docker

## Description

This project is an image classification application that categorizes weather images using a pre-trained ResNet152V2 model. The application processes images from an input directory and outputs the classification results to a CSV file. It is designed to efficiently handle large numbers of images by avoiding reprocessing images that have already been classified.

## Features

- **Weather Classification** : Classifies images into one of the following categories:
  - `cloudy`
  - `foggy`
  - `rainy`
  - `shine`
  - `sunrise`
- **Efficient Processing** : Skips images that have already been processed to save time.
- **Result Logging** : Saves classification results with timestamps for easy tracking.
- **Dockerized Application** : Run the application within a Docker container for consistency and ease of setup.

## Prerequisites

- **Docker** : Ensure Docker is installed on your machine.
  - [Install Docker](https://docs.docker.com/get-docker/) if you haven't already.

## Installation and Setup

### Step 1 : Clone the Repository

Open your terminal and run :

```bash
git clone https://github.com/Aminorer/Projet_Applications_of_Big_Data.git
cd Projet_Applications_of_Big_Data
```

### Step 2 : Obtain the Pre-trained Model

You need the `ResNet152V2-Weather-Classification-03.h5` model file to run the application.

#### Option A : Download from Kaggle (Manual Download)

1. **Navigate to the Dataset Page** :

   - Visit the dataset page : [Weather Classification ResNet152V2](https://www.kaggle.com/datasets/utkarshsaxenadn/weather-classification-resnet152v2).

2. **Download the Model File** :

   - Download `ResNet152V2-Weather-Classification-03.h5` from the dataset.

3. **Place the Model File** :

   - Move the downloaded `.h5` file to the root directory of the project (`Projet_Applications_of_Big_Data`).

**Note** : The model file is large 

### Step 3 : Prepare Input and Output Directories

Create directories for input images and output predictions :

```bash
mkdir input_images
mkdir output_predictions
```

- **Input Images**: Place the images you want to classify into the `input_images` directory.
- **Supported Image Formats** : `.jpg`

### Step 4 : Build the Docker Image

Build the Docker image using the provided `Dockerfile`:

```bash
docker build -t weather-classifier .
```

This command builds the image and tags it as `weather-classifier`.

### Step 5 : Run the Docker Container

Run the application using Docker, mounting the input and output directories :

```bash
docker run --rm \
  -v "$(pwd)/input_images:/input" \
  -v "$(pwd)/output_predictions:/output" \
  weather-classifier
```

- **Explanation** :
  - `--rm`: Automatically removes the container when it exits.
  - `-v "$(pwd)/input_images:/input"`: Mounts the `input_images` directory to `/input` in the container.
  - `-v "$(pwd)/output_predictions:/output"`: Mounts the `output_predictions` directory to `/output` in the container.

**For Windows** :

- On Command Prompt :

  ```cmd
  docker run --rm -v "%cd%/input_images:/input" -v "%cd%/output_predictions:/output" weather-classifier
  ```

- On PowerShell :

  ```powershell
  docker run --rm -v "${PWD}/input_images:/input" -v "${PWD}/output_predictions:/output" weather-classifier
  ```

## Usage

- **Place Images** : Add the images you want to classify into the `input_images` directory.
- **Run the Application** : Use the Docker command from Step 5 to run the classifier.
- **View Results** : After processing, check the `output_predictions` directory for the CSV output.

## Understanding the Output

- **CSV Output File** : A file named `predictions_YYYYMMDD_HHMMSS.csv` will be created in the `output_predictions` directory.
- **CSV Columns** :
  - `image_name`: Name of the image file.
  - `prediction_label`: Predicted weather category.
  - `first_analysis`:
    - `yes` : Image was analyzed for the first time.
    - `no` : Prediction was retrieved from previous results.

## How It Works

- The application scans the `/input` directory for images.
- It checks previous prediction files to avoid reprocessing images.
- New images are processed, and predictions are made using the pre-trained model.
- Results are saved in the `/output` directory with a timestamped CSV file.
- Previous prediction files are moved to the `/output/old` directory within the container (this is internal and does not affect your host directories).

## Notes

- **Avoiding Reprocessing**: The script checks previous prediction files to skip images that have already been classified.
- **Image Naming**:
  - Ensure image names are unique.
  - Avoid special characters and spaces in image names to prevent issues.
- **Model File**:
  - Must be named `ResNet152V2-Weather-Classification-03.h5`.
  - Located in the project root directory.

## Troubleshooting

- **Cannot Find the Model File**:
  - Ensure the `ResNet152V2-Weather-Classification-03.h5` file is in the project root directory.
  - Verify the file name and location.

- **Permission Errors with Docker**:
  - Ensure Docker has permissions to access the directories.
  - On Windows, you may need to adjust sharing settings in Docker Desktop.

- **Missing Dependencies**:
  - The Docker image includes all necessary dependencies.
  - Ensure the image builds successfully without errors.

- **Errors with Image Loading**:
  - Check that your images are valid and not corrupted.
  - Ensure image formats are supported.

## Project Structure

```
Projet_Applications_of_Big_Data/
├── predict.py
├── requirements.txt
├── Dockerfile
├── ResNet152V2-Weather-Classification-03.h5
├── input_images/
├── output_predictions/
│   └── old/

```

- **predict.py**: Main application script.
- **requirements.txt**: Lists Python dependencies.
- **Dockerfile**: Defines how to build the Docker image.
- **input_images/**: Directory to place input images.
- **output_predictions/**: Directory where output CSV files will be saved.
- **output_predictions/old/**: Directory containing previous prediction CSV files.
- **ResNet152V2-Weather-Classification-03.h5**: Pre-trained model file.

## Dependencies

All dependencies are included in the Docker image.

- **Python Packages** :
  - `tensorflow`
  - `keras`
  - `numpy`
  - `pandas`
  - `tqdm`
  - `Pillow`


## Contact

For questions or support, please contact :

- **Amine BELAHBIB , Rémy DIMACHKIE , Zakaria EL FERDI, Yanis BESTAOUI**
- **Email**: [amine.belahbib@efrei.net](mailto:amine.belahbib@efrei.net)
- **GitHub**: [Aminorer](https://github.com/Aminorer)


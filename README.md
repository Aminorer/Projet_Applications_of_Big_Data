# Weather Image Classification with Docker

## Description

This project is an image classification application that categorizes weather images using a pre-trained ResNet152V2 model. The application processes images from an input directory and outputs the classification results to a CSV file. It is designed to efficiently handle large numbers of images by avoiding reprocessing images that have already been classified.

## Features

- **Weather Classification**: Classifies images into one of the following categories:
  - `cloudy`
  - `foggy`
  - `rainy`
  - `shine`
  - `sunrise`
- **Efficient Processing**: Skips images that have already been processed to save time.
- **Result Logging**: Saves classification results with timestamps for easy tracking.
- **Dockerized Application**: Run the application within a Docker container for consistency and ease of setup.

## Prerequisites

- **Docker**: Ensure Docker is installed on your machine.
  - [Install Docker](https://docs.docker.com/get-docker/) if you haven't already.

## Installation and Setup

### Step 1: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/yourusername/weather-classifier.git
cd weather-classifier
```

### Step 2: Obtain the Pre-trained Model

You need the `ResNet152V2-Weather-Classification-03.h5` model file to run the application.

#### Option A: Download from Kaggle

1. **Sign Up or Log In to Kaggle**:

   - Go to [Kaggle](https://www.kaggle.com/) and sign up for an account if you don't have one.

2. **Obtain Kaggle API Credentials**:

   - Click on your profile picture in the top right corner and select **"Account"**.
   - Scroll down to the **"API"** section and click **"Create New API Token"**.
   - A file named `kaggle.json` will be downloaded.

3. **Place `kaggle.json` in the Project Directory**:

   - Move the `kaggle.json` file to the root directory of the project (`weather-classifier`).

4. **Download the Model Using the Kaggle API**:

   - Run the following commands in your terminal:

     ```bash
     docker run --rm -v "$(pwd)":/app -w /app python:3.8-slim bash -c "\
       pip install kaggle && \
       mkdir -p /root/.kaggle && \
       cp kaggle.json /root/.kaggle/ && \
       chmod 600 /root/.kaggle/kaggle.json && \
       kaggle datasets download -d utkarshsaxenadn/weather-classification-resnet152v2 --unzip -f ResNet152V2-Weather-Classification-03.h5"
     ```

   - This command uses a temporary Docker container to download the model file directly into your project directory.

5. **Verify the Model File**:

   - Ensure that the file `ResNet152V2-Weather-Classification-03.h5` is now present in your project directory.

#### Option B: Manual Download (Alternative)

If you prefer to download the model manually:

1. **Navigate to the Dataset Page**:

   - Visit the dataset page: [Weather Classification ResNet152V2](https://www.kaggle.com/datasets/utkarshsaxenadn/weather-classification-resnet152v2).

2. **Download the Model File**:

   - Download `ResNet152V2-Weather-Classification-03.h5` from the dataset.

3. **Place the Model File**:

   - Move the downloaded `.h5` file to the root directory of the project (`weather-classifier`).

**Note**: The model file is large (~230 MB). Ensure you have sufficient disk space.

### Step 3: Prepare Input and Output Directories

Create directories for input images and output predictions:

```bash
mkdir input_images
mkdir output_predictions
```

- **Input Images**: Place the images you want to classify into the `input_images` directory.
- **Supported Image Formats**: `.jpg`, `.jpeg`, `.png`

### Step 4: Build the Docker Image

Build the Docker image using the provided `Dockerfile`:

```bash
docker build -t weather-classifier .
```

This command builds the image and tags it as `weather-classifier`.

### Step 5: Run the Docker Container

Run the application using Docker, mounting the input and output directories:

```bash
docker run --rm \
  -v "$(pwd)/input_images:/input" \
  -v "$(pwd)/output_predictions:/output" \
  weather-classifier
```

- **Explanation**:
  - `--rm`: Automatically removes the container when it exits.
  - `-v "$(pwd)/input_images:/input"`: Mounts the `input_images` directory to `/input` in the container.
  - `-v "$(pwd)/output_predictions:/output"`: Mounts the `output_predictions` directory to `/output` in the container.

**Note for Windows Users**:

- On Command Prompt:

  ```cmd
  docker run --rm -v "%cd%/input_images:/input" -v "%cd%/output_predictions:/output" weather-classifier
  ```

- On PowerShell:

  ```powershell
  docker run --rm -v "${PWD}/input_images:/input" -v "${PWD}/output_predictions:/output" weather-classifier
  ```

## Usage

- **Place Images**: Add the images you want to classify into the `input_images` directory.
- **Run the Application**: Use the Docker command from Step 5 to run the classifier.
- **View Results**: After processing, check the `output_predictions` directory for the CSV output.

## Understanding the Output

- **CSV Output File**: A file named `predictions_YYYYMMDD_HHMMSS.csv` will be created in the `output_predictions` directory.
- **CSV Columns**:
  - `image_name`: Name of the image file.
  - `prediction_label`: Predicted weather category.
  - `first_analysis`:
    - `yes`: Image was analyzed for the first time.
    - `no`: Prediction was retrieved from previous results.

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
weather-classifier/
├── predict.py
├── requirements.txt
├── Dockerfile
├── ResNet152V2-Weather-Classification-03.h5
├── input_images/
├── output_predictions/
```

- **predict.py**: Main application script.
- **requirements.txt**: Lists Python dependencies.
- **Dockerfile**: Defines how to build the Docker image.
- **input_images/**: Directory to place input images.
- **output_predictions/**: Directory where output CSV files will be saved.
- **ResNet152V2-Weather-Classification-03.h5**: Pre-trained model file (must be obtained separately).

## Dependencies

All dependencies are included in the Docker image.

- **Python Packages**:
  - `tensorflow`
  - `keras`
  - `numpy`
  - `pandas`
  - `tqdm`
  - `Pillow`

## Advanced Usage

### Customizing Input and Output Paths

If you wish to use different directories for input and output, modify the Docker run command:

```bash
docker run --rm \
  -v "/path/to/your/images:/input" \
  -v "/path/to/your/output:/output" \
  weather-classifier
```

### Rebuilding the Docker Image

If you make changes to the `predict.py` script or other code, rebuild the Docker image:

```bash
docker build -t weather-classifier .
```

## Cleaning Up

To remove the Docker image from your system:

```bash
docker rmi weather-classifier
```

## Contact

For questions or support, please contact:

- **BELAHBIB Amine**
- **Email**: [amine.belahbib@efrei.net](mailto:amine.belahbib@efrei.net)
- **GitHub**: [Aminorer](https://github.com/Aminorer)


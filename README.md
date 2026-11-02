# Parkinson's Disease Detection

A Python project that explores voice measurements for Parkinson's disease classification and provides a Flask web interface for uploading WAV audio.

> **Medical disclaimer:** This project is for educational and research purposes only. It is not a medical device and must not be used to diagnose, treat, or rule out Parkinson's disease. Consult a qualified healthcare professional for medical advice.

## Features

- Uses the voice-measurement dataset in `data.csv` for model training.
- Includes scripts for model training, feature extraction, and prediction.
- Provides a Flask web application with registration, login, dashboards, and an audio-upload page.
- Uses Praat through `praat-parselmouth` to extract voice measurements from WAV files.
- Saves trained model and feature scaler artifacts as `model_knn.pkl` and `scaling.pkl`.

## Project structure

| File or directory | Purpose |
| --- | --- |
| `app.py` | Small launcher for the Flask application. |
| `app_knn.py` | Flask routes and application setup. |
| `feature_extraction.py` | Extracts voice measurements from WAV files. |
| `model_utils.py` | Loads the model and scaler and makes predictions. |
| `train_model.py` | Trains a classifier from `data.csv` and saves the model and scaler. |
| `parkinson_detection.py` | Separate data preparation and K-nearest-neighbor training script. |
| `data.csv` | Voice-measurement dataset used by the training scripts. |
| `model_knn.pkl`, `scaling.pkl` | Serialized model and scaler used by the web app. |
| `templates/`, `static/` | Flask HTML templates and static assets. |
| `init_db.py` | Creates the MySQL database and tables used by the web app. |

## Requirements

- Python 3.9 or later
- MySQL Server
- Git (for cloning the repository)

Python packages are listed in `requirements.txt`. The web app also imports `pycountry`, which is not currently listed there; install it separately as shown below.

## Installation

Clone the repository and enter its directory:

```bash
git clone https://github.com/chetandangwal001-svg/parkinson-disease-detection.git
cd parkinson-disease-detection
```

Create and activate a virtual environment.

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pycountry
```

## Database configuration

The web application requires a local MySQL server and a database named `user_db`. Before running the setup script, configure the MySQL connection settings in `init_db.py` and `app_knn.py` for your environment. Then create the database tables:

```bash
python init_db.py
```

Do not commit database passwords or Flask secret keys. Store secrets outside the source code before publishing or deploying the application, and rotate any credentials that may already have been exposed.

## Model files

The repository includes `model_knn.pkl` and `scaling.pkl`. The web application expects both files to be present in the project root.

To regenerate the model and scaler from `data.csv`, run:

```bash
python train_model.py
```

This script trains a `RandomForestClassifier` and saves its outputs to the model and scaler filenames above. `parkinson_detection.py` is a separate K-nearest-neighbor training script.

## Run the application

After configuring MySQL and ensuring the model files are present, start the Flask app:

```bash
python app_knn.py
```

Open the local address printed by Flask (typically `http://127.0.0.1:5000`) in your browser. The `app.py` file is also available as a launcher:

```bash
python app.py
```

## Dataset

`data.csv` contains 195 voice-recording examples with measurements such as fundamental frequency, jitter, shimmer, noise-to-harmonics ratio, and a `status` label. The source dataset is the [UCI Parkinson's Disease voice dataset](https://archive.ics.uci.edu/dataset/174/parkinsons).

## Current limitation

The WAV feature extractor currently returns six measurements, while `model_utils.py` expects fourteen input features. As a result, audio-upload predictions may fail until the extracted features and model input schema are made consistent.

## Disclaimer

Predictions are experimental outputs from a machine-learning project and are not clinically validated. Do not use them to make health decisions.

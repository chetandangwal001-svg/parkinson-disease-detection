import sys
from feature_extraction import extract_voice_features
from model_utils import load_model_and_scaler, predict_from_features

if len(sys.argv) < 2:
    print("Usage: python debug_audio.py <wav_file_path>")
    sys.exit(1)

wav_path = sys.argv[1]
model, scaler = load_model_and_scaler()

# Extract features
features = extract_voice_features(wav_path)
print(f"\nExtracted features from {wav_path}:")
for name, value in features.items():
    print(f"  {name}: {value:.6f}")

# Make prediction
prediction = predict_from_features(model, scaler, features)
result = "Parkinson's" if prediction == 1 else "Healthy"
print(f"\nPrediction: {result}")

# Also show what the training data ranges were
import pandas as pd
FEATURE_COLUMNS = ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Shimmer", "NHR"]
df = pd.read_csv("data.csv")

print(f"\nTraining data ranges (for reference):")
for col in FEATURE_COLUMNS:
    healthy = df[df["status"] == 0][col]
    parkinsons = df[df["status"] == 1][col]
    your_val = features[col]
    
    h_mean, h_std = healthy.mean(), healthy.std()
    p_mean, p_std = parkinsons.mean(), parkinsons.std()
    
    print(f"\n  {col}:")
    print(f"    Your value:     {your_val:.6f}")
    print(f"    Healthy (mean ± std): {h_mean:.6f} ± {h_std:.6f}")
    print(f"    Parkinson's (mean ± std): {p_mean:.6f} ± {p_std:.6f}")

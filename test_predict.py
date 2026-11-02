from feature_extraction import extract_voice_features
from model_utils import load_model_and_scaler, predict_from_features

# Load model and scaler
model, scaler = load_model_and_scaler()

# Extract features from test WAV
wav_path = 'uploads/test_sine.wav'
try:
    feature_dict = extract_voice_features(wav_path)
    print(f'Features extracted: {feature_dict}')
    
    # Make prediction
    prediction = predict_from_features(model, scaler, feature_dict)
    result = 'Parkinson\'s Disease Detected' if prediction == 1 else 'Parkinson\'s Disease Not Detected'
    print(f'RESULT: {result}')
except Exception as e:
    print(f'ERROR: {e}')

import math
import wave
import struct
from feature_extraction import extract_voice_features

# Generate 1 second of a 220 Hz sine wave (A3-ish) at 16kHz
sample_rate = 16000
duration = 1.0
freq = 220.0
n_samples = int(sample_rate * duration)
filename = 'uploads/test_sine.wav'

# ensure uploads exists
import os
os.makedirs('uploads', exist_ok=True)

with wave.open(filename, 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 16-bit
    wf.setframerate(sample_rate)
    for i in range(n_samples):
        sample = 0.5 * math.sin(2 * math.pi * freq * (i / sample_rate))
        val = int(sample * 32767.0)
        data = struct.pack('<h', val)
        wf.writeframesraw(data)

print('WAV written:', filename)
print('Extracting features...')
features = extract_voice_features(filename)
print(features)

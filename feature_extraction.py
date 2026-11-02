import os
from parselmouth import Sound
from parselmouth.praat import call

ALLOWED_EXTENSIONS = {"wav"}


def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_voice_features(wav_path):
    if not os.path.exists(wav_path):
        raise FileNotFoundError(f"Audio file not found: {wav_path}")

    sound = Sound(wav_path)
    pitch = sound.to_pitch()
    mean_f0 = call(pitch, "Get mean", 0, 0, "Hertz")
    min_f0 = call(pitch, "Get minimum", 0, 0, "Hertz", "Parabolic")
    max_f0 = call(pitch, "Get maximum", 0, 0, "Hertz", "Parabolic")
    point_process = call(sound, "To PointProcess (periodic, cc)", 75, 500)

    jitter_local = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    shimmer_local = call(
        [sound, point_process],
        "Get shimmer (local)",
        0,
        0,
        0.0001,
        0.02,
        1.3,
        1.6,
    )
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    nhr = call(harmonicity, "Get mean", 0, 0)

    if None in (mean_f0, min_f0, max_f0, jitter_local, shimmer_local, nhr):
        raise ValueError("Could not extract all required voice features from the WAV file.")

    return {
        "MDVP:Fo(Hz)": float(mean_f0),
        "MDVP:Fhi(Hz)": float(max_f0),
        "MDVP:Flo(Hz)": float(min_f0),
        "MDVP:Jitter(%)": float(jitter_local) * 100.0,
        "MDVP:Shimmer": float(shimmer_local),
        "NHR": float(nhr),
    }

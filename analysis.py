import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def analyze_song_structure(audio_path):
    # Load the audio file
    y, sr = librosa.load(audio_path)

    # Harmonic-percussive source separation
    harmonic, percussive = librosa.effects.hpss(y)

    # Compute chroma features from the harmonic signal
    chromagram = librosa.feature.chroma_cqt(harmonic, sr=sr)

    # Compute the Recurrence Matrix
    recurrence_matrix = librosa.segment.recurrence_matrix(
        chromagram, mode="affinity", sym=True
    )

    # Enhance diagonals with a median filter (for cleaner segmentation)
    recurrence_matrix = librosa.segment.path_enhance(recurrence_matrix, size=17)

    # Use librosa's Decomposition and Segmentation methods
    # to extract the segments. This involves some complex steps
    # like spectral clustering which librosa handles internally.
    tempo, beats = librosa.beat.beat_track(y, sr=sr)
    segments = librosa.segment.agglomerative(chromagram, beats)

    # Plotting the results
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(recurrence_matrix, x_axis="time", y_axis="time", sr=sr)
    plt.title("Recurrence Matrix")
    plt.colorbar()
    plt.tight_layout()

    plt.figure(figsize=(12, 4))
    librosa.display.specshow(
        librosa.amplitude_to_db(chromagram, ref=np.max),
        y_axis="chroma",
        x_axis="time",
        sr=sr,
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title("Chroma Features")
    plt.tight_layout()

    plt.figure(figsize=(12, 4))
    librosa.display.waveplot(y, sr=sr, alpha=0.6)
    plt.vlines([t for t in librosa.frames_to_time(segments, sr=sr)], -1, 1, color="r")
    plt.title("Audio Waveform and Segmented Sections")
    plt.tight_layout()

    plt.show()


# Example usage
audio_path = "Assets/Dennis_Quin_-_Dedication_To_House_Music_(Extended_Mix).mp3"  # Replace with your audio file path
analyze_song_structure(audio_path)

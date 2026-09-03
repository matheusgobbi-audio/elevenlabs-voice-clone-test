"""
Goal: visually compare the REFERENCE recording (short sentence, the same
one the API generates) against the audio the API generated from that
condition's clone, using spectrograms.

Important: the comparison uses reference/{condition}.wav, not the long
paragraph in samples/ used for cloning. Different text would invalidate
the comparison.

This turns "I think it got worse" into something concrete that can be
shown and explained technically in the README.
"""

import json
from pathlib import Path
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
REFERENCE_DIR = BASE_DIR / "reference"
RESULTS_DIR = BASE_DIR / "results"


REFERENCE_EXTENSIONS = ("wav", "mp3", "m4a", "ogg", "oga", "flac")


def find_reference_file(condition_name: str):
    for ext in REFERENCE_EXTENSIONS:
        candidate = REFERENCE_DIR / f"{condition_name}.{ext}"
        if candidate.exists():
            return candidate
    return None


# Fixed scale for every spectrogram, so the comparison across conditions
# is visual and direct: same colormap, same dynamic-range window (dB) and
# same frequency limit on every panel.
CMAP = "magma"
DB_FLOOR = -80.0   # bottom of the color scale, in dB below the signal's own peak
DB_CEIL = 0.0      # top of the color scale (peak = 0 dB)
FMAX = 16000       # Hz; the API output never exceeds this, so it is the
                   # band where the comparison is meaningful

# ref=np.max normalizes each panel by its own peak: the silence between
# words drops to the dark end of the colormap and speech shows up bright,
# so the noise-floor difference between conditions is immediately
# visible. The scale becomes relative (dynamic), not absolute level
# across conditions.
def _spectrogram_db(y):
    return librosa.amplitude_to_db(abs(librosa.stft(y)), ref=np.max)


def plot_comparison(original_path: Path, generated_path: Path, condition_name: str):
    y_orig, sr_orig = librosa.load(original_path, sr=None)
    y_gen, sr_gen = librosa.load(generated_path, sr=None)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)

    for ax, (title, y, sr) in zip(
        axes,
        [
            (f"Original - {condition_name}", y_orig, sr_orig),
            (f"AI-generated - {condition_name}", y_gen, sr_gen),
        ],
    ):
        img = librosa.display.specshow(
            _spectrogram_db(y),
            sr=sr,
            x_axis="time",
            y_axis="hz",
            ax=ax,
            cmap=CMAP,
            vmin=DB_FLOOR,
            vmax=DB_CEIL,
        )
        ax.set_title(title)
        ax.set_ylim(0, FMAX)

    fig.colorbar(img, ax=axes, format="%+2.0f dB", location="right", pad=0.02)
    output_path = RESULTS_DIR / f"spectrogram_{condition_name}.png"
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {output_path}")


def main():
    voice_ids_path = RESULTS_DIR / "voice_ids.json"
    if not voice_ids_path.exists():
        raise SystemExit("Run clone_voice.py and generate_speech.py first.")

    with open(voice_ids_path) as f:
        voice_ids = json.load(f)

    for condition_name in voice_ids:
        original_path = find_reference_file(condition_name)
        generated_path = RESULTS_DIR / f"generated_{condition_name}.mp3"
        if original_path and generated_path.exists():
            plot_comparison(original_path, generated_path, condition_name)
        else:
            print(f"Warning: missing reference/{condition_name}.* or generated_{condition_name}.mp3, skipping.")


if __name__ == "__main__":
    main()

"""
Objetivo: comparar visualmente a gravação de REFERÊNCIA (frase curta,
mesma que a IA gera) com o áudio que a IA gerou a partir do clone
daquela condição, usando espectrogramas.

Importante: a comparação usa reference/{condition}.wav, não o
parágrafo longo em samples/ usado para a clonagem. Textos diferentes
invalidariam a comparação.

Isso transforma "eu acho que ficou pior" em algo concreto, que dá pra
mostrar e explicar tecnicamente no README.
"""

import json
from pathlib import Path
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


def plot_comparison(original_path: Path, generated_path: Path, condition_name: str):
    y_orig, sr_orig = librosa.load(original_path, sr=None)
    y_gen, sr_gen = librosa.load(generated_path, sr=None)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    d_orig = librosa.amplitude_to_db(abs(librosa.stft(y_orig)), ref=1.0)
    librosa.display.specshow(d_orig, sr=sr_orig, x_axis="time", y_axis="hz", ax=axes[0])
    axes[0].set_title(f"Original - {condition_name}")

    d_gen = librosa.amplitude_to_db(abs(librosa.stft(y_gen)), ref=1.0)
    librosa.display.specshow(d_gen, sr=sr_gen, x_axis="time", y_axis="hz", ax=axes[1])
    axes[1].set_title(f"Gerado pela IA - {condition_name}")

    plt.tight_layout()
    output_path = RESULTS_DIR / f"spectrogram_{condition_name}.png"
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Salvo: {output_path}")


def main():
    voice_ids_path = RESULTS_DIR / "voice_ids.json"
    if not voice_ids_path.exists():
        raise SystemExit("Rode clone_voice.py e generate_speech.py primeiro.")

    with open(voice_ids_path) as f:
        voice_ids = json.load(f)

    for condition_name in voice_ids:
        original_path = find_reference_file(condition_name)
        generated_path = RESULTS_DIR / f"generated_{condition_name}.mp3"
        if original_path and generated_path.exists():
            plot_comparison(original_path, generated_path, condition_name)
        else:
            print(f"Aviso: faltando reference/{condition_name}.* ou generated_{condition_name}.mp3, pulando.")


if __name__ == "__main__":
    main()

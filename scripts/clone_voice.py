"""
Goal: take each recording in samples/ (in any common format: wav, mp3,
m4a, ogg, oga, flac) and create a separate voice clone on ElevenLabs
for each one (Instant Voice Cloning).

Before uploading, each file is converted to MP3 320kbps (above the
192kbps minimum recommended by ElevenLabs; their docs state that higher
bitrates bring no perceptible difference in clone quality, but WAV can
cause upload problems, so MP3 is still the right choice). The conversion
is applied equally to every condition, so it introduces no bias in the
comparison.

Requires ffmpeg installed and available on PATH.
"""

import os
import json
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise SystemExit(
        "ELEVENLABS_API_KEY not found. Copy .env.example to .env "
        "and paste your key into it."
    )

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "samples"
CONVERTED_DIR = BASE_DIR / "samples_mp3"
RESULTS_DIR = BASE_DIR / "results"
CONVERTED_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

HEADERS = {"xi-api-key": API_KEY}
SUPPORTED_PATTERNS = ("*.wav", "*.mp3", "*.m4a", "*.ogg", "*.oga", "*.flac")

MIME_TYPES = {
    ".wav": "audio/wav",
    ".mp3": "audio/mpeg",
    ".m4a": "audio/mp4",
    ".ogg": "audio/ogg",
    ".oga": "audio/ogg",
    ".flac": "audio/flac",
}

# studio_96_32 is the deliberately elevated-spec capture (96kHz,
# lossless), compared against the standard studio delivery
# (studio_clean, already MP3). Not converted, to preserve the native
# format of that specific comparison.
SKIP_CONVERSION = {"studio_96_32"}


def find_sample_files():
    files = []
    for pattern in SUPPORTED_PATTERNS:
        files.extend(SAMPLES_DIR.glob(pattern))
    return sorted(files)


def ensure_mp3(audio_path: Path) -> Path:
    """Convert to MP3 320kbps, reusing the file if already converted before."""
    mp3_path = CONVERTED_DIR / f"{audio_path.stem}.mp3"
    if mp3_path.exists():
        return mp3_path

    subprocess.run(
        ["ffmpeg", "-y", "-i", str(audio_path), "-b:a", "320k", str(mp3_path)],
        check=True,
        capture_output=True,
    )
    print(f"Converted: {audio_path.name} -> {mp3_path.name}")
    return mp3_path


def clone_voice(name: str, audio_path: Path) -> str:
    url = "https://api.elevenlabs.io/v1/voices/add"
    mime_type = MIME_TYPES.get(audio_path.suffix.lower(), "application/octet-stream")
    with open(audio_path, "rb") as f:
        files = {"files": (audio_path.name, f, mime_type)}
        data = {"name": name}
        response = requests.post(url, headers=HEADERS, data=data, files=files)
    response.raise_for_status()
    voice_id = response.json()["voice_id"]
    print(f"Clone created: {name} -> {voice_id}")
    return voice_id


def main():
    audio_files = find_sample_files()
    if not audio_files:
        raise SystemExit(
            "No audio files found in samples/ "
            "(accepted formats: wav, mp3, m4a, ogg, oga, flac)."
        )

    output_path = RESULTS_DIR / "voice_ids.json"
    voice_ids = {}
    if output_path.exists():
        with open(output_path) as f:
            voice_ids = json.load(f)

    for audio_path in audio_files:
        condition_name = audio_path.stem  # e.g. phone_home_open
        if condition_name in voice_ids:
            print(f"Already cloned, skipping: {condition_name}")
            continue
        if condition_name in SKIP_CONVERSION:
            upload_path = audio_path
            print(f"Uploading without conversion (spec test): {condition_name}")
        else:
            upload_path = ensure_mp3(audio_path)
        voice_ids[condition_name] = clone_voice(condition_name, upload_path)
        with open(output_path, "w") as f:
            json.dump(voice_ids, f, indent=2)

    print(f"\nUpdated {output_path}")


if __name__ == "__main__":
    main()

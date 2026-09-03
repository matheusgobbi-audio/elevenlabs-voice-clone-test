"""
Goal: take each voice_id created (one per recording condition) and ask
the API to generate the SAME test sentence with each of them.

This isolates the variable under test (quality of the input recording),
because the generated text is identical across all conditions; only the
original recording behind each clone changes.
"""

import os
import json
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

# Same sentence for every condition, so the comparison is fair.
TEST_TEXT = (
    "This is a voice cloning test to evaluate how the quality of the "
    "original recording affects the generated result."
)

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
HEADERS = {"xi-api-key": API_KEY, "Content-Type": "application/json"}


def generate_speech(voice_id: str, condition_name: str):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": TEST_TEXT,
        "model_id": "eleven_multilingual_v2",
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()

    output_path = RESULTS_DIR / f"generated_{condition_name}.mp3"
    with open(output_path, "wb") as f:
        f.write(response.content)
    print(f"Generated: {output_path}")


def main():
    voice_ids_path = RESULTS_DIR / "voice_ids.json"
    if not voice_ids_path.exists():
        raise SystemExit("Run clone_voice.py first, to generate voice_ids.json.")

    with open(voice_ids_path) as f:
        voice_ids = json.load(f)

    for condition_name, voice_id in voice_ids.items():
        output_path = RESULTS_DIR / f"generated_{condition_name}.mp3"
        if output_path.exists():
            print(f"Already generated, skipping: {condition_name}")
            continue
        generate_speech(voice_id, condition_name)


if __name__ == "__main__":
    main()

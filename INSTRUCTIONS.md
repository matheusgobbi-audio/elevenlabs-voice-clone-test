# How to run this project

## 1. Confirm you have Python installed
Open a terminal and run:

    python3 --version

If a version shows up (e.g. Python 3.11), go to step 2.
If it errors, download from https://www.python.org/downloads/ and install first.

## 2. Enter the project folder

    cd path/to/elevenlabs-voice-clone-test

## 3. Create an isolated environment
This keeps this project's libraries from interfering with anything else.

    python3 -m venv venv
    source venv/bin/activate

You'll see "(venv)" appear at the start of the terminal line when it's active.
Run "source venv/bin/activate" every time you open a new terminal to keep
working on this project.

## 4. Install the dependencies
    pip install -r requirements.txt

You also need ffmpeg installed on the system (not a Python package; it's
used by clone_voice.py to convert audio to MP3 before upload, and by
librosa to read formats like m4a and ogg). If you don't have it, install
with:

    brew install ffmpeg

If you don't have Homebrew, get it at https://brew.sh first.

## 5. Configure your API key
Copy the example file:

    cp .env.example .env

Open .env in a text editor and paste your API key, found at elevenlabs.io,
in your profile, "API Keys" section (Instant Voice Cloning needs a paid plan).

Never put the key directly in the scripts, and never commit the .env file.
It's already listed in .gitignore so it won't be committed by accident.

## 6. Organize your recorded audio
If your files already follow a naming convention different from the one the
project expects, create a raw/ folder at the project root, put the 14
original files inside it (without renaming anything), and run:

    python scripts/setup_from_raw.py

This copies the files into samples/ and reference/ with the correct names,
based on the mapping defined at the top of the script. Check the terminal
output to make sure all 14 files were recognized; none should show up as
"unrecognized pattern".

If you prefer to name them manually, each condition needs TWO files, with
the same name (without extension), in different folders. Any common format
works (wav, mp3, m4a, ogg, oga, flac):

    samples/condition_bad.m4a     (long paragraph, used for cloning)
    reference/condition_bad.m4a   (short test sentence, the same one the AI
                                    will generate, recorded in the same
                                    physical condition)

The short reference sentence is always the same:
"This is a voice cloning test to evaluate how the quality of the
original recording affects the generated result."

## 7. Run the scripts, in this order
    python scripts/clone_voice.py
    python scripts/generate_speech.py
    python scripts/analyze.py

## 8. Check the results
The AI-generated audio and the spectrogram plots appear inside the
results/ folder.

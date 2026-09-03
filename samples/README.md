Put your recorded audio files here, one per condition.

Format: any of these is accepted, with no manual conversion needed: wav,
mp3, m4a, ogg, oga, flac. Record and save in whatever each app exports
natively (iPhone Voice Memos exports m4a, WhatsApp exports ogg, etc.).
The script automatically converts to MP3 before sending to the API,
because that is the format ElevenLabs recommends.

Suggested names (the filename, without extension, becomes the condition
name everywhere else in the project):

- phone_home_open.m4a
- phone_home_closed.m4a
- whatsapp_home_closed.ogg
- phone_studio.m4a
- studio_clean.wav
- studio_noise.wav
- studio_96_32.wav

Rules:
- The SAME sentence (long paragraph) spoken in every recording
- You can have as many conditions as you want; the scripts adapt
  automatically to whatever files are in this folder

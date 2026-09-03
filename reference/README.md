Put the recording of the short TEST SENTENCE here (the same one
generate_speech.py asks the AI to generate), one per condition, with the
SAME filename (without extension) used in samples/.

Format: any of these is accepted, no manual conversion: wav, mp3, m4a,
ogg, oga, flac. The extension can differ from the one used in samples/
for the same condition; what matters is that the filename (without
extension) is identical.

Exact sentence to record in each condition:
"This is a voice cloning test to evaluate how the quality of the
original recording affects the generated result."

Example: if samples/ has phone_home_open.m4a (the long paragraph used
for cloning), then reference/ must contain phone_home_open.m4a or
phone_home_open.wav (any accepted format), holding only that short
sentence recorded in the same physical condition.

This exists for a fair comparison: analyze.py compares this file
(original, short sentence) with the audio the AI generated (same short
sentence), instead of comparing against the long cloning paragraph,
which has different text and would invalidate the comparison.

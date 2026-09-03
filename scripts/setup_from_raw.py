"""
Goal: take the original files (with the naming convention already used
in your own workflow, inside raw/) and organize them into samples/ and
reference/ with the canonical names the rest of the pipeline expects,
without renaming the originals by hand.

Put the 14 files (7 conditions x clone + reference) inside the raw/
folder at the project root, keeping their original names, and run this
script once. It copies (does not move) the files, so raw/ stays intact
as a backup.
"""

import re
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw"
SAMPLES_DIR = BASE_DIR / "samples"
REFERENCE_DIR = BASE_DIR / "reference"

SAMPLES_DIR.mkdir(exist_ok=True)
REFERENCE_DIR.mkdir(exist_ok=True)

# Maps the suffix of your original filename to the canonical condition
# name used across the rest of the project. Adjust here if a suffix does
# not match exactly what you recorded.
SUFFIX_TO_CONDITION = {
    "studio__416__treated": "studio_clean",
    "studio__416__leaks": "studio_noise",
    "studio__416__treated__96.32": "studio_96_32",
    "studio__iphone__treated": "phone_studio",
    "livingroom__iphone__closed-window": "phone_home_closed",
    "livingroom__iphone+wpp__closed-window__wpp": "whatsapp_home_closed",
    "livingroom__iphone__open-window": "phone_home_open",
}


def parse_filename(path: Path):
    # Strip a numeric prefix like "1 - "
    name = re.sub(r"^\d+\s*-\s*", "", path.stem)
    if name.startswith("clone__"):
        kind = "samples"
        suffix = name[len("clone__"):]
    elif name.startswith("reference__"):
        kind = "reference"
        suffix = name[len("reference__"):]
    else:
        return None
    return kind, suffix


def main():
    if not RAW_DIR.exists():
        raise SystemExit(
            "raw/ folder not found. Create raw/ at the project root and "
            "put the 14 original files inside it."
        )

    files = [f for f in RAW_DIR.iterdir() if f.is_file()]
    if not files:
        raise SystemExit("raw/ is empty. Put the original files in there.")

    matched = 0
    for path in files:
        parsed = parse_filename(path)
        if not parsed:
            print(f"Warning: unrecognized pattern in {path.name}, skipping.")
            continue
        kind, suffix = parsed
        condition_name = SUFFIX_TO_CONDITION.get(suffix)
        if not condition_name:
            print(f"Warning: suffix '{suffix}' not in the mapping, skipping {path.name}.")
            continue

        dest_dir = SAMPLES_DIR if kind == "samples" else REFERENCE_DIR
        dest_path = dest_dir / f"{condition_name}{path.suffix}"
        shutil.copy2(path, dest_path)
        print(f"{path.name} -> {dest_path.relative_to(BASE_DIR)}")
        matched += 1

    print(f"\n{matched} file(s) organized.")


if __name__ == "__main__":
    main()

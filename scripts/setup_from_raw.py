"""
Objetivo: pegar os arquivos originais (com a nomenclatura que você já
usa no seu fluxo de trabalho, dentro de raw/) e organizá-los em
samples/ e reference/ com os nomes canônicos que o resto do pipeline
espera, sem precisar renomear os arquivos originais na mão.

Coloque os 14 arquivos (7 condições x clone + reference) dentro da
pasta raw/ na raiz do projeto, mantendo os nomes originais, e rode
este script uma vez. Ele copia (não move) os arquivos, então raw/
continua intacta como backup.
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

# Mapeamento do sufixo do seu nome de arquivo original para o nome
# canônico da condição usado no resto do projeto. Ajuste aqui se
# algum sufixo não bater exatamente com o que você gravou.
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
    # Remove prefixo numérico tipo "1 - "
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
            "Pasta raw/ não encontrada. Crie raw/ na raiz do projeto e "
            "coloque os 14 arquivos originais lá dentro."
        )

    files = [f for f in RAW_DIR.iterdir() if f.is_file()]
    if not files:
        raise SystemExit("raw/ está vazia. Coloque os arquivos originais lá.")

    matched = 0
    for path in files:
        parsed = parse_filename(path)
        if not parsed:
            print(f"Aviso: não reconheci o padrão em {path.name}, pulando.")
            continue
        kind, suffix = parsed
        condition_name = SUFFIX_TO_CONDITION.get(suffix)
        if not condition_name:
            print(f"Aviso: sufixo '{suffix}' não está no mapeamento, pulando {path.name}.")
            continue

        dest_dir = SAMPLES_DIR if kind == "samples" else REFERENCE_DIR
        dest_path = dest_dir / f"{condition_name}{path.suffix}"
        shutil.copy2(path, dest_path)
        print(f"{path.name} -> {dest_path.relative_to(BASE_DIR)}")
        matched += 1

    print(f"\n{matched} arquivo(s) organizados.")


if __name__ == "__main__":
    main()

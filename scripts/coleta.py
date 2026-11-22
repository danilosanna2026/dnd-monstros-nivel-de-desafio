# Baixa a lista de monstros do SRD 5e (mesmo conteúdo que a dnd5eapi.co serve).
# Uso: python scripts/coleta.py
import json
import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/5e-bits/5e-database/main/src/2014/en/5e-SRD-Monsters.json"
DESTINO = Path("data/raw/monstros.json")

DESTINO.parent.mkdir(parents=True, exist_ok=True)
with urllib.request.urlopen(URL, timeout=60) as resposta:
    monstros = json.load(resposta)

DESTINO.write_text(json.dumps(monstros, ensure_ascii=False), encoding="utf-8")
print(f"{len(monstros)} monstros salvos em {DESTINO}")

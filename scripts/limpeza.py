# Transforma o JSON dos monstros em uma tabela plana (data/processed/monstros.csv).
# As decisões estão em docs/03-limpeza.md.
# Uso: python scripts/limpeza.py
import json
import re
from pathlib import Path

import pandas as pd

bruto = json.loads(Path("data/raw/monstros.json").read_text(encoding="utf-8"))
df = pd.json_normalize(bruto)


def pes(texto):
    # "30 ft." vira 30; velocidade que não existe vira 0
    if isinstance(texto, str):
        return float(re.match(r"\s*(\d+)", texto).group(1))
    return 0.0


tabela = pd.DataFrame(
    {
        "nome": df["name"],
        "tamanho": df["size"],
        # "swarm of Tiny beasts" vira só "swarm"
        "tipo": df["type"].replace({"swarm of Tiny beasts": "swarm"}),
        "nd": df["challenge_rating"],
        "xp": df["xp"],
        "pv": df["hit_points"],
        # alguns monstros têm duas CAs (ex.: com e sem armadura); fico com a primeira
        "ca": df["armor_class"].apply(lambda lista: lista[0]["value"]),
        "forca": df["strength"],
        "destreza": df["dexterity"],
        "constituicao": df["constitution"],
        "inteligencia": df["intelligence"],
        "sabedoria": df["wisdom"],
        "carisma": df["charisma"],
        "vel_andar": df["speed.walk"].apply(pes),
        "vel_voar": df["speed.fly"].apply(pes),
        "vel_nadar": df["speed.swim"].apply(pes),
        "lendario": df["legendary_actions"].apply(lambda x: isinstance(x, list) and len(x) > 0),
    }
)

Path("data/processed").mkdir(parents=True, exist_ok=True)
tabela.to_csv("data/processed/monstros.csv", index=False)
print(f"{len(tabela)} monstros, {tabela.shape[1]} colunas")

# Responde as perguntas do docs/02 e gera os gráficos em graficos/.
# Uso: python scripts/analise.py   (precisa de pandas, scipy e matplotlib)
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/processed/monstros.csv")
Path("graficos").mkdir(exist_ok=True)
AZUL = "#118DFF"
CINZA = "#9AA5B1"

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
    }
)

# P1: PV e CA acompanham o ND?
corr = df[["nd", "pv", "ca"]].corr(method="spearman")
print("Correlação de Spearman com o ND: PV =", round(corr.loc["nd", "pv"], 2), "| CA =", round(corr.loc["nd", "ca"], 2))
por_nd = df.groupby("nd").agg(pv=("pv", "median"), ca=("ca", "median"), n=("nome", "count"))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
ax1.scatter(df["nd"], df["pv"], s=18, color=CINZA, alpha=0.7, label="cada monstro")
ax1.plot(por_nd.index, por_nd["pv"], color=AZUL, lw=2.5, label="mediana por ND")
ax1.set_yscale("log")
ax1.set_xlabel("Nível de desafio (ND)")
ax1.set_ylabel("Pontos de vida (escala log)")
ax1.set_title("Pontos de vida crescem junto com o ND")
ax1.legend(frameon=False)
ax2.scatter(df["nd"], df["ca"], s=18, color=CINZA, alpha=0.7)
ax2.plot(por_nd.index, por_nd["ca"], color=AZUL, lw=2.5)
ax2.set_xlabel("Nível de desafio (ND)")
ax2.set_ylabel("Classe de armadura (CA)")
ax2.set_title("A CA sobe, mas bem mais devagar")
fig.tight_layout()
fig.savefig("graficos/01_pv_e_ca_por_nd.png", dpi=130)
plt.close(fig)

# P2: quem foge do PV típico do ND?
df["pv_tipico"] = df.groupby("nd")["pv"].transform("median")
df["n_do_nd"] = df.groupby("nd")["nome"].transform("count")
df["razao_pv"] = df["pv"] / df["pv_tipico"]
base = df[(df["n_do_nd"] >= 5) & (df["nd"] >= 1)].sort_values("razao_pv")
colunas = ["nome", "nd", "pv", "pv_tipico", "razao_pv"]
print("\nPV bem abaixo do típico do ND:\n", base.head(5)[colunas].round(2).to_string(index=False))
print("\nPV bem acima do típico do ND:\n", base.tail(5)[colunas].round(2).to_string(index=False))

# P3: ND por tipo de criatura
por_tipo = df.groupby("tipo")["nd"].agg(quantidade="count", nd_mediano="median", nd_maximo="max")
por_tipo = por_tipo.sort_values("nd_mediano")
print("\nND por tipo:\n", por_tipo.sort_values("nd_mediano", ascending=False).to_string())

fig, ax = plt.subplots(figsize=(9, 6))
cores = [AZUL if t in ("dragon", "fiend") else CINZA for t in por_tipo.index]
ax.barh(por_tipo.index, por_tipo["nd_mediano"], color=cores)
for i, (tipo, linha) in enumerate(por_tipo.iterrows()):
    ax.text(linha["nd_mediano"] + 0.15, i, f"{linha['nd_mediano']:g}  (n={int(linha['quantidade'])})", va="center", fontsize=9)
ax.set_xlabel("ND mediano")
ax.set_title("Dragões e demônios têm os maiores ND medianos")
fig.tight_layout()
fig.savefig("graficos/02_nd_por_tipo.png", dpi=130)
plt.close(fig)

# P4: lendários têm ND mais alto?
lend = df.groupby("lendario")["nd"].agg(quantidade="count", minimo="min", mediano="median", maximo="max")
print("\nLendários:\n", lend.to_string())

# P5: o XP é função do ND?
xp_comum = df.groupby("nd")["xp"].agg(lambda s: s.mode().iloc[0])
df["xp_comum"] = df["nd"].map(xp_comum)
fora = df[df["xp"] != df["xp_comum"]][["nome", "nd", "xp", "xp_comum"]]
print(f"\nXP diferente do valor mais comum do ND: {len(fora)} monstros\n", fora.to_string(index=False))

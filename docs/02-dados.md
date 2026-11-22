# 02 · Dados

**Fonte:** lista de monstros do SRD 5e (edição 2014, em inglês), do repositório [5e-bits/5e-database](https://github.com/5e-bits/5e-database), arquivo `src/2014/en/5e-SRD-Monsters.json`. É o mesmo conteúdo que a API pública dnd5eapi.co serve. Licença do repositório: MIT. O conteúdo do SRD é de uso livre (Wizards of the Coast, licença aberta).

**Por que o repositório e não a API:** o arquivo vem completo em uma única requisição, é mais simples de reproduzir e não depende de paginação.

**Tamanho:** 334 monstros, 44 colunas depois de achatar o JSON.

**Campos usados**

| Campo original | Uso |
|---|---|
| `challenge_rating` | nível de desafio (ND), de 0 a 30 |
| `hit_points` | pontos de vida (PV) |
| `armor_class` | classe de armadura (CA), vem como lista |
| `xp` | experiência dada ao derrotar |
| `type`, `size` | tipo e tamanho |
| `speed.*` | velocidades (andar, voar, nadar) |
| `legendary_actions` | indica se o monstro é lendário |
| `strength` ... `charisma` | atributos |

**Como baixar:** `python scripts/coleta.py` (salva em `data/raw/monstros.json`). Os dados brutos não ficam no repositório.

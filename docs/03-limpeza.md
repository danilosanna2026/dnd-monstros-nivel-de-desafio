# 03 · Limpeza

Script: `scripts/limpeza.py`. Entrada: `data/raw/monstros.json`. Saída: `data/processed/monstros.csv` (334 linhas, 17 colunas).

## O que eu olhei antes
- Nenhum monstro repetido (nome único) e nenhum PV, ND ou XP vazio.
- Campos opcionais vazios são normais: só 32 monstros têm ações lendárias, e quem não voa não tem `speed.fly`.

## Decisões
| Problema | Decisão |
|---|---|
| JSON aninhado (`speed`, `armor_class`) | `pandas.json_normalize` e colunas novas |
| `armor_class` é uma lista; 7 monstros têm duas CAs | fico com a primeira |
| Velocidades são texto (`"30 ft."`) | extraio o número; sem velocidade vira 0 |
| `legendary_actions` é lista ou vazio | coluna `lendario` verdadeiro/falso |
| Tipo `swarm of Tiny beasts` | encurtado para `swarm` |
| Nomes das colunas em inglês | renomeadas para português |

## Limite conhecido
Escolher só a primeira CA ignora a variação de monstros com armadura opcional. Para a pergunta (tendência por ND) o efeito é pequeno, mas é uma simplificação.

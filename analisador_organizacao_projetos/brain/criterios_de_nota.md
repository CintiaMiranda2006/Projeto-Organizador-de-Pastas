# Critérios de Nota

## Escala

A nota final é calculada de `0` a `10`, com uma casa decimal.

## Tabela de pontuação

| Critério | Pontuação máxima | Módulo responsável |
|---|---:|---|
| Organização de pastas | 2 pontos | `score.py` |
| Ausência de arquivos soltos | 2 pontos | `score.py` + `loose_file_checker.py` |
| Ausência de arquivos vazios | 1 ponto | `score.py` + `empty_checker.py` |
| Ausência de pastas vazias | 1 ponto | `score.py` + `empty_checker.py` |
| Padrão de nomes | 2 pontos | `score.py` + `naming_checker.py` |
| Uso correto de timestamp | 1 ponto | `score.py` + `timestamp_checker.py` |
| Coerência entre ordem e timestamp | 1 ponto | `score.py` + `order_checker.py` |
| **Total** | **10 pontos** | |

## Como cada critério é calculado

### 1. Organização de pastas (máx 2)

Avalia a proporção de arquivos que estão organizados em subpastas.

- Se não existir nenhuma subpasta: **0 pontos**.
- Se existirem subpastas: a nota é reduzida proporcionalmente à quantidade de arquivos soltos.
- Fórmula: `2.0 × (1 - proporção_de_arquivos_soltos)`

### 2. Ausência de arquivos soltos (máx 2)

Avalia quantos arquivos estão diretamente na raiz da pasta analisada.

- Fórmula: `2.0 × (1 - proporção_de_arquivos_soltos)`

### 3. Ausência de arquivos vazios (máx 1)

Avalia quantos arquivos têm tamanho zero.

- Fórmula: `1.0 × (1 - proporção_de_arquivos_vazios)`

### 4. Ausência de pastas vazias (máx 1)

Avalia quantas pastas não contêm nenhum arquivo (recursivo).

- Fórmula: `1.0 × (1 - proporção_de_pastas_vazias)`

### 5. Padrão de nomes (máx 2)

Avalia quantos arquivos têm problemas de nome:
- Fora do padrão `ordem_tipo_assunto_aammdd_hhmm`.
- Nome genérico (`teste`, `novo`, `final`, etc.).
- Separador diferente do dominante no projeto.

- Fórmula: `2.0 × (1 - proporção_de_arquivos_com_problema_de_nome)`

### 6. Uso correto de timestamp (máx 1)

Avalia quantos arquivos não têm timestamp ou têm timestamp inválido.

- Fórmula: `1.0 × (1 - proporção_de_arquivos_com_problema_de_timestamp)`

### 7. Coerência entre ordem e timestamp (máx 1)

Avalia se a sequência de letras (`a`, `b`, `c`) corresponde à ordem cronológica dos timestamps dentro de cada pasta.

- Se não há arquivos com letra de ordem: **1 ponto** (critério não aplicável).
- Fórmula: `1.0 × (1 - proporção_de_arquivos_com_ordem_incoerente)`

## Interpretação da nota

| Nota | Classificação |
|---|---|
| 9.0 a 10.0 | Excelente — projeto bem organizado |
| 7.0 a 8.9 | Bom — pequenos problemas a corrigir |
| 5.0 a 6.9 | Regular — organização pode melhorar |
| 0.0 a 4.9 | Crítico — projeto com sérios problemas de organização |

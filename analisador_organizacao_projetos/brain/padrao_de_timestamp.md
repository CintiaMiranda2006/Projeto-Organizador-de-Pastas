# Padrão de Timestamp

## Formato obrigatório

```
AAMMDD_HHMM
```

O timestamp deve aparecer **ao final do nome do arquivo**, logo antes da extensão.

## Exemplo completo

```
c_requisitos_autenticacao_260622_1850.md
                          ^^^^^^^_^^^^
                          AAMMDD   HHMM
```

## Decomposição do timestamp

| Parte | Significado | Dígitos | Exemplo |
|---|---|---|---|
| `AA` | Ano (2 dígitos) | 2 | `26` = 2026 |
| `MM` | Mês | 2 | `06` = junho |
| `DD` | Dia | 2 | `22` = dia 22 |
| `_` | Separador obrigatório entre data e horário | — | `_` |
| `HH` | Hora (formato 24h) | 2 | `18` = 18h |
| `MM` | Minuto | 2 | `50` = 50 min |

## Exemplo de leitura

```
260622_1850
```

Leitura: **22 de junho de 2026, às 18:50**.

## Regras de validação

O analisador verifica os seguintes critérios:

| Critério | Regra |
|---|---|
| Mês | Entre `01` e `12` |
| Dia | Entre `01` e `31` |
| Hora | Entre `00` e `23` |
| Minuto | Entre `00` e `59` |
| Posição | Deve estar ao final do nome, antes da extensão |
| Formato | 6 dígitos para data + `_` + 4 dígitos para hora |

## Exemplos válidos

```
260101_0000   → 1º de janeiro de 2026, meia-noite
260622_1850   → 22 de junho de 2026, 18:50
261231_2359   → 31 de dezembro de 2026, 23:59
```

## Exemplos inválidos

```
260622        → sem horário
991399_2500   → mês 13 e hora 25 são inválidos
260622_18     → horário incompleto (só 2 dígitos)
_260622_1850  → timestamp no início, não no final
```

## Por que o timestamp é importante?

O timestamp permite:

- Rastrear quando cada arquivo foi criado.
- Verificar se a ordem cronológica (`a`, `b`, `c`) é coerente com a data real.
- Identificar arquivos desatualizados ou fora de sequência.

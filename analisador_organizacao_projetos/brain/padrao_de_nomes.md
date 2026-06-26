# Padrão de Nomes de Arquivos

## Formato obrigatório

```
ordem_tipo_assunto_aammdd_hhmm.extensao
```

## Exemplo

```
a_prd_login_260522_1150.md
b_requisitos_cadastro_260523_1850.md
c_ata_reuniao_260622_1400.txt
```

## Componentes do nome

| Componente | Descrição | Exemplo |
|---|---|---|
| `ordem` | Letra minúscula que indica a posição cronológica do arquivo | `a`, `b`, `c` |
| `tipo` | Categoria ou tipo do documento | `prd`, `requisitos`, `ata`, `documentacao` |
| `assunto` | Tema ou contexto do arquivo | `login`, `cadastro`, `autenticacao` |
| `aammdd` | Data no formato ano-mês-dia de dois dígitos cada | `260622` = 22/06/2026 |
| `hhmm` | Horário no formato hora-minuto | `1850` = 18:50 |
| `extensao` | Extensão do arquivo | `.md`, `.txt`, `.docx` |

## Separadores

| Separador | Válido? | Observação |
|---|---|---|
| `_` (underscore) | Sim | Padrão recomendado |
| `-` (hífen) | Sim | Válido se usado de forma consistente no projeto inteiro |
| ` ` (espaço) | Não | Nunca deve ser usado |
| Mistura de `_` e `-` | Não | Penalizado como inconsistência |

## Regra de ordem

A letra de ordem deve refletir a sequência cronológica real dos arquivos.

- `a` representa o arquivo mais antigo.
- `b` deve ter timestamp posterior ao de `a`.
- `c` deve ter timestamp posterior ao de `b`.

Exemplos **corretos**:

```
a_prd_login_260522_1150.md      → mais antigo
b_prd_cadastro_260523_1850.md   → gerado depois
c_requisitos_auth_260622_1400.md → o mais recente
```

Exemplo com **problema**:

```
a_prd_login_260523_1150.md      → timestamp mais recente
b_prd_cadastro_260522_1850.md   → timestamp mais antigo — ERRO
```

Nesse caso, a letra `b` deveria ser anterior à `a`, mas o timestamp diz o contrário. O analisador aponta essa inconsistência.

## Nomes genéricos (proibidos)

Os seguintes nomes são considerados inválidos por serem pouco descritivos:

```
teste, test, novo, new, final, final2, documento, doc,
arquivo, file, temp, tmp, copia, copy, versao_final,
untitled, semtitulo, rascunho, draft, backup, bkp
```

# Regras de Organização

Este documento descreve o que o Analisador de Organização de Projetos verifica em cada análise.

---

## O que o analisador verifica

### 1. Arquivos soltos

**Definição:** arquivos localizados diretamente na raiz da pasta analisada.

**Critério:** se existem subpastas no projeto, qualquer arquivo diretamente na raiz é considerado solto (deveria estar organizado em uma subpasta).

**Exemplo de problema:**

```
meu_projeto/
  contrato.md        ← arquivo solto
  prd.md             ← arquivo solto
  docs/
    requisitos.md
```

**Sugestão:** mover os arquivos soltos para subpastas organizadas por tema ou tipo.

---

### 2. Arquivos vazios

**Definição:** arquivos com tamanho igual a zero bytes.

**Motivo:** arquivos vazios podem indicar documentos criados mas nunca preenchidos, arquivos temporários esquecidos ou falhas no processo de geração.

**Exemplo de problema:**

```
docs/
  a_prd_login_260622_1400.md        ← 0 bytes — arquivo vazio
  b_requisitos_auth_260622_1430.md  ← 2.4 KB — OK
```

**Sugestão:** remover os arquivos vazios ou preenchê-los com conteúdo relevante.

---

### 3. Pastas vazias

**Definição:** diretórios que não contêm nenhum arquivo, nem mesmo em subpastas (verificação recursiva).

**Motivo:** pastas vazias geralmente indicam estrutura criada mas não utilizada.

**Exemplo de problema:**

```
meu_projeto/
  docs/
    a_prd_login.md
  contratos/         ← pasta vazia
  rascunhos/         ← pasta vazia
```

**Sugestão:** remover as pastas vazias ou adicionar conteúdo relevante a elas.

---

### 4. Nomes fora do padrão

**Definição:** arquivos cujos nomes não seguem o padrão `ordem_tipo_assunto_aammdd_hhmm.extensao`.

**Problemas identificados:**

- Nome não segue a estrutura esperada.
- Nome genérico (`teste`, `novo`, `final`, `documento`, etc.).
- Mistura de separadores (`_` e `-` no mesmo projeto).

**Exemplos de nomes problemáticos:**

```
teste.md
novo_documento.docx
final_versao.md
b-prd-login.md       ← hífen num projeto que usa underscore
```

**Exemplos de nomes válidos:**

```
a_prd_login_260622_1400.md
b_requisitos_auth_260623_0900.md
```

**Sugestão:** renomear os arquivos seguindo o padrão definido em `padrao_de_nomes.md`.

---

### 5. Timestamp inválido ou ausente

**Definição:** arquivos sem o timestamp `AAMMDD_HHMM` no nome, ou com valores fora dos limites válidos.

**Verificações realizadas:**

| Verificação | Detalhe |
|---|---|
| Ausência de timestamp | O arquivo não contém o padrão `DDDDDD_DDDD` |
| Mês inválido | Valor fora do intervalo `01`–`12` |
| Dia inválido | Valor fora do intervalo `01`–`31` |
| Hora inválida | Valor fora do intervalo `00`–`23` |
| Minuto inválido | Valor fora do intervalo `00`–`59` |
| Posição incorreta | Timestamp não está no final do nome (antes da extensão) |

**Exemplo de timestamp inválido:**

```
a_prd_login_261399_2500.md  → mês 13 e hora 25 são inválidos
a_prd_login_260622.md       → sem horário, apenas data
```

**Sugestão:** adicionar ou corrigir o timestamp seguindo o formato em `padrao_de_timestamp.md`.

---

### 6. Ordem incoerente com o timestamp

**Definição:** a letra de ordem do arquivo (`a`, `b`, `c`) não corresponde à sequência cronológica indicada pelos timestamps, dentro de uma mesma pasta.

**Regra:** arquivos com letras menores devem ter timestamps mais antigos.

**Exemplo de problema:**

```
a_prd_login_260523_1150.md      → timestamp: 260523_1150 (mais recente)
b_prd_cadastro_260522_1850.md   → timestamp: 260522_1850 (mais antigo)
```

Nesse caso, `b` tem data mais antiga que `a`, o que contradiz a ordem alfabética esperada.

**Sugestão:** corrigir a letra de ordem dos arquivos para que reflita a sequência cronológica real, do mais antigo para o mais recente.

---

## O que o analisador NÃO verifica

O analisador não avalia:

- Qualidade do código-fonte.
- Cobertura de testes.
- Configuração de Docker.
- Deploy ou infraestrutura.
- Performance da aplicação.
- Segurança do código.
- Arquitetura interna da aplicação.

Esses aspectos estão fora do escopo porque a ferramenta deve funcionar também em projetos que não são de código, como projetos de documentação, PRDs e planejamento.

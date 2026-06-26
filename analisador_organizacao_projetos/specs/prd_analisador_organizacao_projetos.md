# PRD — Analisador de Organização de Projetos

## 1. Visão geral

O **Analisador de Organização de Projetos** é uma ferramenta para avaliar automaticamente a organização estrutural de uma pasta de projeto.

O sistema deve analisar arquivos e diretórios, identificar problemas de organização e gerar um relatório com nota, inconsistências encontradas e sugestões de melhoria.

A ferramenta não é limitada a repositórios de código. Ela deve funcionar também para pastas compostas por documentos, PRDs, especificações, relatórios, arquivos Markdown, planilhas, JSONs, imagens ou outros materiais usados em um projeto digital.

---

## 2. Problema

Projetos digitais frequentemente acumulam arquivos desorganizados, nomes inconsistentes, documentos vazios, pastas sem uso e versões difíceis de rastrear.

Isso dificulta:

- Encontrar arquivos importantes.
- Entender a ordem dos documentos.
- Saber qual arquivo é mais recente.
- Manter um padrão entre entregas.
- Evitar duplicidade ou arquivos esquecidos.
- Avaliar a qualidade da organização do projeto.

A ferramenta resolve esse problema analisando a estrutura do projeto e apontando automaticamente os pontos de desorganização.

---

## 3. Objetivo

Criar uma ferramenta capaz de:

- Ler uma pasta de projeto.
- Mapear arquivos e subpastas.
- Verificar arquivos soltos.
- Verificar arquivos vazios.
- Verificar pastas vazias.
- Validar padrão de nomes.
- Validar timestamp no nome dos arquivos.
- Validar ordem cronológica dos arquivos.
- Gerar uma nota geral de organização.
- Gerar um relatório final em Markdown e/ou JSON.
- Sugerir melhorias práticas para organização do projeto.

---

## 4. Escopo

### 4.1 Dentro do escopo

O sistema deve analisar:

- Estrutura de pastas.
- Arquivos na raiz.
- Arquivos dentro das pastas.
- Arquivos vazios.
- Pastas vazias.
- Nomes fora do padrão.
- Uso de separadores no nome.
- Uso de timestamp.
- Coerência entre ordem alfabética e timestamp.
- Tipos de arquivos existentes.
- Possíveis arquivos duplicados ou parecidos.
- Nomes genéricos ou pouco descritivos.

### 4.2 Fora do escopo

O sistema não deve avaliar:

- Qualidade do código.
- Cobertura de testes.
- Existência de testes.
- Docker.
- Banco de dados.
- Deploy.
- Performance da aplicação.
- Segurança de código.
- Arquitetura interna da aplicação.

Esses pontos ficam fora do escopo porque a ferramenta deve funcionar também em projetos que não são de código, como projetos compostos apenas por PRDs, documentação ou arquivos de planejamento.

---

## 5. Padrão principal de nomes

O sistema terá um padrão recomendado para nomear arquivos.

Formato principal:

```text
ordem_tipo_assunto_aammdd_hhmm.extensao
```

Exemplo:

```text
a_prd_login_260522_1150.md
b_prd_cadastro_260523_1850.md
c_requisitos_autenticacao_260622_1850.md
```

Nesse padrão:

- `a`, `b`, `c` indicam a ordem dos arquivos.
- `a` representa o arquivo mais antigo.
- `b` representa o arquivo gerado depois do `a`.
- `c` representa o arquivo mais recente entre esses exemplos.
- `prd`, `requisitos`, `ata`, `documentacao` indicam o tipo do arquivo.
- `login`, `cadastro`, `autenticacao` indicam o assunto.
- `260622` representa a data no formato `AAMMDD`.
- `1850` representa o horário no formato `HHMM`.
- `.md` representa a extensão do arquivo.

---

## 6. Regra de ordem

A primeira parte do nome indica a ordem do arquivo dentro de uma sequência.

Exemplo correto:

```text
a_prd_login_260522_1150.md
b_prd_cadastro_260523_1850.md
c_requisitos_autenticacao_260622_1850.md
```

Interpretação:

- `a` é o arquivo mais antigo.
- `b` foi gerado depois de `a`.
- `c` é o arquivo mais recente.

O sistema deve verificar se a letra de ordem está coerente com o timestamp.

Exemplo com problema:

```text
a_prd_login_260523_1150.md
b_prd_cadastro_260522_1850.md
```

Nesse caso, o arquivo `b` aparece como posterior ao `a`, mas possui timestamp mais antigo. O sistema deve apontar essa inconsistência no relatório.

---

## 7. Regra de timestamp

O timestamp deve ficar no final do nome do arquivo, antes da extensão.

Formato:

```text
AAMMDD_HHMM
```

Exemplo:

```text
260622_1850
```

Interpretação:

- `26` = ano 2026.
- `06` = mês junho.
- `22` = dia 22.
- `18` = hora.
- `50` = minuto.

Nome completo:

```text
c_requisitos_autenticacao_260622_1850.md
```

O sistema deve validar:

- Se o timestamp existe.
- Se a data possui 6 dígitos.
- Se o horário possui 4 dígitos.
- Se o mês está entre `01` e `12`.
- Se o dia está entre `01` e `31`.
- Se a hora está entre `00` e `23`.
- Se o minuto está entre `00` e `59`.
- Se o timestamp está no final do nome, antes da extensão.
- Se os arquivos da mesma pasta seguem o mesmo padrão.

---

## 8. Regra de separadores

O padrão principal deve usar `_` para separar as palavras.

Exemplo correto:

```text
a_prd_login_260523_1150.md
```

O uso de `-` pode ser aceito quando o projeto inteiro seguir esse padrão de forma consistente.

Exemplo aceitável, caso o projeto adote hífen:

```text
a-prd-login-260523-1150.md
```

O sistema deve penalizar misturas sem padrão.

Exemplo ruim:

```text
a_prd_login_260523_1150.md
b-prd-cadastro-260523-1850.md
c requisitos autenticacao 260622 1850.md
```

Problemas:

- Mistura `_`, `-` e espaços.
- Falta consistência.
- Dificulta automação e leitura.

---

## 9. Nomes genéricos

O sistema deve identificar nomes pouco descritivos.

Exemplos de nomes problemáticos:

```text
teste.md
novo.md
final.docx
final2.docx
documento.md
arquivo.txt
versao_final_agora.md
```

Esses nomes devem ser marcados como problemas porque não indicam claramente o tipo, o assunto ou a ordem do arquivo.

---

## 10. Arquivos soltos

O sistema deve identificar arquivos soltos na raiz do projeto ou em locais incoerentes.

Exemplo de estrutura problemática:

```text
meu_projeto/
  contrato_final_260523_1100.md
  prd_login_260523_1150.md
  anotacoes_260523_1200.txt
  documentacao/
  requisitos/
```

Possível sugestão:

```text
meu_projeto/
  contratos/
    a_contrato_final_260523_1100.md

  prds/
    a_prd_login_260523_1150.md

  anotacoes/
    a_anotacoes_260523_1200.txt
```

A ferramenta não deve obrigar uma única estrutura, mas deve identificar sinais de desorganização.

---

## 11. Arquivos vazios

O sistema deve identificar arquivos com tamanho zero ou praticamente sem conteúdo.

Exemplos:

```text
a_prd_login_260523_1150.md
b_requisitos_cadastro_260523_1300.md
c_ata_reuniao_260523_1400.md
```

Se esses arquivos estiverem vazios, o relatório deve apontar o problema.

Arquivos vazios podem indicar:

- Documento criado e esquecido.
- Documento incompleto.
- Arquivo temporário.
- Falha no processo de geração.
- Organização artificial sem conteúdo real.

---

## 12. Pastas vazias

O sistema deve identificar pastas sem arquivos.

Exemplo:

```text
projeto/
  documentos/
  contratos/
  requisitos/
    a_prd_login_260523_1150.md
```

Nesse caso, `documentos/` e `contratos/` estão vazias.

Pastas vazias não são sempre erros graves, mas devem aparecer no relatório para revisão.

---

## 13. Tipos de arquivo

O sistema deve mapear os tipos de arquivos encontrados.

Exemplos:

```text
.md
.txt
.docx
.pdf
.json
.csv
.xlsx
.png
.js
.java
.py
```

Esse mapeamento ajuda a identificar misturas incoerentes dentro de pastas.

Exemplo de possível problema:

```text
documentacao/
  a_prd_login_260523_1150.md
  b_script_validacao_260523_1300.js
  c_imagem_fluxo_260523_1400.png
  d_contrato_cliente_260523_1500.docx
```

Nesse caso, o sistema pode sugerir separar arquivos por finalidade ou tipo.

---

## 14. Critérios de pontuação

A nota final deve ser de `0` a `10`.

Critérios sugeridos:

| Critério | Pontuação |
|---|---:|
| Organização de pastas | 2 pontos |
| Ausência de arquivos soltos | 2 pontos |
| Ausência de arquivos vazios | 1 ponto |
| Ausência de pastas vazias | 1 ponto |
| Padrão de nomes | 2 pontos |
| Uso correto de timestamp | 1 ponto |
| Coerência entre ordem e timestamp | 1 ponto |

Total: `10 pontos`.

---

## 15. Saída esperada

O sistema deve gerar um relatório com:

- Nome da pasta analisada.
- Data da análise.
- Nota geral.
- Quantidade de arquivos analisados.
- Quantidade de pastas analisadas.
- Lista de arquivos soltos.
- Lista de arquivos vazios.
- Lista de pastas vazias.
- Lista de arquivos fora do padrão de nome.
- Lista de arquivos sem timestamp.
- Lista de arquivos com timestamp inválido.
- Lista de arquivos com ordem incoerente.
- Pontos positivos.
- Sugestões de melhoria.

---

## 16. Exemplo de saída no terminal

```text
Projeto analisado: projeto_baguncado

Nota final: 5.0/10

Problemas encontrados:
- 4 arquivos soltos na raiz.
- 2 arquivos vazios.
- 1 pasta vazia.
- 5 arquivos fora do padrão de nome.
- 3 arquivos sem timestamp.
- 1 arquivo com ordem incompatível com o timestamp.

Sugestões:
- Organizar arquivos soltos em pastas por tema.
- Remover ou preencher arquivos vazios.
- Remover pastas vazias sem uso.
- Renomear arquivos usando o padrão: ordem_tipo_assunto_aammdd_hhmm.extensao
- Corrigir a letra inicial dos arquivos conforme a ordem cronológica.
```

---

## 17. Exemplo de relatório Markdown

Arquivo gerado:

```text
reports/projeto_baguncado_relatorio.md
```

Conteúdo esperado:

```markdown
# Relatório de Organização

## Projeto analisado

projeto_baguncado

## Nota final

5.0/10

## Problemas encontrados

- Arquivos soltos na raiz.
- Arquivos vazios.
- Pastas vazias.
- Nomes fora do padrão.
- Timestamp ausente ou inválido.
- Ordem incompatível com data.

## Sugestões

- Mover arquivos para pastas específicas.
- Corrigir nomes dos arquivos.
- Padronizar separador com underline.
- Adicionar timestamp no formato AAMMDD_HHMM.
```

---

## 18. Estrutura técnica sugerida

Estrutura inicial do projeto:

```text
analisador_projetos/
  src/
    analyzer.py
    file_scanner.py
    naming_checker.py
    timestamp_checker.py
    order_checker.py
    empty_checker.py
    loose_file_checker.py
    score.py
    report.py

  brain/
    regras_de_organizacao.md
    criterios_de_nota.md
    padrao_de_nomes.md
    padrao_de_timestamp.md
    padrao_de_ordem.md
    decisoes_do_projeto.md

  specs/
    prd_analisador_organizacao.md

  samples/
    projeto_organizado/
    projeto_medio/
    projeto_baguncado/
    projeto_com_prds/

  reports/
    relatorio_exemplo.md

  README.md
  requirements.txt
```

---

## 19. Responsabilidade dos módulos

### `analyzer.py`

Arquivo principal. Recebe o caminho da pasta, chama os módulos de análise e coordena o fluxo.

### `file_scanner.py`

Percorre a estrutura do projeto e retorna arquivos, pastas, tamanhos, extensões e caminhos.

### `naming_checker.py`

Valida se os nomes dos arquivos seguem o padrão definido.

### `timestamp_checker.py`

Valida se o timestamp existe e se está em formato correto.

### `order_checker.py`

Verifica se a ordem `a`, `b`, `c` está coerente com o timestamp dos arquivos.

### `empty_checker.py`

Identifica arquivos vazios e pastas vazias.

### `loose_file_checker.py`

Identifica arquivos soltos na raiz ou em locais incoerentes.

### `score.py`

Calcula a nota final com base nos critérios definidos.

### `report.py`

Gera o relatório final em Markdown e/ou JSON.

---

## 20. Fluxo de funcionamento

Fluxo principal:

```text
Entrada da pasta
↓
Leitura dos arquivos e diretórios
↓
Validação de arquivos soltos
↓
Validação de arquivos vazios
↓
Validação de pastas vazias
↓
Validação de nomes
↓
Validação de timestamp
↓
Validação de ordem
↓
Cálculo da nota
↓
Geração do relatório
```

---

## 21. Exemplo de uso

Comando:

```bash
python src/analyzer.py ./samples/projeto_baguncado
```

Resultado esperado:

```text
Análise concluída.
Relatório gerado em: reports/projeto_baguncado_relatorio.md
Nota final: 5.0/10
```

---

## 22. Requisitos funcionais

### RF01 — Ler pasta de projeto

O sistema deve receber o caminho de uma pasta e analisar seu conteúdo.

### RF02 — Mapear arquivos e pastas

O sistema deve listar arquivos, pastas, extensões, tamanhos e caminhos.

### RF03 — Identificar arquivos soltos

O sistema deve identificar arquivos na raiz ou em locais incoerentes.

### RF04 — Identificar arquivos vazios

O sistema deve identificar arquivos com tamanho zero ou quase sem conteúdo.

### RF05 — Identificar pastas vazias

O sistema deve identificar diretórios sem arquivos.

### RF06 — Validar padrão de nomes

O sistema deve verificar se os nomes seguem o padrão definido.

### RF07 — Validar timestamp

O sistema deve verificar se os arquivos possuem timestamp no formato `AAMMDD_HHMM`.

### RF08 — Validar ordem cronológica

O sistema deve verificar se a letra inicial do arquivo está coerente com o timestamp.

### RF09 — Calcular nota

O sistema deve calcular uma nota final de `0` a `10`.

### RF10 — Gerar relatório

O sistema deve gerar relatório em Markdown e/ou JSON.

---

## 23. Requisitos não funcionais

### RNF01 — Simplicidade

O sistema deve ser simples de executar por terminal.

### RNF02 — Legibilidade

O código deve ser organizado em módulos pequenos e com responsabilidades claras.

### RNF03 — Compatibilidade

O sistema deve funcionar em projetos de código e em projetos documentais.

### RNF04 — Configurabilidade

O padrão de nomes e timestamp deve poder ser ajustado futuramente.

### RNF05 — Clareza do relatório

O relatório deve ser direto, legível e útil para tomada de decisão.

---

## 24. MVP

A primeira versão funcional deve conter:

- Leitura de pasta.
- Mapeamento de arquivos e diretórios.
- Identificação de arquivos soltos.
- Identificação de arquivos vazios.
- Identificação de pastas vazias.
- Validação do padrão de nomes.
- Validação do timestamp.
- Validação da ordem cronológica.
- Cálculo de nota.
- Relatório Markdown.

---

## 25. Melhorias futuras

Possíveis evoluções:

- Configuração personalizada de padrão de nomes.
- Correção automática de nomes.
- Sugestão automática de pastas.
- Detecção avançada de arquivos duplicados.
- Histórico de análises.
- Exportação em PDF.
- Interface web.
- Integração com GitHub.
- Comparação entre versões de organização.
- Modo específico para PRDs.
- Modo específico para documentação.
- Modo específico para projetos de código.

---

## 26. Próximo passo técnico

Com este PRD definido, o próximo passo é criar a estrutura inicial do repositório e implementar o MVP.

Ordem recomendada:

1. Criar a pasta do projeto.
2. Criar a estrutura `src/`, `specs/`, `brain/`, `samples/` e `reports/`.
3. Colocar este PRD dentro de `specs/`.
4. Criar arquivos de regras dentro de `brain/`.
5. Criar exemplos bons e ruins dentro de `samples/`.
6. Implementar o scanner de arquivos.
7. Implementar validadores de nome, timestamp, ordem, arquivos vazios e pastas vazias.
8. Implementar cálculo de nota.
9. Implementar geração de relatório.
10. Rodar o analisador nos exemplos da pasta `samples/`.

---

## 27. Resumo

O **Analisador de Organização de Projetos** é uma ferramenta para avaliar a organização de arquivos e pastas em projetos digitais.

Ele verifica se existem arquivos soltos, arquivos vazios, pastas vazias, nomes fora do padrão, timestamps inválidos e inconsistência entre ordem e data.

O padrão principal recomendado é:

```text
ordem_tipo_assunto_aammdd_hhmm.extensao
```

Exemplo:

```text
a_prd_login_260522_1150.md
b_prd_cadastro_260523_1850.md
c_requisitos_autenticacao_260622_1850.md
```

A saída principal será um relatório com nota, problemas encontrados e sugestões de melhoria.

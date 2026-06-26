# PRD — CRUD de Análises de Organização de Projetos

**Versão:** 1.0  
**Data:** 2026-06-24  
**Status:** Em definição  
**Relacionado a:** `prd_analisador_organizacao_projetos.md`

---

## 1. Contexto

O **Analisador de Organização de Projetos** já existe como ferramenta de linha de comando.

Ele recebe o caminho de uma pasta, verifica arquivos soltos, vazios, padrão de nomes, timestamps e coerência de ordem, calcula uma nota e gera um relatório em Markdown.

Este PRD define a evolução do projeto para um **sistema CRUD end-to-end**, onde o usuário poderá cadastrar, consultar, editar e excluir análises por meio de uma interface web, sem precisar usar o terminal.

---

## 2. Problema

O analisador atual funciona apenas no terminal. Isso cria as seguintes limitações:

- Não há histórico de análises realizadas.
- Cada análise precisa ser executada manualmente a cada vez.
- Os relatórios são arquivos soltos sem nenhuma relação registrada entre eles.
- Não existe interface para usuários não técnicos.
- Não é possível comparar resultados de diferentes análises do mesmo projeto ao longo do tempo.
- Não há como buscar ou filtrar análises anteriores.

---

## 3. Objetivo

Evoluir o projeto para um sistema com:

- Interface web para gerenciar análises.
- API REST para operações de CRUD.
- Banco de dados para persistir análises e resultados.
- Integração com o analisador existente para executar a análise ao criar ou atualizar um registro.

O sistema deve permitir que o usuário cadastre uma análise informando o nome, a descrição e o caminho da pasta. O sistema executa o analisador automaticamente e salva o resultado.

---

## 4. Entidades principais

### 4.1 Análise (`Analise`)

Representa um registro de análise realizada sobre uma pasta de projeto.

| Campo               | Tipo     | Descrição                                                                   |
|---------------------|----------|-----------------------------------------------------------------------------|
| `id`                | inteiro  | Identificador único gerado automaticamente.                                 |
| `nome`              | texto    | Nome dado pelo usuário para identificar a análise.                          |
| `descricao`         | texto    | Descrição opcional da análise.                                              |
| `caminho_pasta`     | texto    | Caminho absoluto ou relativo da pasta analisada.                            |
| `nota`              | decimal  | Nota de 0 a 10 gerada pelo analisador.                                      |
| `status`            | enum     | Estado da análise: `pendente`, `concluida`, `erro`.                         |
| `caminho_relatorio` | texto    | Caminho do arquivo Markdown do relatório gerado.                            |
| `resumo_problemas`  | JSON     | Lista resumida dos problemas encontrados pelo analisador.                   |
| `criado_em`         | datetime | Data e hora de criação do registro.                                         |
| `atualizado_em`     | datetime | Data e hora da última atualização.                                          |

---

## 5. Operações CRUD

### 5.1 Create — Cadastrar nova análise

**O que faz:** Cadastra uma nova análise e executa o analisador automaticamente.

**Dados de entrada:**

- `nome` (obrigatório): Nome para identificar a análise.
- `descricao` (opcional): Texto livre de contexto.
- `caminho_pasta` (obrigatório): Caminho da pasta a ser analisada.

**Fluxo:**

1. Usuário preenche o formulário na interface.
2. O frontend envia uma requisição `POST /analises` para a API.
3. A API valida os dados.
4. A API chama o analisador passando o `caminho_pasta`.
5. O analisador executa e retorna nota, lista de problemas e caminho do relatório.
6. A API salva o registro no banco de dados com status `concluida`.
7. A API retorna o registro criado com todos os campos preenchidos.
8. O frontend exibe a nova análise na listagem.

**Validações:**

- `nome` não pode ser vazio.
- `caminho_pasta` não pode ser vazio.
- O caminho informado deve ser uma pasta existente no sistema.
- Se o analisador falhar, o status deve ser gravado como `erro` com mensagem descritiva.

---

### 5.2 Read — Consultar análises

#### Listar todas as análises

**O que faz:** Retorna todas as análises cadastradas.

**Endpoint:** `GET /analises`

**Dados retornados por item:**

- `id`
- `nome`
- `descricao`
- `caminho_pasta`
- `nota`
- `status`
- `criado_em`
- `atualizado_em`

**Comportamento:**

- Retorna lista ordenada pela data de criação, da mais recente para a mais antiga.
- Se não houver análises, retorna lista vazia.

---

#### Visualizar uma análise

**O que faz:** Retorna o detalhe completo de uma análise específica.

**Endpoint:** `GET /analises/{id}`

**Dados retornados:**

- Todos os campos da entidade `Analise`.
- Conteúdo do relatório Markdown gerado (se existir).

**Comportamento:**

- Se o `id` não existir, retorna erro 404.

---

### 5.3 Update — Editar análise

**O que faz:** Atualiza os dados de uma análise existente.

**Endpoint:** `PUT /analises/{id}`

**Dados editáveis:**

- `nome`
- `descricao`
- `caminho_pasta`

**Comportamento:**

- Apenas os campos enviados são atualizados (suporte a atualização parcial).
- Atualiza o campo `atualizado_em` automaticamente.
- Não re-executa o analisador automaticamente ao editar apenas nome ou descrição.

#### Re-executar análise

**O que faz:** Re-executa o analisador sobre o caminho atual da análise e atualiza o resultado.

**Endpoint:** `POST /analises/{id}/reanalisar`

**Comportamento:**

- Roda novamente o analisador com o `caminho_pasta` atual.
- Atualiza `nota`, `status`, `resumo_problemas`, `caminho_relatorio` e `atualizado_em`.
- Se o analisador falhar, atualiza o `status` para `erro`.

---

### 5.4 Delete — Excluir análise

**O que faz:** Remove o registro da análise do banco de dados.

**Endpoint:** `DELETE /analises/{id}`

**Comportamento:**

- Remove apenas o registro do banco.
- **Não exclui** a pasta original analisada.
- **Não exclui** o arquivo de relatório gerado em `reports/`.
- Se o `id` não existir, retorna erro 404.
- Retorna resposta com status 204 (sem conteúdo) em caso de sucesso.

---

## 6. Regras de negócio

| Regra | Descrição                                                                                           |
|-------|------------------------------------------------------------------------------------------------------|
| RN01  | Ao criar uma análise, o analisador deve ser executado automaticamente.                              |
| RN02  | Se o caminho informado não existir ou não for uma pasta, a análise deve ser salva com status `erro`.|
| RN03  | A nota gerada é sempre de 0 a 10, conforme os critérios do analisador.                              |
| RN04  | O relatório Markdown continua sendo salvo na pasta `reports/` conforme o comportamento atual.       |
| RN05  | Excluir uma análise não exclui o relatório nem a pasta original analisada.                          |
| RN06  | O campo `criado_em` não pode ser alterado após a criação.                                           |
| RN07  | O campo `atualizado_em` deve ser atualizado automaticamente em toda operação de escrita.            |
| RN08  | O campo `resumo_problemas` deve armazenar a lista estruturada de problemas em formato JSON.         |
| RN09  | Re-executar uma análise atualiza os campos de resultado, mas mantém o `id` e o `criado_em`.         |
| RN10  | O `nome` da análise não precisa ser único. O `id` é o identificador único.                         |

---

## 7. Fluxo completo do usuário

### Fluxo 1 — Criar e visualizar uma análise

```
1. Usuário acessa a interface web.
2. Clica em "Nova Análise".
3. Preenche: nome, descrição (opcional) e caminho da pasta.
4. Clica em "Analisar".
5. O sistema executa o analisador e exibe o resultado.
6. A análise aparece na listagem com nota e status.
7. Usuário clica na análise para ver os detalhes completos.
8. Visualiza nota, problemas encontrados e link do relatório.
```

### Fluxo 2 — Re-executar uma análise

```
1. Usuário seleciona uma análise existente.
2. Clica em "Re-analisar".
3. O sistema roda o analisador novamente com o mesmo caminho.
4. Os resultados são atualizados na tela.
```

### Fluxo 3 — Editar e re-analisar com novo caminho

```
1. Usuário seleciona uma análise existente.
2. Clica em "Editar".
3. Altera o caminho da pasta.
4. Salva a edição.
5. Clica em "Re-analisar" para rodar com o novo caminho.
6. Os resultados são atualizados.
```

### Fluxo 4 — Excluir uma análise

```
1. Usuário seleciona uma análise existente.
2. Clica em "Excluir".
3. Confirma a exclusão.
4. O registro é removido do banco.
5. A pasta original e o relatório permanecem intocados.
```

---

## 8. Estrutura técnica esperada

```
analisador_organizacao_projetos/
  src/
    analyzer/          <- lógica do analisador (já existente, pode ser refatorada)
    api/               <- API REST (endpoints CRUD)
    database/          <- configuração e modelos do banco de dados
    frontend/          <- interface web do sistema
      pages/           <- arquivos HTML das telas
      styles/          <- arquivos CSS
      scripts/         <- arquivos JavaScript

  specs/               <- PRDs e documentos de especificação
  brain/               <- base de conhecimento e regras do projeto
  skills/              <- instruções e skills do agente
  samples/             <- projetos de exemplo para teste
  reports/             <- relatórios gerados pelo analisador
```

---

## 9. Divisão por camada

### 9.1 `src/analyzer/`

Responsável pela lógica de análise de projetos.

Contém os módulos já existentes:

- `analyzer.py` — ponto de entrada e coordenação da análise.
- `file_scanner.py` — leitura de arquivos e diretórios.
- `naming_checker.py` — validação do padrão de nomes.
- `timestamp_checker.py` — validação de timestamps.
- `order_checker.py` — verificação de coerência de ordem.
- `empty_checker.py` — identificação de arquivos e pastas vazios.
- `loose_file_checker.py` — identificação de arquivos soltos.
- `score.py` — cálculo da nota.
- `report.py` — geração do relatório Markdown.

A camada `api/` deve chamar os módulos de `analyzer/` como biblioteca interna, sem depender do terminal.

---

### 9.2 `src/api/`

Responsável por expor os endpoints REST do CRUD.

Responsabilidades:

- Receber e validar requisições HTTP.
- Chamar o analisador via código (não via subprocess).
- Interagir com o banco de dados via a camada `database/`.
- Retornar respostas em JSON.

Endpoints esperados:

| Método | Endpoint                     | Descrição                               |
|--------|------------------------------|-----------------------------------------|
| GET    | `/analises`                  | Lista todas as análises.                |
| POST   | `/analises`                  | Cria nova análise e executa o analisador.|
| GET    | `/analises/{id}`             | Retorna detalhe de uma análise.         |
| PUT    | `/analises/{id}`             | Edita os dados de uma análise.          |
| POST   | `/analises/{id}/reanalisar`  | Re-executa o analisador.                |
| DELETE | `/analises/{id}`             | Exclui uma análise.                     |

---

### 9.3 `src/database/`

Responsável pela persistência dos dados.

Responsabilidades:

- Definir o modelo da entidade `Analise`.
- Configurar a conexão com o banco de dados.
- Expor funções de acesso a dados (CRUD no banco).

Banco de dados sugerido para o MVP: **SQLite** (arquivo local, zero configuração).

---

### 9.4 `src/frontend/`

Responsável pela interface web.

Tecnologia: HTML, CSS e JavaScript puro (sem framework externo no MVP).

Telas esperadas:

| Tela           | Arquivo              | Descrição                                       |
|----------------|----------------------|-------------------------------------------------|
| Listagem       | `pages/index.html`   | Lista todas as análises com nota e status.      |
| Detalhes       | `pages/detalhe.html` | Exibe detalhes completos de uma análise.        |
| Nova análise   | `pages/nova.html`    | Formulário para criar uma análise.              |
| Editar análise | `pages/editar.html`  | Formulário para editar uma análise.             |

---

## 10. Escopo

### 10.1 Dentro do escopo do CRUD

- Cadastro de análises com nome, descrição e caminho da pasta.
- Execução automática do analisador ao criar ou re-analisar.
- Listagem de análises realizadas.
- Visualização de detalhes de uma análise.
- Edição de nome, descrição e caminho de uma análise.
- Re-execução manual do analisador sobre a análise.
- Exclusão de análises do banco de dados.
- API REST com endpoints CRUD.
- Persistência em banco de dados local (SQLite).
- Interface web simples com HTML, CSS e JavaScript.

### 10.2 Fora do escopo do CRUD

- Autenticação e controle de acesso.
- Multi-usuário.
- Deploy em servidor externo.
- Exportação em PDF.
- Integração com GitHub ou serviços externos.
- Agendamento automático de análises.
- Comparação visual entre duas análises.
- Correção automática de nomes ou estrutura de arquivos.
- Notificações por e-mail ou push.
- Paginação de grandes volumes de análises (não necessário no MVP).

---

## 11. MVP do CRUD

A primeira versão funcional do CRUD deve conter:

- [ ] API com os 5 endpoints principais (GET lista, POST criar, GET detalhe, PUT editar, DELETE excluir).
- [ ] Endpoint de re-análise (`POST /analises/{id}/reanalisar`).
- [ ] Modelo `Analise` no banco de dados com todos os campos definidos.
- [ ] Banco de dados SQLite configurado e funcional.
- [ ] Integração entre a API e o analisador existente (chamada via código, não terminal).
- [ ] Interface web com listagem de análises.
- [ ] Interface web com formulário de criação.
- [ ] Interface web com tela de detalhes.
- [ ] Interface web com formulário de edição.
- [ ] Botão de re-análise na tela de detalhes.
- [ ] Botão de exclusão com confirmação.

---

## 12. Requisitos funcionais do CRUD

### RF-CRUD-01 — Criar análise

O sistema deve permitir criar uma análise informando nome, descrição opcional e caminho da pasta.

### RF-CRUD-02 — Executar analisador ao criar

Ao criar uma análise, o sistema deve executar o analisador automaticamente e salvar o resultado.

### RF-CRUD-03 — Listar análises

O sistema deve listar todas as análises cadastradas, ordenadas da mais recente para a mais antiga.

### RF-CRUD-04 — Visualizar detalhes

O sistema deve exibir todos os campos de uma análise, incluindo nota, problemas encontrados e caminho do relatório.

### RF-CRUD-05 — Editar análise

O sistema deve permitir editar nome, descrição e caminho de uma análise existente.

### RF-CRUD-06 — Re-executar análise

O sistema deve permitir re-executar o analisador sobre uma análise existente e atualizar o resultado.

### RF-CRUD-07 — Excluir análise

O sistema deve permitir excluir um registro de análise sem excluir a pasta original nem o relatório.

### RF-CRUD-08 — Tratar erros de análise

Se o analisador falhar (caminho inválido, pasta inexistente, erro interno), o sistema deve registrar a análise com status `erro` e uma mensagem descritiva.

---

## 13. Requisitos não funcionais do CRUD

### RNF-CRUD-01 — Banco de dados local

O banco de dados do MVP deve ser SQLite para evitar dependência de infraestrutura externa.

### RNF-CRUD-02 — API em JSON

Todos os endpoints devem receber e retornar dados em JSON.

### RNF-CRUD-03 — Frontend sem framework no MVP

A interface web do MVP deve usar apenas HTML, CSS e JavaScript puro.

### RNF-CRUD-04 — Integração interna com o analisador

A API deve chamar o analisador via importação de módulo Python, não via subprocess ou terminal.

### RNF-CRUD-05 — Relatórios existentes preservados

O comportamento atual de geração de relatórios na pasta `reports/` deve ser preservado.

### RNF-CRUD-06 — Compatibilidade com o analisador atual

O analisador deve continuar funcionando de forma independente via linha de comando mesmo após a integração com a API.

---

## 14. Próximos passos técnicos

Ordem recomendada de implementação:

1. Refatorar `src/` para separar a lógica do analisador em `src/analyzer/`.
2. Criar o modelo `Analise` e configurar o banco de dados em `src/database/`.
3. Implementar os endpoints REST em `src/api/`.
4. Integrar a API com o analisador existente.
5. Criar as telas HTML em `src/frontend/pages/`.
6. Estilizar com CSS em `src/frontend/styles/`.
7. Implementar a lógica de chamada à API em `src/frontend/scripts/`.
8. Testar o fluxo completo com as pastas de exemplo em `samples/`.

---

## 15. Resumo

O sistema evolui de uma ferramenta de terminal para um **CRUD web end-to-end**.

O usuário passa a gerenciar análises por uma interface, sem precisar do terminal. A lógica do analisador existente é preservada e integrada à API. O banco de dados persiste o histórico de análises.

O MVP entrega as quatro operações completas — criar, listar, editar e excluir — com interface web, API REST e banco de dados local.

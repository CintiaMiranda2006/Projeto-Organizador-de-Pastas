# Arquitetura do Projeto — Analisador de Organização de Projetos

---

## Estrutura de pastas

### `specs/`

É a pasta onde ficam os PRDs e as regras principais do projeto.
Serve para explicar exatamente o que o sistema deve fazer e quais regras ele precisa seguir.

### `brain/`

É a base de conhecimento do projeto.
Contém documentos que explicam as regras do analisador: padrão de nomes, formato de timestamp, critérios de nota e o que o sistema verifica.
Serve como referência rápida para entender o funcionamento interno.

### `skills/`

São guias de comportamento para o agente de IA que desenvolve o projeto.
Cada Skill é um arquivo Markdown com instruções sobre como criar ou evoluir uma parte específica do sistema — como o frontend ou o design da interface.

### `src/`

É onde fica todo o código do projeto.
Dividida em quatro partes principais: `analyzer`, `api`, `database` e `frontend`.

### `src/analyzer/`

É o coração do sistema.
Contém a lógica que percorre uma pasta, verifica arquivos soltos, vazios, nomes fora do padrão, timestamps inválidos, pastas vazias e ordem incoerente.
No final, calcula a nota e gera o relatório.

### `src/api/`

É a API REST construída com FastAPI.
Recebe as requisições do frontend, chama o analyzer, salva o resultado no banco e retorna os dados formatados.
Também serve o frontend como arquivos estáticos.

### `src/database/`

Cuida da conexão com o banco de dados SQLite.
Contém três arquivos:

- `connection.py`: abre e fecha a conexão.
- `init_db.py`: cria as tabelas na primeira execução.
- `repository.py`: faz as operações de salvar, buscar, atualizar e excluir análises.

### `src/frontend/`

É a interface web do sistema.
O usuário acessa pelo navegador e pode criar, listar, visualizar, editar, reexecutar e excluir análises sem precisar usar o terminal ou o `/docs` da API.

### `src/frontend/pages/`

Contém o arquivo HTML principal da interface (`index.html`).
É a estrutura da tela: formulário, lista de análises, modais de detalhes e edição.

### `src/frontend/styles/`

Contém o CSS do sistema (`style.css`).
Define as cores, tipografia, cards, botões, badges, modais e responsividade da interface.

### `src/frontend/scripts/`

Contém o JavaScript dividido em três arquivos:

- `api.js`: faz as chamadas para os endpoints da API.
- `ui.js`: monta e atualiza os elementos da tela.
- `analyses.js`: coordena o fluxo completo do CRUD e os eventos do usuário.

### `samples/`

Pasta com exemplos de projetos para testar o analisador.
Contém três subpastas:

- `projeto_organizado/`: exemplo bem estruturado, nota alta esperada.
- `projeto_baguncado/`: exemplo com vários problemas, nota baixa esperada.
- `projeto_com_prds/`: exemplo com foco em PRDs.

### `reports/`

Pasta onde os relatórios Markdown são salvos automaticamente após cada análise.
O nome do arquivo segue o padrão: `<nome_da_pasta_analisada>_relatorio.md`.

### `docs/`

Documentação técnica do projeto.
Contém este arquivo de arquitetura e o registro dos MCPs utilizados.

### `README.md`

O arquivo principal de apresentação do projeto.
Explica o que o sistema faz, como instalar, como rodar a API, como abrir o frontend e como usar o CRUD.
É a primeira coisa que qualquer pessoa deve ler ao chegar no projeto.

### `requirements.txt`

Lista de dependências Python do projeto.
Para instalar tudo de uma vez:

```bash
py -m pip install -r requirements.txt
```

### `database.db`

O banco de dados SQLite criado automaticamente quando a API inicia pela primeira vez.
Armazena todas as análises cadastradas: nome, descrição, caminho, nota, status, resumo dos problemas e caminhos dos relatórios.
Não precisa ser configurado — é gerado sozinho.

---

## Fluxo principal do sistema

1. O usuário preenche o formulário no frontend com nome, descrição e caminho da pasta.
2. O frontend envia os dados para a API via `POST /analyses`.
3. A API recebe os dados e chama o analyzer.
4. O analyzer percorre a pasta, verifica os arquivos e calcula a nota.
5. O relatório Markdown é gerado e salvo em `reports/`.
6. O resultado (nota, status, resumo e listas de problemas) é salvo no banco SQLite.
7. O frontend exibe o card com nota, status e botões de ação. O usuário pode ver os detalhes, editar, reexecutar ou excluir.

---

## Principais partes para o funcionamento

| Parte | Função |
|---|---|
| **Frontend** | Interface usada pelo usuário para interagir com o sistema. |
| **API** | Recebe as requisições, coordena o fluxo e expõe os endpoints do CRUD. |
| **Database** | Salva e recupera as análises cadastradas. |
| **Analyzer** | Faz a análise real das pastas: verifica nomes, timestamps, arquivos vazios e muito mais. |
| **Reports** | Guarda os relatórios Markdown gerados após cada análise. |
| **Specs / Brain / Skills** | Guiam as regras do sistema, a base de conhecimento e a forma como o agente deve desenvolver o projeto. |

---

## MCPs utilizados

### Sequential Thinking

Usado para ajudar o agente a planejar etapas maiores antes de alterar qualquer arquivo.
Antes de criar o frontend, por exemplo, o Sequential Thinking foi usado para definir a ordem correta de criação dos arquivos, as decisões de design e os possíveis problemas a considerar.

### Chrome DevTools for agents

Usado para auxiliar na validação do frontend diretamente no navegador.
Depois de criar a interface, o Chrome DevTools abriu a página, inspecionou o console em busca de erros, testou o fluxo de criação de análise e confirmou que tudo funcionou de ponta a ponta.

---

## Skills utilizadas

### `frontend_crud_builder`

Orienta o agente a criar o frontend conectado ao CRUD da API.
Define quais telas criar, quais endpoints consumir, como tratar erros e qual fluxo o usuário deve seguir.

### `frontend_ui_design`

Orienta o agente a criar uma interface limpa, responsiva e visualmente consistente.
Define as regras de cores, tipografia, espaçamento, botões, cards, modais e mensagens de estado.

---

## Resumo da arquitetura

O projeto é um **CRUD end-to-end de análises de organização de projetos**.

O usuário acessa o **frontend** pelo navegador, cria análises informando o caminho de uma pasta, e o sistema usa o **analyzer** em Python para verificar a organização dos arquivos. O resultado é salvo no **banco SQLite** e o relatório é gerado em **Markdown**. A comunicação entre frontend e backend acontece via **API FastAPI**.

O projeto também é guiado por **PRDs** na pasta `specs/`, tem uma **base de conhecimento** em `brain/`, e usa **Skills** que orientam o agente no desenvolvimento. Dois **MCPs** foram utilizados durante a construção: o Sequential Thinking para planejamento e o Chrome DevTools para validação do frontend.

É um projeto completo, com documentação, exemplos de teste, regras bem definidas e uma interface funcional.

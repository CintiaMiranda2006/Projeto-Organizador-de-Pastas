# Analisador de Organização de Projetos

Sistema CRUD end-to-end para analisar a organização estrutural de pastas de projeto e gerenciar o histórico de análises.

---

## O que é este projeto

O **Analisador de Organização de Projetos** percorre uma pasta, identifica problemas de organização e gera um relatório em Markdown com nota, lista de problemas e sugestões de melhoria.

A ferramenta não avalia qualidade de código, testes, Docker ou deploy. Ela avalia apenas a **estrutura e organização dos arquivos e pastas**.

O sistema agora possui uma **API REST** e uma **interface web** para gerenciar análises sem precisar do terminal.

---

## O que o analisador verifica

| Critério | Descrição | Pontuação |
|---|---|---:|
| Organização de pastas | Se os arquivos estão em subpastas ou soltos na raiz | 2 pt |
| Arquivos soltos | Arquivos diretamente na raiz sem estrutura de pastas | 2 pt |
| Arquivos vazios | Arquivos com tamanho zero | 1 pt |
| Pastas vazias | Diretórios sem nenhum arquivo | 1 pt |
| Padrão de nomes | Se os nomes seguem `ordem_tipo_assunto_aammdd_hhmm.extensao` | 2 pt |
| Timestamp | Se o timestamp existe e é válido (`AAMMDD_HHMM`) | 1 pt |
| Coerência de ordem | Se `a`, `b`, `c`... estão em ordem cronológica crescente | 1 pt |
| **Total** | | **10 pt** |

---

## Pré-requisitos

- Python 3.8 ou superior

```bash
python --version
```

---

## Instalação

```bash
py -m pip install -r requirements.txt
```

---

## Como rodar a API

```bash
py -m uvicorn src.api.main:app --reload
```

A API ficará disponível em:

```
http://127.0.0.1:8000
```

---

## Como abrir o frontend

Com a API rodando, abra no navegador:

```
http://127.0.0.1:8000/app/pages/index.html
```

Ou acesse a raiz e o sistema redireciona automaticamente:

```
http://127.0.0.1:8000
```

---

## Documentação da API

O FastAPI gera documentação interativa automaticamente:

```
http://127.0.0.1:8000/docs
```

---

## Como usar o CRUD

### Criar análise

1. Preencha o formulário na tela inicial:
   - **Nome da análise** (obrigatório)
   - **Descrição** (opcional)
   - **Caminho da pasta** (obrigatório — pode ser relativo ou absoluto)
2. Clique em **Analisar**.
3. O sistema executa o analisador e exibe o resultado com nota e status.

Exemplos de caminhos para testar:

```
./samples/projeto_organizado    → nota esperada: 10.0
./samples/projeto_baguncado     → nota esperada: baixa
./samples/projeto_com_prds      → nota esperada: média/alta
```

### Listar análises

As análises aparecem automaticamente na lista abaixo do formulário, ordenadas da mais recente para a mais antiga.

### Ver detalhes

Clique em **Detalhes** para ver:
- Nota completa com detalhamento por critério.
- Contagem de problemas encontrados.
- Caminho do relatório gerado.

### Editar análise

Clique em **Editar** para alterar nome, descrição ou caminho da pasta. A edição não reexecuta a análise automaticamente.

### Reexecutar análise

Clique em **Reexecutar** para rodar o analisador novamente com o caminho atual e atualizar o resultado.

### Excluir análise

Clique em **Excluir** e confirme. O registro é removido do banco de dados. A pasta original e o relatório gerado não são apagados.

---

## Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/analyses` | Cria análise e executa o analisador |
| `GET` | `/analyses` | Lista todas as análises |
| `GET` | `/analyses/{id}` | Detalhe completo de uma análise |
| `PUT` | `/analyses/{id}` | Atualiza nome, descrição ou caminho |
| `POST` | `/analyses/{id}/rerun` | Reexecuta o analisador |
| `DELETE` | `/analyses/{id}` | Exclui o registro |

---

## Onde os relatórios são gerados

Os relatórios são salvos automaticamente na pasta `reports/` na raiz do projeto:

```
analisador_organizacao_projetos/
  reports/
    projeto_organizado_relatorio.md
    projeto_baguncado_relatorio.md
```

O arquivo é nomeado como `<nome_da_pasta_analisada>_relatorio.md`.

---

## Estrutura do projeto

```
analisador_organizacao_projetos/
  src/
    analyzer/                    # Lógica do analisador (pacote Python)
      service.py                 # Servico chamado pela API
      file_scanner.py
      naming_checker.py
      timestamp_checker.py
      order_checker.py
      empty_checker.py
      loose_file_checker.py
      score.py
      report.py

    api/                         # API REST (FastAPI)
      main.py                    # Ponto de entrada da aplicacao
      routes.py                  # Rotas do CRUD
      schemas.py                 # Modelos Pydantic

    database/                    # Banco de dados (SQLite)
      connection.py              # Conexao com o banco
      init_db.py                 # Criacao das tabelas
      repository.py              # Operacoes CRUD no banco

    frontend/                    # Interface web
      pages/
        index.html               # Pagina principal
      styles/
        style.css                # Estilos
      scripts/
        api.js                   # Chamadas para a API
        ui.js                    # Renderizacao do DOM
        analyses.js              # Fluxo e handlers

  brain/                         # Base de conhecimento do projeto
    padrao_de_nomes.md
    padrao_de_timestamp.md
    criterios_de_nota.md
    regras_de_organizacao.md

  docs/                          # Documentacao tecnica
    mcp_utilizados.md

  specs/                         # PRDs e especificacoes
    prd_analisador_organizacao_projetos.md
    prd_crud_analises_organizacao.md

  skills/                        # Skills do agente
    frontend_crud_builder/
      SKILL.md
    frontend_ui_design/
      SKILL.md

  samples/                       # Pastas de exemplo para teste
    projeto_organizado/
    projeto_baguncado/
    projeto_com_prds/

  reports/                       # Relatorios gerados
  database.db                    # Banco SQLite (criado automaticamente)
  requirements.txt
  .gitignore
  README.md
```

---

## Skills do projeto

O projeto possui Skills que orientam o agente no desenvolvimento:

| Skill | Localização | Objetivo |
|---|---|---|
| Frontend CRUD Builder | `skills/frontend_crud_builder/SKILL.md` | Guia para criar e evoluir o frontend do sistema |
| Frontend UI Design | `skills/frontend_ui_design/SKILL.md` | Guia de design, layout, cores e acessibilidade |

---

## MCPs utilizados

| MCP | Uso |
|---|---|
| Sequential Thinking | Planejamento de tarefas e organização de etapas |
| Chrome DevTools for agents | Validacao do frontend e inspecao de erros no navegador |

Mais detalhes em `docs/mcp_utilizados.md`.

---

## Analisador via terminal (modo legado)

O analisador continua funcionando de forma independente pelo terminal:

```bash
python src/analyzer.py <caminho_da_pasta>
```

Exemplos:

```bash
python src/analyzer.py ./samples/projeto_organizado
python src/analyzer.py ./samples/projeto_baguncado
python src/analyzer.py C:/Users/usuario/meu_projeto
```

---

_Projeto desenvolvido como sistema CRUD end-to-end para avaliacao de organizacao estrutural de projetos digitais._

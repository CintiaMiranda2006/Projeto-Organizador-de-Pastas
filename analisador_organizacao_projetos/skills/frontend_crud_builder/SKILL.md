# Skill — Frontend CRUD Builder

## Objetivo

Esta Skill ensina o agente a criar e evoluir o frontend do projeto **Analisador de Organização de Projetos**.

O frontend deve consumir a API FastAPI existente e permitir que o usuário use o CRUD de análises sem precisar acessar diretamente o `/docs`.

---

## Quando usar esta Skill

Use esta Skill sempre que a tarefa envolver:

* criar tela inicial do sistema;
* criar listagem de análises;
* criar formulário de nova análise;
* criar tela de detalhes;
* editar análise;
* excluir análise;
* reexecutar análise;
* conectar HTML, CSS e JavaScript com a API;
* melhorar a usabilidade do CRUD.

---

## Estrutura obrigatória do frontend

O frontend deve ficar dentro de:

```text
src/frontend/
  pages/
  styles/
  scripts/
```

Use a estrutura:

```text
src/frontend/pages/index.html
src/frontend/styles/style.css
src/frontend/scripts/app.js
```

Se o projeto crescer, separar scripts por responsabilidade:

```text
src/frontend/scripts/api.js
src/frontend/scripts/analyses.js
src/frontend/scripts/ui.js
```

---

## API que o frontend deve consumir

O frontend deve usar os endpoints já existentes do backend:

```text
POST /analyses
GET /analyses
GET /analyses/{id}
PUT /analyses/{id}
POST /analyses/{id}/rerun
DELETE /analyses/{id}
```

A URL base padrão deve ser:

```text
http://127.0.0.1:8000
```

---

## Funcionalidades obrigatórias da tela

A tela principal deve ter:

1. Formulário para criar nova análise.
2. Lista de análises salvas.
3. Botão para visualizar detalhes.
4. Botão para editar análise.
5. Botão para reexecutar análise.
6. Botão para excluir análise.
7. Exibição da nota da análise.
8. Exibição do status.
9. Exibição do caminho analisado.
10. Exibição do caminho do relatório gerado.

---

## Formulário de nova análise

O formulário deve conter:

* nome da análise;
* descrição opcional;
* caminho da pasta que será analisada.

Ao enviar o formulário:

1. Chamar `POST /analyses`.
2. Mostrar mensagem de carregamento.
3. Atualizar a lista de análises.
4. Mostrar erro claro se o caminho for inválido.

---

## Listagem de análises

A listagem deve exibir:

* ID;
* nome;
* descrição;
* caminho analisado;
* nota;
* status;
* data de criação;
* data de atualização;
* ações disponíveis.

Cada análise deve ter botões para:

```text
Detalhes
Editar
Reexecutar
Excluir
```

---

## Tela ou seção de detalhes

Ao clicar em detalhes, o frontend deve chamar:

```text
GET /analyses/{id}
```

E mostrar:

* nome;
* descrição;
* caminho analisado;
* nota;
* resumo dos problemas;
* caminho do relatório;
* data de criação;
* data de atualização.

---

## Edição de análise

Ao editar, o usuário pode alterar:

* nome;
* descrição;
* caminho da pasta.

A edição deve chamar:

```text
PUT /analyses/{id}
```

A edição não deve reexecutar a análise automaticamente.

---

## Reexecução de análise

Ao clicar em reexecutar, o frontend deve chamar:

```text
POST /analyses/{id}/rerun
```

Depois deve atualizar os dados da análise na tela.

Use mensagem clara, por exemplo:

```text
Reexecutando análise...
Análise atualizada com sucesso.
Erro ao reexecutar análise.
```

---

## Exclusão de análise

Ao excluir, o frontend deve chamar:

```text
DELETE /analyses/{id}
```

Antes de excluir, pedir confirmação.

A exclusão remove apenas a análise salva no banco.

Nunca excluir a pasta original analisada.

---

## Regras de interface

A interface deve ser simples, limpa e funcional.

Não criar frontend complexo.

Não usar framework nesta primeira versão.

Usar apenas:

```text
HTML
CSS
JavaScript puro
```

A tela deve priorizar funcionamento, clareza e facilidade de teste.

---

## Regras importantes

O frontend não deve conter lógica de análise de arquivos.

Toda análise deve ser feita pelo backend.

O frontend apenas:

* envia dados;
* recebe respostas da API;
* mostra resultados;
* executa ações do CRUD.

Não duplicar regras de timestamp, nomes ou pontuação no JavaScript.

---

## Fluxo esperado

O fluxo completo do usuário deve ser:

```text
Usuário abre o frontend
↓
Cadastra uma nova análise
↓
Informa o caminho da pasta
↓
Frontend chama a API
↓
Backend executa o analyzer
↓
Backend salva no SQLite
↓
Backend gera relatório
↓
Frontend mostra a análise na lista
↓
Usuário pode ver detalhes, editar, reexecutar ou excluir
```

---

## Antes de alterar o frontend

Antes de criar ou modificar arquivos, o agente deve verificar:

1. Se a API está funcionando.
2. Quais endpoints existem.
3. Qual formato de resposta a API retorna.
4. Se o backend permite CORS, caso necessário.
5. Se os arquivos devem ficar em `src/frontend/`.

---

## Depois de alterar o frontend

Ao terminar, o agente deve informar:

* arquivos criados ou alterados;
* como rodar o backend;
* como abrir o frontend;
* como testar o CRUD completo;
* quais endpoints o frontend está consumindo.

---

## Limites

Não criar login.

Não criar autenticação.

Não criar dashboard avançado.

Não criar gráficos agora.

Não criar framework React, Vue ou Angular.

Não alterar regras do analyzer.

Não alterar banco sem necessidade.

Não mudar endpoints existentes sem avisar.

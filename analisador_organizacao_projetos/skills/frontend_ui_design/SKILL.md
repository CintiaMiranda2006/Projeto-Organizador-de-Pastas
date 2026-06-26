# Skill — Frontend UI Design

## Objetivo

Esta Skill orienta o agente a criar interfaces bonitas, limpas, responsivas e fáceis de usar no projeto **Analisador de Organização de Projetos**.

Ela deve ser usada sempre que o agente criar ou alterar telas, estilos, componentes visuais, formulários, cards, tabelas, botões, mensagens e estados de carregamento.

---

## Quando usar esta Skill

Use esta Skill em tarefas envolvendo:

* criação de telas;
* melhoria visual do frontend;
* organização de layout;
* criação de formulários;
* criação de cards;
* criação de tabelas;
* criação de botões;
* mensagens de erro, sucesso e carregamento;
* responsividade;
* acessibilidade básica;
* padronização visual.

---

## Princípios visuais obrigatórios

A interface deve ser:

* limpa;
* moderna;
* legível;
* objetiva;
* responsiva;
* consistente;
* fácil de usar.

Evite telas poluídas, excesso de cores, fontes pequenas, espaçamentos apertados e elementos desalinhados.

---

## Estrutura visual recomendada

A tela principal deve ter:

1. Cabeçalho com nome do sistema.
2. Breve descrição do que o sistema faz.
3. Card ou seção para criar nova análise.
4. Lista ou tabela de análises cadastradas.
5. Área de detalhes da análise selecionada.
6. Mensagens claras de erro, sucesso e carregamento.

A interface deve deixar claro o fluxo:

```text
Criar análise
↓
Ver resultado
↓
Consultar detalhes
↓
Editar, reexecutar ou excluir
```

---

## Layout

Use um layout centralizado, com largura máxima para não deixar o conteúdo espalhado demais em telas grandes.

Recomendação:

```css
max-width: 1200px;
margin: 0 auto;
padding: 24px;
```

Use espaçamentos consistentes entre seções.

Evite elementos colados uns nos outros.

---

## Cores

Use uma paleta simples e profissional.

Recomendações:

* fundo claro ou levemente acinzentado;
* cards brancos;
* texto principal escuro;
* texto secundário cinza;
* cor principal para botões e destaques;
* vermelho apenas para erros e exclusão;
* verde apenas para sucesso;
* amarelo/laranja apenas para alerta.

Não usar muitas cores diferentes.

---

## Tipografia

Use fontes legíveis e padrão do sistema.

Recomendação:

```css
font-family: Arial, Helvetica, sans-serif;
```

Regras:

* títulos maiores e bem definidos;
* textos comuns com tamanho confortável;
* labels claros nos formulários;
* evitar textos longos em blocos grandes;
* usar hierarquia visual.

---

## Cards

Use cards para separar informações importantes.

Exemplo de uso:

* card do formulário;
* card de resumo da análise;
* card de detalhes;
* card de problemas encontrados.

Os cards devem ter:

* fundo branco;
* borda leve;
* sombra suave;
* bordas arredondadas;
* espaçamento interno adequado.

---

## Formulários

Os formulários devem ser simples e claros.

Cada campo deve ter:

* label visível;
* placeholder útil;
* espaçamento adequado;
* mensagem de erro quando necessário.

Campos obrigatórios devem ser fáceis de identificar.

O formulário de nova análise deve conter:

* nome da análise;
* descrição;
* caminho da pasta.

---

## Botões

Os botões devem ter aparência consistente.

Tipos principais:

* botão primário: criar análise ou salvar;
* botão secundário: detalhes ou editar;
* botão de alerta: reexecutar;
* botão perigoso: excluir.

Regras:

* botões devem ter texto claro;
* evitar botões só com ícone;
* botões destrutivos devem pedir confirmação;
* botões devem ter estado visual de hover;
* botões devem ficar desabilitados durante carregamentos.

---

## Tabelas e listas

A lista de análises deve ser fácil de ler.

Pode ser tabela ou cards.

Deve exibir:

* nome;
* caminho analisado;
* nota;
* status;
* data de criação;
* ações disponíveis.

Em telas pequenas, prefira cards no lugar de tabela muito larga.

---

## Nota da análise

A nota deve ter destaque visual.

Exemplo:

```text
Nota: 8.5/10
```

Sugestão visual:

* nota alta: aparência positiva;
* nota média: aparência de alerta;
* nota baixa: aparência crítica.

Não exagerar nas cores.

---

## Mensagens de estado

A interface deve mostrar mensagens claras para:

* carregando;
* análise criada com sucesso;
* erro ao criar análise;
* caminho inválido;
* análise reexecutada;
* análise excluída;
* erro de conexão com API.

Exemplos:

```text
Criando análise...
Análise criada com sucesso.
Não foi possível acessar esse caminho.
Erro ao conectar com a API.
```

---

## Responsividade

A interface deve funcionar bem em:

* desktop;
* notebook;
* tablet;
* celular.

Regras:

* evitar largura fixa grande;
* usar `flex-wrap` quando necessário;
* permitir que cards quebrem linha;
* em telas pequenas, empilhar elementos verticalmente;
* evitar tabelas quebradas em mobile.

---

## Acessibilidade básica

O frontend deve seguir práticas básicas:

* labels associados aos inputs;
* botões com texto claro;
* contraste adequado entre texto e fundo;
* foco visível ao navegar pelo teclado;
* mensagens de erro fáceis de entender;
* não depender apenas de cor para indicar estado.

---

## Organização do CSS

O CSS deve ser organizado por seções.

Sugestão:

```css
/* Reset básico */
/* Layout */
/* Header */
/* Cards */
/* Formulários */
/* Botões */
/* Lista de análises */
/* Detalhes */
/* Estados */
/* Responsividade */
```

Evite CSS bagunçado, duplicado ou sem padrão.

---

## Organização do JavaScript

O JavaScript não deve misturar regra de negócio com manipulação visual de forma confusa.

Separar, quando possível:

```text
api.js       → chamadas para API
ui.js        → atualização da tela
analyses.js  → fluxo das análises
```

O frontend não deve duplicar regras do analyzer.

Toda análise deve ser feita pelo backend.

---

## Limites

Não criar visual exagerado.

Não usar emojis.

Não usar bibliotecas externas sem necessidade.

Não usar React, Vue ou Angular nesta primeira versão.

Não criar dashboard complexo.

Não criar gráficos agora.

Não mudar endpoints da API por causa do frontend.

Não colocar regra de análise no JavaScript.

---

## Resultado esperado

Ao finalizar qualquer tarefa visual, o agente deve entregar uma interface:

* funcional;
* organizada;
* agradável visualmente;
* responsiva;
* conectada à API;
* fácil de testar;
* coerente com o projeto.

O agente deve informar:

* quais arquivos visuais foram criados ou alterados;
* como abrir a tela;
* como testar o fluxo;
* se houve alguma limitação.

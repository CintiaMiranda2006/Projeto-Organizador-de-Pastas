# MCPs Utilizados no Projeto

Este documento registra os MCPs (Model Context Protocol) utilizados durante o desenvolvimento do Analisador de Organização de Projetos.

---

## Sequential Thinking

**Uso:** planejamento de tarefas maiores e organização das etapas de desenvolvimento.

O Sequential Thinking foi utilizado para estruturar o raciocínio antes de implementar funcionalidades complexas, como:

- Definir a arquitetura do frontend antes de criar os arquivos.
- Planejar a ordem correta de criação de componentes (api.js → ui.js → analyses.js → style.css → index.html).
- Identificar decisões técnicas críticas (CORS, caminhos de arquivos estáticos, separação de responsabilidades).
- Validar premissas antes de alterar código existente.

**Benefício:** evita implementações precipitadas e garante que todas as dependências e implicações sejam consideradas antes de qualquer alteração.

---

## Chrome DevTools for agents

**Uso:** validação do frontend, inspeção de erros no navegador e verificação de problemas visuais ou de JavaScript.

O Chrome DevTools foi utilizado para:

- Abrir o frontend em `http://127.0.0.1:8000/app/pages/index.html` e verificar se a página carregava corretamente.
- Inspecionar o console do navegador em busca de erros de JavaScript, falhas de rede ou bloqueios de CORS.
- Testar o fluxo completo do CRUD diretamente no navegador: criar análise, ver detalhes, editar e reexecutar.
- Confirmar que os toasts de estado e os modais abriam e fechavam corretamente.
- Verificar que o indicador de "API conectada" aparecia em verde.

**Benefício:** permite validar o frontend de forma automatizada sem depender de interação manual do usuário, garantindo que o sistema funciona de ponta a ponta.

---

## Configuração dos MCPs

Os MCPs estão configurados no ambiente do agente e não requerem instalação adicional no projeto.

Para mais informações sobre os MCPs disponíveis, consulte a documentação do ambiente de desenvolvimento.

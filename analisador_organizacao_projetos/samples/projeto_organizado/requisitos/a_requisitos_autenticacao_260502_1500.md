# Requisitos — Autenticação

## Requisitos funcionais

- RF01: O sistema deve autenticar usuários por email e senha.
- RF02: O sistema deve gerar token JWT com validade de 24h.
- RF03: O sistema deve revogar tokens em caso de logout.

## Requisitos não funcionais

- RNF01: O tempo de resposta do login deve ser menor que 500ms.
- RNF02: O sistema deve suportar 1000 requisições simultâneas.

## Dependências

- Biblioteca de criptografia para hash de senha.
- Serviço de envio de email para recuperação de senha.

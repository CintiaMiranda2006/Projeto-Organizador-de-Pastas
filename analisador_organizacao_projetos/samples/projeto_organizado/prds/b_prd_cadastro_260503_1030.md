# PRD — Sistema de Cadastro

## Visão geral

Requisitos para o módulo de cadastro de novos usuários na plataforma.

## Funcionalidades

- Formulário com nome, email e senha.
- Validação de formato de email.
- Verificação de email duplicado.
- Envio de email de boas-vindas após cadastro bem-sucedido.

## Regras de negócio

- Não é permitido cadastrar dois usuários com o mesmo email.
- O nome deve ter no mínimo 3 caracteres.
- A confirmação de senha deve ser idêntica à senha digitada.

## Critérios de aceite

- Novo usuário é criado com dados válidos.
- Email de boas-vindas é enviado em até 1 minuto.
- Mensagem de erro é exibida quando email já está em uso.

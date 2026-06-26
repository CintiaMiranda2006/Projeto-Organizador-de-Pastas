# Decisões Técnicas

## Data: 08/06/2026

## Contexto

Registro das principais decisões técnicas tomadas durante a fase de especificação.

## Decisões

### 1. Gateway de pagamento

**Decisão:** Utilizar Stripe como gateway principal.
**Motivo:** Melhor documentação, SDK em Python e suporte a PIX.

### 2. Banco de dados para analytics

**Decisão:** ClickHouse para dados analíticos.
**Motivo:** Alta performance para consultas agregadas em grandes volumes.

### 3. WebSocket para notificações

**Decisão:** Utilizar socket.io com fallback para long-polling.
**Motivo:** Compatibilidade com browsers legados.

### 4. Formato de exportação

**Decisão:** PDF gerado server-side com WeasyPrint.
**Motivo:** Controle total sobre o layout sem dependências de cliente.

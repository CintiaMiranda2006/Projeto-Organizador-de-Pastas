/**
 * api.js — Chamadas à API FastAPI do Analisador de Organização de Projetos.
 *
 * Todas as funções são async e lançam erros com mensagens legíveis.
 * Nenhuma lógica de negócio ou de DOM aqui.
 */

const API_BASE = "http://127.0.0.1:8000";

/**
 * Wrapper central de fetch. Lança Error com mensagem legível em caso de falha.
 */
async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;
  let response;
  try {
    response = await fetch(url, {
      headers: { "Content-Type": "application/json", ...options.headers },
      ...options,
    });
  } catch (networkErr) {
    throw new Error(
      "Não foi possível conectar à API. Verifique se o backend está rodando em " +
        API_BASE
    );
  }

  if (response.status === 204) return null;

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = data?.detail || `Erro HTTP ${response.status}`;
    throw new Error(detail);
  }

  return data;
}

// ── Endpoints ─────────────────────────────────────────────────────────────────

/** GET /analyses — lista todas as análises */
async function listAnalyses() {
  return apiFetch("/analyses");
}

/** GET /analyses/{id} — detalhe completo */
async function getAnalysis(id) {
  return apiFetch(`/analyses/${id}`);
}

/** POST /analyses — criar análise */
async function createAnalysis(name, description, targetPath) {
  return apiFetch("/analyses", {
    method: "POST",
    body: JSON.stringify({ name, description, target_path: targetPath }),
  });
}

/** PUT /analyses/{id} — atualizar campos */
async function updateAnalysis(id, name, description, targetPath) {
  const body = {};
  if (name !== undefined) body.name = name;
  if (description !== undefined) body.description = description;
  if (targetPath !== undefined) body.target_path = targetPath;
  return apiFetch(`/analyses/${id}`, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

/** POST /analyses/{id}/rerun — reexecutar análise */
async function rerunAnalysis(id) {
  return apiFetch(`/analyses/${id}/rerun`, { method: "POST", body: "{}" });
}

/** DELETE /analyses/{id} — excluir análise */
async function deleteAnalysis(id) {
  return apiFetch(`/analyses/${id}`, { method: "DELETE" });
}

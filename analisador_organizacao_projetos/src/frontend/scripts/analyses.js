/**
 * analyses.js — Coordena o fluxo das análises.
 *
 * Responsável por:
 *   - inicializar a página
 *   - conectar eventos de formulário, botões e modais
 *   - chamar api.js e atualizar o DOM via ui.js
 */

// Cache local para evitar busca desnecessária ao editar
let currentAnalyses = [];

// ── Handlers de ação ──────────────────────────────────────────────────────────

const cardHandlers = {
  onDetail: handleDetail,
  onEdit: handleEdit,
  onRerun: handleRerun,
  onDelete: handleDelete,
};

// ── Inicialização ─────────────────────────────────────────────────────────────

async function init() {
  await loadAnalyses();

  // Formulário de criação
  document.getElementById("form-create").addEventListener("submit", handleCreate);

  // Formulário de edição
  document.getElementById("form-edit").addEventListener("submit", handleSaveEdit);

  // Fechar modais
  document.getElementById("btn-close-detail").addEventListener("click", closeDetailModal);
  document.getElementById("btn-close-edit").addEventListener("click", closeEditModal);
  document.getElementById("btn-cancel-edit").addEventListener("click", closeEditModal);

  // Fechar modal clicando no overlay
  document.getElementById("modal-detail").addEventListener("click", (e) => {
    if (e.target === e.currentTarget) closeDetailModal();
  });
  document.getElementById("modal-edit").addEventListener("click", (e) => {
    if (e.target === e.currentTarget) closeEditModal();
  });

  // ESC fecha modais
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeDetailModal();
      closeEditModal();
    }
  });
}

// ── Carregar lista ────────────────────────────────────────────────────────────

async function loadAnalyses() {
  showListLoading();
  try {
    const analyses = await listAnalyses();
    currentAnalyses = analyses || [];
    renderAnalysisList(currentAnalyses, cardHandlers);
  } catch (err) {
    showListError(err.message);
  }
}

// ── Criar análise ─────────────────────────────────────────────────────────────

async function handleCreate(e) {
  e.preventDefault();
  const name = document.getElementById("create-name").value.trim();
  const description = document.getElementById("create-description").value.trim();
  const targetPath = document.getElementById("create-path").value.trim();

  if (!name) { showToast("O nome da análise é obrigatório.", "error"); return; }
  if (!targetPath) { showToast("O caminho da pasta é obrigatório.", "error"); return; }

  setFormLoading(true);
  showToast("Criando análise...", "info");

  try {
    const analysis = await createAnalysis(name, description || null, targetPath);
    currentAnalyses.unshift(analysis);
    prependCard(analysis, cardHandlers);
    clearCreateForm();
    showToast(
      analysis.status === "error"
        ? `Análise salva com erro: ${analysis.summary?.error || "Caminho inválido."}`
        : "Análise criada com sucesso.",
      analysis.status === "error" ? "error" : "success"
    );
  } catch (err) {
    showToast(`Erro ao criar análise: ${err.message}`, "error");
  } finally {
    setFormLoading(false);
  }
}

// ── Ver detalhes ──────────────────────────────────────────────────────────────

async function handleDetail(id) {
  showToast("Carregando detalhes...", "info");
  try {
    const analysis = await getAnalysis(id);
    openDetailModal(analysis);
  } catch (err) {
    showToast(`Erro ao buscar detalhes: ${err.message}`, "error");
  }
}

// ── Editar ────────────────────────────────────────────────────────────────────

function handleEdit(analysis) {
  openEditModal(analysis);
}

async function handleSaveEdit(e) {
  e.preventDefault();
  const id = Number(document.getElementById("edit-id").value);
  const name = document.getElementById("edit-name").value.trim();
  const description = document.getElementById("edit-description").value.trim();
  const targetPath = document.getElementById("edit-path").value.trim();

  if (!name) { showToast("O nome não pode ser vazio.", "error"); return; }

  setEditLoading(true);
  try {
    const updated = await updateAnalysis(id, name, description || null, targetPath || undefined);
    // Atualizar cache
    const idx = currentAnalyses.findIndex((a) => a.id === id);
    if (idx !== -1) currentAnalyses[idx] = updated;
    // Atualizar card na lista
    updateCardInList(updated, cardHandlers);
    closeEditModal();
    showToast("Análise atualizada com sucesso.", "success");
  } catch (err) {
    showToast(`Erro ao salvar: ${err.message}`, "error");
  } finally {
    setEditLoading(false);
  }
}

// ── Reexecutar ────────────────────────────────────────────────────────────────

async function handleRerun(id, btn) {
  if (!confirm("Deseja reexecutar a análise? O resultado será atualizado.")) return;

  const originalText = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Executando...";
  showToast("Reexecutando análise...", "info");

  try {
    const updated = await rerunAnalysis(id);
    const idx = currentAnalyses.findIndex((a) => a.id === id);
    if (idx !== -1) currentAnalyses[idx] = updated;
    updateCardInList(updated, cardHandlers);
    showToast(
      updated.status === "error"
        ? "Erro ao reexecutar. Verifique o caminho da pasta."
        : "Análise reexecutada com sucesso.",
      updated.status === "error" ? "error" : "success"
    );
  } catch (err) {
    btn.disabled = false;
    btn.textContent = originalText;
    showToast(`Erro ao reexecutar: ${err.message}`, "error");
  }
}

// ── Excluir ───────────────────────────────────────────────────────────────────

async function handleDelete(id) {
  if (!confirm("Excluir esta análise? O registro será removido do banco.\nA pasta original não será apagada.")) return;

  showToast("Excluindo análise...", "info");
  try {
    await deleteAnalysis(id);
    currentAnalyses = currentAnalyses.filter((a) => a.id !== id);
    removeCardFromList(id);
    showToast("Análise excluída.", "success");
  } catch (err) {
    showToast(`Erro ao excluir: ${err.message}`, "error");
  }
}

// ── Iniciar quando o DOM estiver pronto ───────────────────────────────────────
document.addEventListener("DOMContentLoaded", init);

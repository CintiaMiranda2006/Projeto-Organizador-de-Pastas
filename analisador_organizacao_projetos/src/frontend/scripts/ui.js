/**
 * ui.js — Funções de renderização e manipulação de DOM.
 *
 * Responsável por:
 *   - criar/atualizar cards de análise na lista
 *   - renderizar detalhes no modal
 *   - mostrar/ocultar modais
 *   - exibir toasts de estado
 *   - mostrar estados de vazio e loading
 */

// ── Utilitários ───────────────────────────────────────────────────────────────

/** Formata data ISO 8601 para DD/MM/AAAA HH:MM */
function formatDate(iso) {
  if (!iso) return "—";
  const d = new Date(iso);
  if (isNaN(d)) return iso;
  const pad = (n) => String(n).padStart(2, "0");
  return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

/** Retorna classe CSS da nota (score-high / score-mid / score-low / score-null) */
function scoreClass(score) {
  if (score === null || score === undefined) return "score-null";
  if (score >= 8) return "score-high";
  if (score >= 5) return "score-mid";
  return "score-low";
}

/** Formata a nota para exibição */
function formatScore(score) {
  if (score === null || score === undefined) return "—";
  return `${score.toFixed(1)}/10`;
}

/** Formata status para exibição */
function formatStatus(status) {
  const map = { completed: "Concluída", error: "Erro", pending: "Pendente" };
  return map[status] || status;
}

/** Retorna classe CSS do status */
function statusClass(status) {
  const map = { completed: "status-completed", error: "status-error", pending: "status-pending" };
  return map[status] || "status-pending";
}

/** Escapa HTML para evitar XSS ao inserir texto como innerHTML */
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Toast ──────────────────────────────────────────────────────────────────────

let toastTimer = null;

/**
 * Exibe uma notificação flutuante.
 * @param {string} message
 * @param {'success'|'error'|'info'} type
 */
function showToast(message, type = "info") {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = `toast toast-${type} toast-visible`;
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove("toast-visible");
  }, 4000);
}

// ── Loading ────────────────────────────────────────────────────────────────────

function showListLoading() {
  const list = document.getElementById("analyses-list");
  list.innerHTML = '<p class="state-message">Carregando análises...</p>';
}

function showListEmpty() {
  const list = document.getElementById("analyses-list");
  list.innerHTML =
    '<p class="state-message state-empty">Nenhuma análise cadastrada. Crie a primeira acima.</p>';
}

function showListError(msg) {
  const list = document.getElementById("analyses-list");
  list.innerHTML = `<p class="state-message state-error">Erro ao carregar: ${escapeHtml(msg)}</p>`;
}

// ── Cards de análise ───────────────────────────────────────────────────────────

/**
 * Renderiza a lista de análises no DOM.
 * @param {Array} analyses
 * @param {Object} handlers - { onDetail, onEdit, onRerun, onDelete }
 */
function renderAnalysisList(analyses, handlers) {
  const list = document.getElementById("analyses-list");
  if (!analyses || analyses.length === 0) {
    showListEmpty();
    return;
  }
  list.innerHTML = analyses.map((a) => buildCard(a)).join("");
  attachCardHandlers(analyses, handlers);
}

function buildCard(a) {
  const scoreHtml = `<span class="badge ${scoreClass(a.score)}">${formatScore(a.score)}</span>`;
  const statusHtml = `<span class="badge ${statusClass(a.status)}">${formatStatus(a.status)}</span>`;

  return `
  <article class="analysis-card" data-id="${a.id}">
    <div class="card-header">
      <div class="card-title-row">
        <h3 class="card-title">${escapeHtml(a.name)}</h3>
        <div class="card-badges">${scoreHtml}${statusHtml}</div>
      </div>
      ${a.description ? `<p class="card-description">${escapeHtml(a.description)}</p>` : ""}
    </div>
    <div class="card-body">
      <p class="card-path"><span class="label">Pasta:</span> <code>${escapeHtml(a.target_path)}</code></p>
      <p class="card-date"><span class="label">Criada em:</span> ${formatDate(a.created_at)}</p>
      ${a.updated_at !== a.created_at ? `<p class="card-date"><span class="label">Atualizada em:</span> ${formatDate(a.updated_at)}</p>` : ""}
    </div>
    <div class="card-actions">
      <button class="btn btn-secondary btn-detail" data-id="${a.id}">Detalhes</button>
      <button class="btn btn-secondary btn-edit" data-id="${a.id}">Editar</button>
      <button class="btn btn-warning btn-rerun" data-id="${a.id}">Reexecutar</button>
      <button class="btn btn-danger btn-delete" data-id="${a.id}">Excluir</button>
    </div>
  </article>`;
}

function attachCardHandlers(analyses, handlers) {
  document.querySelectorAll(".btn-detail").forEach((btn) =>
    btn.addEventListener("click", () => handlers.onDetail(Number(btn.dataset.id)))
  );
  document.querySelectorAll(".btn-edit").forEach((btn) =>
    btn.addEventListener("click", () => {
      const a = analyses.find((x) => x.id === Number(btn.dataset.id));
      handlers.onEdit(a);
    })
  );
  document.querySelectorAll(".btn-rerun").forEach((btn) =>
    btn.addEventListener("click", () => handlers.onRerun(Number(btn.dataset.id), btn))
  );
  document.querySelectorAll(".btn-delete").forEach((btn) =>
    btn.addEventListener("click", () => handlers.onDelete(Number(btn.dataset.id)))
  );
}

/** Atualiza apenas o card de uma análise específica na lista */
function updateCardInList(analysis, handlers) {
  const existing = document.querySelector(`.analysis-card[data-id="${analysis.id}"]`);
  if (!existing) return;
  existing.outerHTML = buildCard(analysis);
  attachCardHandlers([analysis], handlers);
}

/** Remove o card de uma análise da lista */
function removeCardFromList(id) {
  const card = document.querySelector(`.analysis-card[data-id="${id}"]`);
  if (card) card.remove();
  const list = document.getElementById("analyses-list");
  if (!list.querySelector(".analysis-card")) showListEmpty();
}

/** Prepend (adiciona ao topo) um novo card */
function prependCard(analysis, handlers) {
  const list = document.getElementById("analyses-list");
  const empty = list.querySelector(".state-message");
  if (empty) empty.remove();
  const temp = document.createElement("div");
  temp.innerHTML = buildCard(analysis);
  const card = temp.firstElementChild;
  list.prepend(card);
  attachCardHandlers([analysis], handlers);
}

// ── Modal de Detalhes ──────────────────────────────────────────────────────────

function openDetailModal(analysis) {
  const modal = document.getElementById("modal-detail");
  const content = document.getElementById("detail-content");

  const s = analysis.summary || {};

  // ── Cabeçalho: dados gerais ──────────────────────────────────────────────
  const headerHtml = `
    <div class="detail-grid">
      <div class="detail-group">
        <span class="detail-label">Nome</span>
        <span class="detail-value">${escapeHtml(analysis.name)}</span>
      </div>
      ${analysis.description ? `
      <div class="detail-group">
        <span class="detail-label">Descrição</span>
        <span class="detail-value">${escapeHtml(analysis.description)}</span>
      </div>` : ""}
      <div class="detail-group">
        <span class="detail-label">Pasta analisada</span>
        <code class="detail-value detail-code">${escapeHtml(analysis.target_path)}</code>
      </div>
      <div class="detail-group">
        <span class="detail-label">Nota</span>
        <span class="badge ${scoreClass(analysis.score)} badge-lg">${formatScore(analysis.score)}</span>
      </div>
      <div class="detail-group">
        <span class="detail-label">Status</span>
        <span class="badge ${statusClass(analysis.status)}">${formatStatus(analysis.status)}</span>
      </div>
      ${analysis.report_path ? `
      <div class="detail-group">
        <span class="detail-label">Relatório gerado</span>
        <code class="detail-value detail-code">${escapeHtml(analysis.report_path)}</code>
      </div>` : ""}
      <div class="detail-group">
        <span class="detail-label">Criada em</span>
        <span class="detail-value">${formatDate(analysis.created_at)}</span>
      </div>
      <div class="detail-group">
        <span class="detail-label">Atualizada em</span>
        <span class="detail-value">${formatDate(analysis.updated_at)}</span>
      </div>
    </div>`;

  // ── Resumo: totais ───────────────────────────────────────────────────────
  const resumoHtml = (s.total_files !== undefined) ? `
    <div class="detail-section">
      <h4 class="detail-section-title">Resumo</h4>
      <div class="summary-stats">
        <div class="stat-item"><span class="stat-num">${s.total_files}</span><span class="stat-label">arquivos</span></div>
        <div class="stat-item"><span class="stat-num">${s.total_dirs}</span><span class="stat-label">pastas</span></div>
      </div>
    </div>` : "";

  // ── Categorias de problemas com listas de arquivos ───────────────────────
  const categorias = [
    { label: "Arquivos soltos",                lista: s.lista_arquivos_soltos,           count: s.loose_files },
    { label: "Arquivos vazios",                lista: s.lista_arquivos_vazios,           count: s.empty_files },
    { label: "Pastas vazias",                  lista: s.lista_pastas_vazias,             count: s.empty_dirs },
    { label: "Fora do padrão de nome",         lista: s.lista_fora_do_padrao,            count: s.invalid_pattern },
    { label: "Nomes genéricos",                lista: s.lista_nomes_genericos,           count: s.generic_names },
    { label: "Separadores inconsistentes",     lista: s.lista_separadores_inconsistentes,count: s.mixed_separators },
    { label: "Sem timestamp",                  lista: s.lista_sem_timestamp,             count: s.missing_timestamps },
    { label: "Timestamp inválido",             lista: s.lista_timestamp_invalido,        count: s.invalid_timestamps },
    { label: "Ordem incoerente",               lista: s.lista_ordem_incoerente,          count: s.order_issues },
  ];

  const problemasHtml = categorias
    .filter((c) => c.count !== undefined)
    .map((c) => {
      const hasIssue = c.count > 0;
      const itensHtml = (hasIssue && Array.isArray(c.lista) && c.lista.length > 0)
        ? `<ul class="problem-file-list">${c.lista.map((f) => `<li><code>${escapeHtml(f)}</code></li>`).join("")}</ul>`
        : "";
      return `
        <div class="problem-category ${hasIssue ? "has-issue" : "no-issue"}">
          <div class="problem-category-header">
            <span class="problem-label">${c.label}</span>
            <span class="problem-count">${c.count}</span>
          </div>
          ${itensHtml}
        </div>`;
    })
    .join("");

  const problemasSection = problemasHtml ? `
    <div class="detail-section">
      <h4 class="detail-section-title">Problemas encontrados</h4>
      <div class="problems-list">${problemasHtml}</div>
    </div>` : "";

  // ── Pontuação por critério (chave portuguesa nova + fallback na antiga) ───
  const pontuacao = s.pontuacao_por_criterio || {};
  const breakdownEntries = Object.entries(pontuacao);

  const pontuacaoHtml = breakdownEntries.length > 0 ? `
    <div class="detail-section">
      <h4 class="detail-section-title">Pontuação por critério</h4>
      <div class="breakdown-grid">
        ${breakdownEntries.map(([key, val]) => `
          <div class="breakdown-row">
            <span>${escapeHtml(key)}</span>
            <span>${val}</span>
          </div>`).join("")}
      </div>
    </div>` : "";

  content.innerHTML = headerHtml + resumoHtml + problemasSection + pontuacaoHtml;

  modal.classList.add("open");
}

function closeDetailModal() {
  document.getElementById("modal-detail").classList.remove("open");
}

// ── Modal de Edição ────────────────────────────────────────────────────────────

function openEditModal(analysis) {
  document.getElementById("edit-id").value = analysis.id;
  document.getElementById("edit-name").value = analysis.name || "";
  document.getElementById("edit-description").value = analysis.description || "";
  document.getElementById("edit-path").value = analysis.target_path || "";
  document.getElementById("modal-edit").classList.add("open");
  document.getElementById("edit-name").focus();
}

function closeEditModal() {
  document.getElementById("modal-edit").classList.remove("open");
}

// ── Formulário de criação ──────────────────────────────────────────────────────

function setFormLoading(loading) {
  const btn = document.getElementById("btn-create");
  btn.disabled = loading;
  btn.textContent = loading ? "Analisando..." : "Analisar";
}

function clearCreateForm() {
  document.getElementById("create-name").value = "";
  document.getElementById("create-description").value = "";
  document.getElementById("create-path").value = "";
}

function setEditLoading(loading) {
  const btn = document.getElementById("btn-save-edit");
  btn.disabled = loading;
  btn.textContent = loading ? "Salvando..." : "Salvar";
}

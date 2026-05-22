"""
Local review app for manually correcting Phase 2 label 0 normalization rows.

The app edits the label 0 full-normalization working CSV directly. It defaults
to rows marked needs_review, then saves manual corrections back to
normalized_text, manual_status, review_note, validation_status, and updated_at.

Run from repository root:
    python scripts/data_pipeline/review_phase2_normalization_app.py

Open:
    http://127.0.0.1:8765
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from build_phase2_full_normalization_dataset_label0 import validate_normalization


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
NORMALIZATION_DIR = DATA_DIR / "normalization"
DEFAULT_WORKING = NORMALIZATION_DIR / "phase2_full_normalization_working.csv"

BASE_COLUMNS = [
    "norm_id",
    "source_text",
    "normalized_text",
    "task_type",
    "label",
    "category",
    "has_url",
    "has_phone_number",
    "sender_type",
    "obfuscation_level",
    "data_origin",
    "source_sample_id",
    "source_dataset",
    "source_row_id",
]
REVIEW_COLUMNS = [
    "generated_normalized_text",
    "validation_status",
    "validation_issues",
    "manual_status",
    "review_note",
    "updated_at",
]
ALL_COLUMNS = BASE_COLUMNS + REVIEW_COLUMNS

VIETNAMESE_ACCENT_RE = re.compile(
    r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡ"
    r"ùúụủũưừứựửữỳýỵỷỹđ"
    r"ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ"
    r"ÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]"
)
TOKEN_RE = re.compile(
    r"(?:[Hh][Tt][Tt][Pp][Ss]?://|[Ww][Ww][Ww]\.)\S+"
    r"|\b[A-Za-z0-9][A-Za-z0-9-]*(?:\.[A-Za-z0-9][A-Za-z0-9-]*)+\b"
    r"|(?:\+?84|0)(?:[\s.-]?\d){8,10}"
    r"|\b(?:1800|1900)(?:[\s.-]?\d){4,6}\b"
    r"|\b[A-Z0-9]{4,}\b"
    r"|\b\d[\d.,]{2,}\s?(?:VND|VNĐ|d|đ|k)?\b"
)


HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Phase 2 Label 0 Normalization Review</title>
  <style>
    :root {
      --bg: #f6f7f9;
      --panel: #ffffff;
      --line: #d8dde6;
      --text: #1f2937;
      --muted: #64748b;
      --accent: #0f766e;
      --danger: #b42318;
      --warn: #a15c00;
      --soft: #eef6f5;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font: 14px/1.45 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 12px 18px;
      background: var(--panel);
      border-bottom: 1px solid var(--line);
      position: sticky;
      top: 0;
      z-index: 3;
    }
    h1 {
      font-size: 16px;
      margin: 0;
      letter-spacing: 0;
    }
    main {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 300px;
      gap: 14px;
      padding: 14px;
      max-width: 1500px;
      margin: 0 auto;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }
    .workspace {
      display: grid;
      grid-template-rows: auto auto 1fr auto;
      min-height: calc(100vh - 92px);
    }
    .bar, .meta, .actions, .side-section {
      padding: 12px;
      border-bottom: 1px solid var(--line);
    }
    .bar {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      justify-content: space-between;
    }
    .bar-group {
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }
    input, select, textarea, button {
      font: inherit;
    }
    input, select {
      height: 34px;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 0 10px;
      background: #fff;
      color: var(--text);
    }
    input[type="number"] {
      width: 88px;
    }
    button {
      height: 34px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--text);
      padding: 0 12px;
      cursor: pointer;
    }
    button.primary {
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }
    button:disabled {
      color: #94a3b8;
      cursor: not-allowed;
    }
    .meta {
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 8px;
      color: var(--muted);
      font-size: 13px;
    }
    .meta strong {
      display: block;
      color: var(--text);
      font-weight: 600;
      overflow-wrap: anywhere;
    }
    .editors {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      padding: 12px;
      min-height: 420px;
    }
    .editor {
      display: grid;
      grid-template-rows: auto 1fr;
      gap: 8px;
      min-width: 0;
    }
    .editor label {
      color: var(--muted);
      font-weight: 600;
    }
    textarea {
      width: 100%;
      min-height: 380px;
      resize: vertical;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      color: var(--text);
      background: #fff;
      line-height: 1.55;
    }

    .actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      border-bottom: 0;
    }
    .status {
      min-height: 20px;
      color: var(--muted);
    }
    .status.warn { color: var(--warn); }
    .status.error { color: var(--danger); }
    aside {
      min-height: calc(100vh - 92px);
    }
    .side-section:last-child {
      border-bottom: 0;
    }
    .side-title {
      margin: 0 0 8px;
      font-size: 13px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: .04em;
    }
    .stats {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }
    .stat {
      background: var(--soft);
      border-radius: 6px;
      padding: 8px;
    }
    .stat strong {
      display: block;
      font-size: 18px;
    }
    .tokens {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .token {
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 3px 8px;
      background: #fff;
      overflow-wrap: anywhere;
      max-width: 100%;
    }
    .shortcuts {
      color: var(--muted);
      display: grid;
      gap: 6px;
    }
    .shortcuts code {
      color: var(--text);
      background: #f1f5f9;
      padding: 1px 5px;
      border-radius: 4px;
    }
    @media (max-width: 980px) {
      main { grid-template-columns: 1fr; }
      .editors { grid-template-columns: 1fr; }
      .meta { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
  </style>
</head>
<body>
  <header>
    <h1>Phase 2 Label 0 SMS Normalization Review</h1>
    <div id="saveState" class="status">Loading...</div>
  </header>
  <main>
    <section class="panel workspace">
      <div class="bar">
        <div class="bar-group">
          <button id="prevBtn">Prev</button>
          <button id="nextBtn">Next</button>
          <span id="position">0 / 0</span>
          <input id="jumpInput" type="number" min="1" value="1">
          <button id="jumpBtn">Go</button>
        </div>
        <div class="bar-group">
          <input id="queryInput" type="search" placeholder="Search source, target, category...">
          <select id="filterSelect">
            <option value="needs_review">Needs review</option>
            <option value="warning">Warning</option>
            <option value="all">All</option>
            <option value="pending">Pending</option>
            <option value="generated">Generated</option>
            <option value="manual_reviewed">Manual reviewed</option>
          </select>
        </div>
      </div>
      <div class="meta" id="meta"></div>
      <div class="editors">
        <div class="editor">
          <label for="sourceText">Source SMS</label>
          <textarea id="sourceText"></textarea>
        </div>
        <div class="editor">
          <label for="targetText">Normalized text</label>
          <textarea id="targetText"></textarea>
        </div>
      </div>
      <div class="actions">
        <div class="bar-group">
          <select id="statusSelect">
            <option value="needs_review">Needs review</option>
            <option value="manual_reviewed">Manual reviewed</option>
            <option value="generated">Generated</option>
            <option value="pending">Pending</option>
          </select>
          <button id="copySourceBtn">Copy source &rarr; target</button>
          <button id="resetBtn">Reset to generated</button>
        </div>
        <div class="bar-group">
          <button id="saveBtn" class="primary">Save</button>
          <button id="saveNextBtn">Save & Next</button>
        </div>
      </div>
    </section>
    <aside class="panel">
      <div class="side-section">
        <p class="side-title">Progress</p>
        <div class="stats" id="stats"></div>
      </div>
      <div class="side-section">
        <p class="side-title">Tokens to preserve</p>
        <div class="tokens" id="tokens"></div>
      </div>
      <div class="side-section">
        <p class="side-title">Review note</p>
        <textarea id="noteText" style="min-height: 110px"></textarea>
      </div>
      <div class="side-section">
        <p class="side-title">Shortcuts</p>
        <div class="shortcuts">
          <div><code>Ctrl+S</code> Save</div>
          <div><code>Ctrl+Enter</code> Save & Next</div>
          <div><code>Alt++</code> Next</div>
          <div><code>Alt+-</code> Prev</div>
          <div><code>Alt+G</code> Mark reviewed</div>
        </div>
      </div>
    </aside>
  </main>
<script>
let state = {
  row: null,
  index: 0,
  filteredTotal: 0,
  total: 0,
  summary: {},
  dirty: false,
};

const el = (id) => document.getElementById(id);

function setStatus(text, kind = "") {
  const node = el("saveState");
  node.textContent = text;
  node.className = "status " + kind;
}

function currentFilter() {
  return {
    filter: el("filterSelect").value,
    q: el("queryInput").value.trim(),
  };
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok || payload.error) {
    throw new Error(payload.error || "Request failed");
  }
  return payload;
}

function renderStats(summary) {
  const stats = [
    ["Total", summary.total],
    ["Pending", summary.pending],
    ["Needs review", summary.needs_review],
    ["Manual", summary.manual_reviewed],
    ["Generated", summary.generated],
  ];
  el("stats").innerHTML = stats.map(([label, value]) =>
    `<div class="stat"><span>${label}</span><strong>${value}</strong></div>`
  ).join("");
}

function renderRow(payload) {
  state.row = payload.row;
  state.index = payload.index;
  state.filteredTotal = payload.filtered_total;
  state.total = payload.total;
  state.summary = payload.summary;
  state.dirty = false;

  const row = payload.row;
  el("position").textContent = `${payload.filtered_position} / ${payload.filtered_total}`;
  el("jumpInput").value = payload.filtered_position || 1;
  el("sourceText").value = row.source_text || "";
  el("targetText").value = row.normalized_text || "";
  el("statusSelect").value = row.manual_status || "needs_review";
  el("noteText").value = row.review_note || "";
  el("prevBtn").disabled = payload.filtered_position <= 1;
  el("nextBtn").disabled = payload.filtered_position >= payload.filtered_total;

  el("meta").innerHTML = [
    ["ID", row.norm_id],
    ["Label", row.label],
    ["Validation", row.validation_status],
    ["Issues", row.validation_issues],
    ["Origin", row.data_origin],
    ["Obfuscation", row.obfuscation_level],
  ].map(([k, v]) => `<div>${k}<strong>${v}</strong></div>`).join("");

  el("tokens").innerHTML = (payload.tokens || []).length
    ? payload.tokens.map(t => `<span class="token">${escapeHtml(t)}</span>`).join("")
    : `<span class="status">No obvious protected tokens.</span>`;

  renderStats(payload.summary);
  setStatus("Loaded");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  }[ch]));
}

async function loadRow(position = 1) {
  if (state.dirty && !confirm("You have unsaved edits. Leave this row?")) return;
  const params = new URLSearchParams({ position, ...currentFilter() });
  setStatus("Loading...");
  renderRow(await api(`/api/row?${params.toString()}`));
}

async function move(delta) {
  await loadRow(Math.max(1, Number(el("jumpInput").value || 1) + delta));
}

async function save(moveNext = false) {
  if (!state.row) return;
  if (moveNext) el("statusSelect").value = "manual_reviewed";
  setStatus("Saving...");
  const payload = await api("/api/save", {
    method: "POST",
    body: JSON.stringify({
      norm_id: state.row.norm_id,
      normalized_text: el("targetText").value,
      manual_status: el("statusSelect").value,
      review_note: el("noteText").value,
    }),
  });
  state.dirty = false;
  renderStats(payload.summary);
  if (payload.warnings.length) {
    setStatus(payload.warnings.join(" "), "warn");
  } else {
    setStatus("Saved");
  }
  if (moveNext) await move(1);
}

function markDirty() {
  state.dirty = true;
  setStatus("Unsaved edits", "warn");
}

el("targetText").addEventListener("input", markDirty);
el("noteText").addEventListener("input", markDirty);
el("statusSelect").addEventListener("change", markDirty);
el("prevBtn").addEventListener("click", () => move(-1));
el("nextBtn").addEventListener("click", () => move(1));
el("jumpBtn").addEventListener("click", () => loadRow(Number(el("jumpInput").value || 1)));
el("saveBtn").addEventListener("click", () => save(false));
el("saveNextBtn").addEventListener("click", () => save(true));
el("filterSelect").addEventListener("change", () => loadRow(1));
el("queryInput").addEventListener("keydown", (event) => {
  if (event.key === "Enter") loadRow(1);
});
el("copySourceBtn").addEventListener("click", () => {
  el("targetText").value = el("sourceText").value;
  markDirty();
});
el("resetBtn").addEventListener("click", async () => {
  if (!state.row) return;
  el("targetText").value = state.row.generated_normalized_text || state.row.normalized_text || "";
  markDirty();
});

document.addEventListener("keydown", async (event) => {
  // Skip global shortcuts when focus is in the search box or jump input,
  // but still allow them from the review textareas and the rest of the page.
  const active = document.activeElement;
  const isSearchOrJump = active === el("queryInput") || active === el("jumpInput");
  if (isSearchOrJump) return;

  const ctrl = event.ctrlKey || event.metaKey;

  // Ctrl+S — Save
  if (ctrl && event.code === "KeyS") {
    event.preventDefault();
    await save(false);
  // Ctrl+Enter — Save & Next
  } else if (ctrl && event.code === "Enter") {
    event.preventDefault();
    await save(true);
  // Alt+= or Alt++ — Next  (event.code is layout-independent)
  } else if (event.altKey && (event.code === "Equal" || event.code === "NumpadAdd")) {
    event.preventDefault();
    await move(1);
  // Alt+- or Alt+_ — Prev
  } else if (event.altKey && (event.code === "Minus" || event.code === "NumpadSubtract")) {
    event.preventDefault();
    await move(-1);
  // Alt+G — Mark manual reviewed & save
  } else if (event.altKey && event.code === "KeyG") {
    event.preventDefault();
    el("statusSelect").value = "manual_reviewed";
    markDirty();
    await save(false);
  }
});

window.addEventListener("beforeunload", (event) => {
  if (!state.dirty) return;
  event.preventDefault();
  event.returnValue = "";
});

loadRow(1).catch(error => setStatus(error.message, "error"));
</script>
</body>
</html>
"""


class ReviewStore:
    def __init__(self, working_path: Path) -> None:
        self.working_path = working_path
        self.rows: list[dict[str, str]] = []
        self.by_norm_id: dict[str, int] = {}
        self.load()

    def load(self) -> None:
        if not self.working_path.exists():
            raise FileNotFoundError(f"Missing working CSV: {self.working_path}")
        NORMALIZATION_DIR.mkdir(parents=True, exist_ok=True)
        self.rows = self._read_rows(self.working_path)
        self.by_norm_id = {row["norm_id"]: idx for idx, row in enumerate(self.rows)}

    def _read_rows(self, path: Path) -> list[dict[str, str]]:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError(f"{path} has no header row")
            missing = [column for column in BASE_COLUMNS if column not in reader.fieldnames]
            if missing:
                raise ValueError(f"{path} is missing columns: {', '.join(missing)}")
            rows = []
            for row in reader:
                clean = {column: row.get(column, "") for column in BASE_COLUMNS}
                clean["manual_status"] = row.get("manual_status") or "pending"
                clean["review_note"] = row.get("review_note") or ""
                clean["updated_at"] = row.get("updated_at") or ""
                clean["generated_normalized_text"] = (
                    row.get("generated_normalized_text") or row.get("normalized_text", "")
                )
                clean["validation_status"] = row.get("validation_status") or "pending"
                clean["validation_issues"] = row.get("validation_issues") or ""
                rows.append(clean)
            return rows

    def _write_rows(self, rows: list[dict[str, str]] | None = None) -> None:
        rows = self.rows if rows is None else rows
        tmp_path = self.working_path.with_suffix(".tmp")
        with tmp_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=ALL_COLUMNS)
            writer.writeheader()
            for row in rows:
                writer.writerow({column: row.get(column, "") for column in ALL_COLUMNS})
        tmp_path.replace(self.working_path)

    def summary(self) -> dict[str, int]:
        counts = {
            "total": len(self.rows),
            "pending": 0,
            "generated": 0,
            "needs_review": 0,
            "manual_reviewed": 0,
        }
        for row in self.rows:
            status = row.get("manual_status") or "pending"
            counts[status] = counts.get(status, 0) + 1
        return counts

    def filtered_indices(self, status_filter: str, query: str) -> list[int]:
        query_norm = query.strip().lower()
        indices = []
        for idx, row in enumerate(self.rows):
            status = row.get("manual_status") or "pending"
            validation_status = row.get("validation_status") or "pending"
            if status_filter == "warning":
                if validation_status != "warning":
                    continue
            elif status_filter != "all" and status != status_filter:
                continue
            if query_norm:
                haystack = " ".join(
                    [
                        row.get("source_text", ""),
                        row.get("normalized_text", ""),
                        row.get("category", ""),
                        row.get("norm_id", ""),
                        row.get("source_dataset", ""),
                        row.get("validation_issues", ""),
                    ]
                ).lower()
                if query_norm not in haystack:
                    continue
            indices.append(idx)
        return indices

    def get_row_payload(self, position: int, status_filter: str, query: str) -> dict[str, object]:
        indices = self.filtered_indices(status_filter, query)
        if not indices:
            raise ValueError("No rows match the current filter.")
        position = min(max(position, 1), len(indices))
        row_idx = indices[position - 1]
        row = dict(self.rows[row_idx])
        tokens = sorted({token.strip() for token in TOKEN_RE.findall(row.get("source_text", "")) if token.strip()})
        return {
            "row": row,
            "index": row_idx,
            "filtered_position": position,
            "filtered_total": len(indices),
            "total": len(self.rows),
            "summary": self.summary(),
            "tokens": tokens[:30],
        }

    def save_row(self, norm_id: str, normalized_text: str, manual_status: str, review_note: str) -> dict[str, object]:
        if norm_id not in self.by_norm_id:
            raise ValueError(f"Unknown norm_id: {norm_id}")
        if manual_status not in {"pending", "generated", "needs_review", "manual_reviewed"}:
            raise ValueError(f"Invalid manual_status: {manual_status}")
        normalized_text = normalized_text.strip()
        row = self.rows[self.by_norm_id[norm_id]]
        validation_status, issues = validate_normalization(row.get("source_text", ""), normalized_text)
        row["normalized_text"] = normalized_text
        if not row.get("generated_normalized_text"):
            row["generated_normalized_text"] = normalized_text
        row["validation_status"] = "manual_pass" if manual_status == "manual_reviewed" else validation_status
        row["validation_issues"] = "" if manual_status == "manual_reviewed" else ";".join(issues)
        row["manual_status"] = manual_status
        row["review_note"] = review_note.strip()
        row["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._write_rows()
        return {"summary": self.summary(), "warnings": self.validation_warnings(row)}

    @staticmethod
    def validation_warnings(row: dict[str, str]) -> list[str]:
        warnings = []
        target = row.get("normalized_text", "")
        if not target:
            warnings.append("Normalized text is empty.")
        if target == row.get("source_text", ""):
            warnings.append("Normalized text matches source.")
        if row.get("manual_status") == "manual_reviewed" and not VIETNAMESE_ACCENT_RE.search(target):
            warnings.append("Manual reviewed text has no Vietnamese accents.")
        return warnings


def json_response(handler: BaseHTTPRequestHandler, payload: dict[str, object], status: int = 200) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def make_handler(store: ReviewStore) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            try:
                if parsed.path == "/":
                    body = HTML.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                if parsed.path == "/api/row":
                    params = parse_qs(parsed.query)
                    position = int(params.get("position", ["1"])[0])
                    status_filter = params.get("filter", ["all"])[0]
                    query = params.get("q", [""])[0]
                    json_response(self, store.get_row_payload(position, status_filter, query))
                    return
                if parsed.path == "/api/summary":
                    json_response(self, store.summary())
                    return
                json_response(self, {"error": "Not found"}, 404)
            except Exception as exc:
                json_response(self, {"error": str(exc)}, 400)

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            try:
                if parsed.path != "/api/save":
                    json_response(self, {"error": "Not found"}, 404)
                    return
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                result = store.save_row(
                    norm_id=str(payload.get("norm_id", "")),
                    normalized_text=str(payload.get("normalized_text", "")),
                    manual_status=str(payload.get("manual_status", "pending")),
                    review_note=str(payload.get("review_note", "")),
                )
                json_response(self, result)
            except Exception as exc:
                json_response(self, {"error": str(exc)}, 400)

        def log_message(self, format: str, *args: object) -> None:
            return

    return Handler


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review Phase 2 label 0 full-normalization rows.")
    parser.add_argument("--working", type=Path, default=DEFAULT_WORKING, help="Working CSV to update.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind.")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    store = ReviewStore(args.working)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(store))
    print(f"Review app: http://{args.host}:{args.port}")
    print(f"Working CSV: {args.working}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    main()

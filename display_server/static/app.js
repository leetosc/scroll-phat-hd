let modes = [];
let state = { mode: null, config: {}, error: null };

const modeSelect = document.getElementById("mode-select");
const configForm = document.getElementById("config-form");
const banner = document.getElementById("banner");
const modeNote = document.getElementById("mode-note");
const activeMode = document.getElementById("active-mode");

async function fetchJson(url, options) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

function currentModeMeta() {
  return modes.find((m) => m.id === state.mode);
}

function listToText(value, field) {
  if (Array.isArray(value)) {
    return field?.type === "int_list" ? value.join(" ") : value.join("\n");
  }
  return String(value ?? "");
}

function coerceValue(field, raw) {
  if (field.type === "bool") return raw === "true" || raw === true;
  if (field.type === "int") return parseInt(raw, 10);
  if (field.type === "float") return parseFloat(raw);
  if (field.type === "list" || field.type === "int_list") {
    const parts =
      field.type === "int_list"
        ? String(raw).trim().split(/[\s,]+/).filter(Boolean)
        : String(raw)
            .split("\n")
            .map((line) => line.trim())
            .filter(Boolean);
    if (field.type === "int_list") {
      return parts.map((x) => parseInt(x, 10));
    }
    return parts;
  }
  return raw;
}

function buildConfigForm() {
  const meta = currentModeMeta();
  configForm.innerHTML = "";
  if (!meta || !meta.schema.length) {
    configForm.innerHTML = "<p class='hint'>No tunable parameters for this mode.</p>";
    return;
  }

  for (const field of meta.schema) {
    const wrap = document.createElement("div");
    wrap.className = "field";
    const label = document.createElement("label");
    label.textContent = field.name;
    label.htmlFor = "cfg-" + field.name;
    wrap.appendChild(label);

    const value = state.config[field.name] ?? field.default;

    if (field.type === "bool") {
      const input = document.createElement("input");
      input.type = "checkbox";
      input.id = "cfg-" + field.name;
      input.name = field.name;
      input.checked = Boolean(value);
      wrap.appendChild(input);
    } else if (field.type === "list" || field.type === "int_list") {
      const input = document.createElement("textarea");
      input.id = "cfg-" + field.name;
      input.name = field.name;
      const text = listToText(value, field);
      input.rows = Math.min(8, Math.max(3, text.split("\n").length + 1));
      input.value = text;
      wrap.appendChild(input);
      if (field.type === "int_list") {
        const hint = document.createElement("p");
        hint.className = "hint";
        hint.textContent = "Space-separated integers";
        wrap.appendChild(hint);
      }
    } else if (field.type === "str" && field.widget === "textarea") {
      const input = document.createElement("textarea");
      input.id = "cfg-" + field.name;
      input.name = field.name;
      const text = Array.isArray(value) ? value.join("\n") : String(value ?? "");
      input.rows = Math.min(10, Math.max(4, text.split("\n").length + 1));
      input.value = text;
      wrap.appendChild(input);
      if (field.name === "LINES") {
        const hint = document.createElement("p");
        hint.className = "hint";
        hint.textContent = "One line of text per row";
        wrap.appendChild(hint);
      }
    } else if (field.type === "float" && field.min !== undefined) {
      const input = document.createElement("input");
      input.type = "range";
      input.id = "cfg-" + field.name;
      input.name = field.name;
      input.min = field.min;
      input.max = field.max;
      input.step = field.step || 0.01;
      input.value = value;
      const valSpan = document.createElement("span");
      valSpan.className = "range-value";
      valSpan.textContent = Number(value).toFixed(2);
      input.addEventListener("input", () => {
        valSpan.textContent = Number(input.value).toFixed(2);
      });
      wrap.appendChild(input);
      wrap.appendChild(valSpan);
    } else {
      const input = document.createElement("input");
      input.type = field.type === "secret" ? "password" : "number";
      if (field.type === "str" || field.type === "secret") input.type = "text";
      input.id = "cfg-" + field.name;
      input.name = field.name;
      input.value = value;
      if (field.type === "float") {
        input.step = field.step || "any";
      } else if (field.step) {
        input.step = field.step;
      }
      wrap.appendChild(input);
    }

    configForm.appendChild(wrap);
  }
}

/** Update status/error only — never rebuilds the settings form. */
function updateStatus() {
  activeMode.textContent = state.mode || "—";

  if (state.mode && modeSelect.value !== state.mode) {
    modeSelect.value = state.mode;
  }

  const meta = currentModeMeta();
  if (meta && meta.note) {
    modeNote.textContent = meta.note;
    if (meta.requires_deps && meta.requires_deps.length) {
      modeNote.textContent += " (requires: " + meta.requires_deps.join(", ") + ")";
    }
  } else if (meta && meta.requires_deps && meta.requires_deps.length) {
    modeNote.textContent = "Requires: " + meta.requires_deps.join(", ");
  } else {
    modeNote.textContent = "";
  }

  if (state.error) {
    banner.textContent = state.error;
    banner.classList.remove("hidden");
  } else {
    banner.classList.add("hidden");
  }
}

/** Full UI refresh including rebuilding the settings form. */
function updateUI() {
  updateStatus();
  buildConfigForm();
}

async function refreshStatus() {
  state = await fetchJson("/api/state");
  updateStatus();
}

async function loadModes() {
  const data = await fetchJson("/api/modes");
  modes = data.modes;
  modeSelect.innerHTML = modes
    .map((m) => `<option value="${m.id}">${m.label}</option>`)
    .join("");
}

document.getElementById("btn-switch").addEventListener("click", async () => {
  const mode = modeSelect.value;
  state = await fetchJson("/api/mode", {
    method: "POST",
    body: JSON.stringify({ mode }),
  });
  updateUI();
});

configForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const meta = currentModeMeta();
  if (!meta) return;

  const payload = {};
  for (const field of meta.schema) {
    const el = configForm.elements.namedItem(field.name);
    if (!el) continue;
    if (field.type === "bool") {
      payload[field.name] = el.checked;
    } else {
      payload[field.name] = coerceValue(field, el.value);
    }
  }

  state = await fetchJson("/api/config", {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
  updateUI();
});

document.getElementById("btn-reset").addEventListener("click", async () => {
  state = await fetchJson("/api/reset", { method: "POST" });
  updateUI();
});

async function init() {
  await loadModes();
  state = await fetchJson("/api/state");
  updateUI();
  setInterval(refreshStatus, 5000);
}

init().catch((err) => {
  banner.textContent = err.message;
  banner.classList.remove("hidden");
});

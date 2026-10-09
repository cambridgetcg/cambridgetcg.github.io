const $ = (sel) => document.querySelector(sel);

const state = {
  worker: null,
  volunteerId: localStorage.getItem("castle-grid-volunteer-id") || crypto.randomUUID(),
  running: false,
  units: [],
  results: []
};
localStorage.setItem("castle-grid-volunteer-id", state.volunteerId);

function log(message, kind = "info") {
  const line = document.createElement("div");
  line.className = `log-line ${kind}`;
  line.textContent = `${new Date().toLocaleTimeString()} · ${message}`;
  $("#log").prepend(line);
}

function setStatus(text, cls = "idle") {
  const el = $("#status");
  el.textContent = text;
  el.className = `pill ${cls}`;
}

function userAgentFamily() {
  const ua = navigator.userAgent || "unknown";
  if (ua.includes("Firefox")) return "Firefox";
  if (ua.includes("Edg/")) return "Edge";
  if (ua.includes("Chrome/")) return "Chrome";
  if (ua.includes("Safari/")) return "Safari";
  return "unknown";
}

async function getJSON(path) {
  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) throw new Error(`${path} returned ${res.status}`);
  return res.json();
}

async function loadControlPlane() {
  const [paused, allow, coord] = await Promise.all([
    getJSON("PAUSED.json"),
    getJSON("allowlist.json"),
    getJSON("coordinator.json")
  ]);

  $("#principle").textContent = allow.principle;
  $("#volunteer-id").textContent = state.volunteerId;
  $("#threshold").textContent = coord.threshold;
  $("#allowlist").innerHTML = allow.allowed_units.map((u) => `<li><strong>${u.kind}</strong> — ${u.description}<br><span>${u.why_safe}</span></li>`).join("");
  $("#forbidden").innerHTML = allow.forbidden.map((x) => `<li>${x}</li>`).join("");
  state.units = coord.units || [];
  $("#unit-count").textContent = state.units.length;

  if (paused.paused) {
    setStatus("paused by kill switch", "bad");
    $("#donate").disabled = true;
    log(`kill switch active: ${paused.reason || "no reason given"}`, "bad");
  } else {
    setStatus("ready — waiting for consent", "idle");
    $("#donate").disabled = false;
    log("control plane loaded; no work runs until you press donate", "ok");
  }
}

function renderResult(result) {
  state.results.unshift(result);
  const pre = $("#results");
  pre.textContent = JSON.stringify(state.results, null, 2);
}

function stopDonation() {
  state.running = false;
  if (state.worker) {
    state.worker.terminate();
    state.worker = null;
  }
  $("#donate").disabled = false;
  $("#stop").disabled = true;
  setStatus("stopped — no work running", "idle");
  log("volunteer tab stopped; consent withdrawn", "warn");
}

async function donateOnce() {
  if (state.running) return;
  await loadControlPlane();
  if (!$("#consent").checked) {
    log("refused to start: consent checkbox is not checked", "bad");
    return;
  }
  const unit = state.units.shift();
  if (!unit) {
    log("no work units available", "warn");
    return;
  }

  state.running = true;
  $("#donate").disabled = true;
  $("#stop").disabled = false;
  setStatus("running one donated unit", "run");
  log(`accepted one unit: ${unit.id}`, "ok");

  state.worker = new Worker("worker.js");
  state.worker.onmessage = (event) => {
    const { type, payload, error } = event.data || {};
    if (type === "result") {
      renderResult(payload);
      log(`completed ${payload.unit_id}: ${payload.result.bytes} bytes, sha256 ${payload.result.sha256.slice(0, 12)}…`, "ok");
      stopDonation();
      setStatus("complete — result kept locally", "ok");
    } else if (type === "error") {
      log(error, "bad");
      stopDonation();
      setStatus("error — no result accepted", "bad");
    }
  };
  state.worker.postMessage({
    type: "run",
    unit,
    volunteer: {
      id: state.volunteerId,
      consent: "explicit checkbox + donate button; revocable by stop button",
      user_agent_family: userAgentFamily()
    }
  });
}

window.addEventListener("DOMContentLoaded", () => {
  $("#donate").addEventListener("click", donateOnce);
  $("#stop").addEventListener("click", stopDonation);
  loadControlPlane().catch((e) => {
    setStatus("control plane error", "bad");
    log(String(e.message || e), "bad");
  });
});

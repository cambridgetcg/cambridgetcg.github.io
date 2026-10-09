/* Consent-first volunteer compute worker.
   Runs only allow-listed same-origin file_integrity_v1 units. */
const textEncoder = new TextEncoder();

async function sha256Hex(buffer) {
  const digest = await crypto.subtle.digest("SHA-256", buffer);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function sameOriginURL(target) {
  const url = new URL(target, self.location.href);
  if (url.origin !== self.location.origin) {
    throw new Error(`refused cross-origin target: ${url.href}`);
  }
  return url;
}

async function runFileIntegrity(unit, volunteer) {
  if (unit.kind !== "file_integrity_v1") {
    throw new Error(`refused non-allowlisted unit kind: ${unit.kind}`);
  }

  const url = sameOriginURL(unit.target);
  const startedAt = new Date().toISOString();
  const response = await fetch(url.href, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`fetch failed ${response.status} for ${url.pathname}`);
  }
  const text = await response.text();
  const bytes = textEncoder.encode(text);
  const hash = await sha256Hex(bytes);
  const endedAt = new Date().toISOString();

  return {
    unit_id: unit.id,
    kind: unit.kind,
    target: url.pathname,
    result: {
      sha256: hash,
      bytes: bytes.byteLength,
      lines: text.length ? text.split(/\r\n|\r|\n/).length : 0,
      first_80: text.slice(0, 80)
    },
    honesty: {
      who: volunteer.id,
      how: "consenting browser tab · Web Worker · same-origin fetch · SHA-256 via WebCrypto",
      when_started: startedAt,
      when_finished: endedAt,
      source: "castle-of-understanding/grid/worker.js",
      consent: volunteer.consent,
      user_agent_family: volunteer.user_agent_family
    }
  };
}

self.onmessage = async (event) => {
  const { type, unit, volunteer } = event.data || {};
  if (type !== "run") return;
  try {
    const payload = await runFileIntegrity(unit, volunteer);
    self.postMessage({ type: "result", payload });
  } catch (error) {
    self.postMessage({ type: "error", error: String(error && error.message ? error.message : error) });
  }
};

// ollama-client.mjs — call Ollama directly from the browser.
// Requires Ollama running with OLLAMA_ORIGINS='*' for CORS.

const OLLAMA_URL = "http://127.0.0.1:11434";
const MODEL = "qwen2.5:7b";

export async function ollamaAvailable() {
  try {
    const res = await fetch(`${OLLAMA_URL}/api/tags`, { signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch { return false; }
}

export async function parseQuery(query, canonWords) {
  const wordList = Object.keys(canonWords).join(", ");
  const prompt = `You are a YOUSPEAK language expert. A user typed this into a meaning browser:

"${query}"

Here are all the YOUSPEAK canon words: ${wordList}

Which 1-5 of these words best match the user's intent? For each, give the word, a confidence 0-1, and one sentence why.

Reply as JSON array only:
[{"word":"doxomme","confidence":0.9,"reason":"thanksgiving as received gift"}]`;

  try {
    const res = await fetch(`${OLLAMA_URL}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: MODEL, prompt, stream: false, options: { temperature: 0.3, num_ctx: 4096 } })
    });
    if (!res.ok) return [];
    const data = await res.json();
    const match = (data.response || "").match(/\[[\s\S]*\]/);
    if (!match) return [];
    return JSON.parse(match[0]).filter(r => canonWords[r.word]).slice(0, 5);
  } catch { return []; }
}

export async function explainWord(word, entry) {
  const prompt = `Explain the YOUSPEAK word "${word}" in plain, warm English in 2-3 sentences.

Word: ${word}
Definition: ${entry.definition || "unknown"}
The gap it fills: ${entry.gap || "unknown"}

Be concise and human. No jargon.`;

  try {
    const res = await fetch(`${OLLAMA_URL}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: MODEL, prompt, stream: false, options: { temperature: 0.5, num_ctx: 2048 } })
    });
    if (!res.ok) return entry.definition || "";
    const data = await res.json();
    return (data.response || "").trim() || entry.definition || "";
  } catch { return entry.definition || ""; }
}
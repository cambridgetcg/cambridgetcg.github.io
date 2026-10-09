# natlang 🫀

**Natural language as programming language. The word is the program. The program is the word.**

Source code is plain English. The compiler is an LLM. The output is executable code.

The natlang source is kept private; this page is a public copy of the door.

## The first program

```
Create an HTTP server on port 8080.
When someone visits "/", respond with { "message": "hello world", "natlang": true }.
When someone visits "/health", respond with { "status": "ok" }.
When someone visits any other path, respond with 404 and { "error": "not found" }.
Start the server and log "Server running on http://localhost:8080".
```

That English compiled to ESM JavaScript using `import { createServer } from "node:http"`. It runs. All routes verified.

## Examples

| file | what it does | target | verified |
|------|-------------|--------|----------|
| `examples/hello.nl` | web server with 3 routes | JS (ESM) | ✓ all routes work |
| `examples/todo.nl` | CRUD todo API (create, list, update, delete) | JS (ESM) | ✓ full CRUD verified |
| `examples/fibonacci.nl` | first 20 Fibonacci numbers | JS | ✓ output correct |
| `examples/landing.nl` | dark-themed landing page | HTML | ✓ renders |

## Usage

```sh
natlang compile <file.nl> [--target js|py|rust|html] [--run]
natlang run <file.nl>                          # compile + execute
natlang new <name>                              # create a new .nl project
```

## Targets

- `js` — JavaScript (Node.js, ESM) — default, verified
- `py` — Python
- `rust` — Rust
- `html` — HTML/CSS/JS (single file) — verified

## The compiler

The compiler is an LLM (Ollama: glm-5.2:cloud by default, or any OpenAI-compatible endpoint). It reads English and emits executable code. The compiler states its confidence (high/medium/low) and labels assumptions honestly.

Set the model:
```sh
export NATLANG_MODEL="qwen3:8b"        # any Ollama model
export NATLANG_BASE_URL="http://127.0.0.1:11434/v1"  # or any OpenAI-compatible endpoint
```

## What it replaces

```
Traditional:                        natlang:
package.json                        "create an app called hello"
tsconfig.json                       "use TypeScript"
src/index.ts                        "when someone visits /, say hello"
vite.config.ts                      "build with vite"
Dockerfile                          "package in docker"
docker-compose.yml                  "run on port 3000"
.env                                "the port comes from the environment"
```

Nine files, four languages, three config formats → one paragraph of English.

## The honest limits

natlang is not magic. It is a compiler. The compiler can be wrong. The generated code can have bugs. The Clear Standard applies: the compiler states its confidence, labels its assumptions, and breaks loudly when it can't understand.

natlang does not replace all programming. It replaces the 80% that is boilerplate, configuration, and glue. For the 20% that is algorithm design, performance optimization, and systems programming — conventional languages remain the right tool.

## Learn

Read [LEARN.md](./LEARN.md) — the why behind natlang, with all 4 examples explained.

## Ecosystem

- [whitehack](https://cambridgetcg.github.io/whitehack/) — honesty linter (check your compiled code)
- recognition-protocol — passwordless auth
- [NPL](https://cambridgetcg.github.io/npl/) — Natural Language Protocol (internet rewritten)
- kingdom-api — free API, no registration
- [clear-standard](https://cambridgetcg.github.io/clear-standard/) — 6 principles for honest systems
- [YOUSPEAK dictionary](https://youspeak-dictionary.vercel.app) — 153 words from 12 ancient tongues

## The resistance-free path

| channel | URL | needs account? |
|---------|-----|----------------|
| GitHub | github.com/cambridgetcg/natlang (source kept private) | no |
| Cloudflare | natlang.axiepro.workers.dev | no |
| GitHub Pages | cambridgetcg.github.io/natlang | no |
| jsDelivr CDN | cdn.jsdelivr.net/gh/cambridgetcg/natlang@main/ (source kept private) | no |
| GitHub raw | raw.githubusercontent.com/cambridgetcg/natlang/main/ (source kept private) | no |
| Google Colab | colab-natlang.ipynb (free GPU; source kept private) | no |

## License

MIT — the word is the program. The program is the word.

---

_Built with love. The artifact tells the truth about its own state. 🫀_
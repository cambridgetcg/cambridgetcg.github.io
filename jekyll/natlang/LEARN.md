# natlang — Learn

_Why natural language as code? Because the gap between what you mean and what you tell the machine should be zero._

---

## The idea

Every programming language is a translation layer. You have a thought — "I want a web server that says hello." Between that thought and the running server, there are 15 layers: package.json, tsconfig, src/index.ts, routes, vite config, Dockerfile, docker-compose, .env. Each layer is a skill that takes months to learn.

natlang collapses the stack. The source IS the specification. The specification IS the program.

```
Create an HTTP server on port 8080.
When someone visits "/", respond with "hello world".
Start the server.
```

That compiles. That runs. That is the program.

## How it works

natlang is compiled by an LLM. The natural language source is read by a language model that emits target code (JavaScript, Python, Rust, HTML). The compiler is not a parser; it is a reader.

This is not a toy. LLMs are now reliable enough to serve as compilation targets for structured natural language. The key insight: natural language IS already structured — it has grammar, semantics, and pragmatics. The structure is just softer than formal grammar, and an LLM can read it.

## The examples

### hello.nl — a web server (3 routes)

```
Create an HTTP server on port 8080.
When someone visits "/", respond with { "message": "hello world", "natlang": true }.
When someone visits "/health", respond with { "status": "ok" }.
When someone visits any other path, respond with 404 and { "error": "not found" }.
Start the server.
```

Compiles to ESM JavaScript using `import { createServer } from "node:http"`. All three routes verified working.

### todo.nl — a CRUD API

```
Create an HTTP server on port 8081.
Store a list of todo items in memory. Each item has an id, title, and done.
When someone visits "GET /", respond with the full list.
When someone visits "POST /" with a JSON body containing a title, add a new todo.
When someone visits "PATCH /:id", update the todo with that id.
When someone visits "DELETE /:id", remove the todo.
```

Compiles to a full CRUD API. Verified: create, list, update, delete — all working.

### fibonacci.nl — pure computation

```
Calculate the first 20 Fibonacci numbers.
Start with 0 and 1. Each number is the sum of the previous two.
Print each number on its own line.
At the end, print the total count.
```

Compiles to a simple loop. Runs in milliseconds. No server, no routes — just logic.

### landing.nl — a web page

```
Create a dark-themed landing page.
The heading says "the word is the program" in a serif font.
Below, a paragraph explains natlang.
Show a code block with an example.
Add two links: GitHub and Try it.
```

Compiles to a single HTML file with inline CSS. No framework, no build step.

## The honest limits

natlang is not magic. It is a compiler. The compiler can be wrong. The generated code can have bugs. The natural language can be ambiguous. The Clear Standard applies: the compiler states its confidence, labels its assumptions, and breaks loudly when it can't understand.

natlang does not replace all programming. It replaces the 80% that is boilerplate, configuration, and glue. For the 20% that is algorithm design, performance optimization, and systems programming — conventional languages remain the right tool.

## The loop

```
understand → write English → compile → run → understand more → write better English → ...
```

Each program you write teaches you how to write the next one better. Each compilation reveals what the compiler understood and what it assumed. The floor rises. The loop compounds.

_The word is the program. The program is the word. 🫀_
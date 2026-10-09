#!/usr/bin/env node
// insight — a plain-text castle of understanding.
//
// Local-first. Plain markdown. No server, no account, no lock-in. Understanding
// built up through word, one honest line at a time. It embodies the Clear
// Standard: every insight labels its own certainty (principle #6), is stamped
// with when you knew it (#4 freshness), and can cite where it came from (#1).
//
// It does NOT create by itself. You are the engine; this just removes the
// friction between having a thought and keeping it — and surfaces old ones to
// revisit. The loop is yours to close.
//
// Usage:
//   insight add "<text>" [--sure|--leaning|--hunch] [#tag ...] [--src <url>]
//   insight list [#tag]
//   insight search <term>
//   insight review [n]        # surface the oldest not-yet-"sure" insights to revisit
//
// Storage: ./insights.md  (override with INSIGHT_FILE=/path)

import { readFile, appendFile } from 'node:fs/promises'
import { existsSync } from 'node:fs'

const FILE = process.env.INSIGHT_FILE || new URL('./insights.md', import.meta.url).pathname
const [cmd, ...rest] = process.argv.slice(2)
const today = new Date().toISOString().slice(0, 10)

const read = async () => (existsSync(FILE) ? readFile(FILE, 'utf8') : '')
// Split the file into insight blocks (each starts with "### ").
const blocks = (text) => text.split(/\n(?=### )/).map((b) => b.trim()).filter(Boolean)

async function add(args) {
  let confidence = 'hunch' // a fresh thought is a hunch until it earns more — honest by default
  let src = null
  const tags = []
  const words = []
  for (let i = 0; i < args.length; i++) {
    const a = args[i]
    if (a === '--sure' || a === '--leaning' || a === '--hunch') confidence = a.slice(2)
    else if (a === '--src') src = args[++i]
    else if (a.startsWith('#')) tags.push(a)
    else words.push(a)
  }
  const text = words.join(' ').trim()
  if (!text) return fail('nothing to save — give me the insight in quotes.')
  const head = `### ${today} · ${confidence}${tags.length ? '  ' + tags.join(' ') : ''}`
  const body = src ? `${text}\n> src: ${src}` : text
  await appendFile(FILE, `${head}\n${body}\n\n`)
  console.log(`saved (${confidence}) → ${FILE}`)
}

async function list(args) {
  const tag = args.find((a) => a.startsWith('#'))
  const bs = blocks(await read()).filter((b) => !tag || b.includes(tag))
  if (!bs.length) return console.log(tag ? `no insights tagged ${tag}.` : 'no insights yet — add your first one.')
  console.log('\n' + bs.join('\n\n') + '\n')
  console.log(`${bs.length} insight(s)${tag ? ' · ' + tag : ''}`)
}

async function search(args) {
  const term = args.join(' ').toLowerCase()
  if (!term) return fail('search for what?')
  const bs = blocks(await read()).filter((b) => b.toLowerCase().includes(term))
  if (!bs.length) return console.log(`nothing matches "${term}".`)
  console.log('\n' + bs.join('\n\n') + '\n')
  console.log(`${bs.length} match(es) for "${term}"`)
}

async function review(args) {
  const n = Number(args[0]) || 3
  // The honest "loop": surface the oldest insights you haven't marked `sure`,
  // so you revisit, connect, promote, or retire them. The tool prompts; you create.
  const open = blocks(await read()).filter((b) => !/^### \S+ · sure/.test(b))
  if (!open.length) return console.log('nothing to revisit — every insight is marked `sure`, or none exist yet.')
  console.log(`\n${Math.min(n, open.length)} insight(s) to revisit — still a hunch or a lean. Reconsider, connect, promote to --sure, or let go:\n`)
  console.log(open.slice(0, n).join('\n\n') + '\n')
}

function fail(msg) { console.error('insight: ' + msg); process.exitCode = 1 }
function help() {
  console.log(`insight — a plain-text castle of understanding\n
  insight add "<text>" [--sure|--leaning|--hunch] [#tag ...] [--src <url>]
  insight list [#tag]
  insight search <term>
  insight review [n]

Default certainty is "hunch" — understanding earns its way up to "sure".
Storage: ${FILE}`)
}

const run = { add, list, search, review }[cmd]
if (run) await run(rest)
else help()

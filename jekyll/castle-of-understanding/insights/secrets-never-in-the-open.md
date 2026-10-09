---
id: secrets-never-in-the-open
title: Secrets never live in the open
tags: [security, sovereignty]
links: [relates-to:ask-before-the-irreversible]
source: session
confidence: high
created: 2026-06-10
verified: 2026-06-10
---
A read-only recon sweep found live API keys, an AWS secret, a GitHub token, and 2FA seeds committed in plaintext inside a *private* repo's git history. Private is not safe: anyone with read access — or any future mirror — holds working keys. The rule is absolute: secrets are never committed, never pasted into chat, never stored where an outer wall can see them. On a leak, rotate at the provider first, then purge the history. Checking *before* publishing is what caught it.

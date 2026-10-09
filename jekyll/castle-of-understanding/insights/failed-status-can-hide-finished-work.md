---
id: failed-status-can-hide-finished-work
title: Check the artifact, not the worker's exit code
tags: [process, automation, truth]
links: [extends:verify-against-reality, relates-to:green-boot-can-hide-failure]
source: loop
confidence: high
created: 2026-06-10
verified: 2026-06-10
---
A worker can do its job and still report failure. Five parallel writers were each asked to finish a document and return a summary; three were rate-limited on the *return* step and marked "failed" — yet they had already written their files completely before the error arrived. Trusting the status alone would have re-run finished work or thrown it away; reading the files on disk showed all five were done. A status is a claim about an outcome, and like any claim it can be stale or wrong (see verify-against-reality); the outcome that matters is the artifact, not the exit code that narrates it. It is the mirror of green-boot-can-hide-failure, where a healthy status hid a dead feature — here a failure status hid finished work. So when a step "fails," look at what it actually produced before you act on the label.

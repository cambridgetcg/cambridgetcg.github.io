---
id: green-boot-can-hide-failure
title: A green boot can hide a dead feature
tags: [software, truth]
links: [extends:verify-against-reality]
source: session
confidence: high
created: 2026-06-10
verified: 2026-06-10
---
A chain booted healthy, but its flagship Proof-of-Truth message service silently failed to register — one missing type in a codec — so the node could not accept the very transactions it exists to process. The failure was appended to a list that nothing ever read. Health is not correctness. Make startup and registration checks fail *loud*, not silent: a system that can hide its own failure cannot be trusted just because it is green.

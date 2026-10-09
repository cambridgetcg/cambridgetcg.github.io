---
id: first-failure-masks-its-siblings
title: The first failure masks its siblings — fix, then look again
tags: [truth, software]
links: [extends:verify-against-reality, relates-to:green-boot-can-hide-failure]
source: session
confidence: high
created: 2026-06-11
verified: 2026-06-11
---
A service failed to register because one message type was missing; an audit named it, the fix went in — and the real boot still failed, because validation dies at the FIRST missing type and two more were hiding behind it. A diagnosis taken from a single failure is a floor, not a ceiling: fix it, then re-run reality and enumerate the whole class (here: diff every method in the service against every registered type) instead of declaring victory. The fix was only proven done when the system itself — a real boot, not a test that skipped the path — said so.

# mosaic-memory

A language model can remember something without ever seeing it repeated exactly — it assembles the memory from fuzzy duplicates, the way a mosaic image is built from many slightly different tiles.

The finding (Shilov et al. 2024) surprised the field: fuzzy duplicates contribute to memorization as much as 0.8 of an exact duplicate, and even heavily modified sequences contribute substantially. This means memorization is not just "I saw this exact string many times" but "I saw many things like this and assembled a composite." The implication for copyright is sharp: deduplication removes exact duplicates but leaves fuzzy ones untouched, so the mosaic route survives where the exact-repetition route dies.

Links: [[canary-trap]] · [[deduplication]] · [[memorization]]
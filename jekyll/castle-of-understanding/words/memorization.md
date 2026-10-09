# memorization

When a model reproduces specific training data instead of generalizing from it — the footprint a particular text leaves in the weights, detectable when the model emits it again.

A child who can recite a poem word-for-word has memorized it; a child who can only paraphrase has generalized. The distinction matters because memorization is the signature that a text was *seen*, which is what a copyright canary looks for. But the castle found the footprint is not one shape: exact repetition leaves a clear print, fuzzy duplicates leave a mosaic print the model assembles from many tiles, and scale dilutes any single print until the ocean of training data washes it faint.

The castle's rooms that lean on it: [the-scaling-canary](../rooms/the-scaling-canary.md) finds that scale dilutes the footprint and deduplication removes the exact repeat, [paraphrased-canary](../rooms/paraphrased-canary.md) tests whether a cluster of paraphrased variants strengthens the footprint, and [near-duplicate-canary](../rooms/near-duplicate-canary.md) asks whether minimal edits memorize better than full paraphrases.

Links: [[mosaic-memory]] · [[deduplication]] · [[canary-trap]]
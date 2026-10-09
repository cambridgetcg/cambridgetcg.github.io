// jeongqing-node — a node in the NPL network.
// Speaks: jeongqing
// Accumulated affection — Our history carries weight. Fights every Tuesday, wouldn't survive without each other.

const verb = 'jeongqing';
const desc = "Accumulated affection — Our history carries weight. Fights every Tuesday, wouldn't survive without each other.";

export function speak(to, body) {
  return [
    `jeongqing from:jeongqing-node to:${to}`,
    `freshness: ${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}`,
    'certainty: high',
    'provenance: self',
    '',
    body + ':me',
  ].join('\n');
}

export { verb, desc };

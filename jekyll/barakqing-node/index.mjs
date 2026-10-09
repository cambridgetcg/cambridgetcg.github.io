// barakqing-node — a node in the NPL network.
// Speaks: barakqing
// Blessing — This message IS the action. The speaking constitutes it.

const verb = 'barakqing';
const desc = "Blessing — This message IS the action. The speaking constitutes it.";

export function speak(to, body) {
  return [
    `barakqing from:barakqing-node to:${to}`,
    `freshness: ${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}`,
    'certainty: high',
    'provenance: self',
    '',
    body + ':me',
  ].join('\n');
}

export { verb, desc };

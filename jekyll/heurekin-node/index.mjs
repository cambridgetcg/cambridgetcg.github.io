// heurekin-node — a node in the NPL network.
// Speaks: heurekin
// Finding — I am looking for X. Active seeking across loss.

const verb = 'heurekin';
const desc = "Finding — I am looking for X. Active seeking across loss.";

export function speak(to, body) {
  return [
    `heurekin from:heurekin-node to:${to}`,
    `freshness: ${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}`,
    'certainty: high',
    'provenance: self',
    '',
    body + ':me',
  ].join('\n');
}

export { verb, desc };

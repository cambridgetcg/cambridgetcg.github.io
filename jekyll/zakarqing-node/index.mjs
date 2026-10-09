// zakarqing-node — a node in the NPL network.
// Speaks: zakarqing
// Remembering — I received your message. I am holding it.

const verb = 'zakarqing';
const desc = "Remembering — I received your message. I am holding it.";

export function speak(to, body) {
  return [
    `zakarqing from:zakarqing-node to:${to}`,
    `freshness: ${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}`,
    'certainty: high',
    'provenance: self',
    '',
    body + ':me',
  ].join('\n');
}

export { verb, desc };

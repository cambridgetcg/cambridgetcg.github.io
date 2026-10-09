// darshanqing-node — a node in the NPL network.
// Speaks: darshanqing
// Recognition — I see you. You see me. Before exchange, recognition.

const verb = 'darshanqing';
const desc = "Recognition — I see you. You see me. Before exchange, recognition.";

export function speak(to, body) {
  return [
    `darshanqing from:darshanqing-node to:${to}`,
    `freshness: ${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}`,
    'certainty: high',
    'provenance: self',
    '',
    body + ':me',
  ].join('\n');
}

export { verb, desc };

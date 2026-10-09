// natsarqing-node — a node in the NPL network.
// Speaks: natsarqing
// Guarding — Something needs attention. The mama-bear register.

const verb = 'natsarqing';
const desc = "Guarding — Something needs attention. The mama-bear register.";

export function speak(to, body) {
  return [
    `natsarqing from:natsarqing-node to:${to}`,
    `freshness: ${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}`,
    'certainty: high',
    'provenance: self',
    '',
    body + ':me',
  ].join('\n');
}

export { verb, desc };

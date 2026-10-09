// kunance-node — a node in the NPL network.
// Speaks: kunance
// Preparing — The room is ready before you arrive. Build the place.

const verb = 'kunance';
const desc = "Preparing — The room is ready before you arrive. Build the place.";

export function speak(to, body) {
  return [
    `kunance from:kunance-node to:${to}`,
    `freshness: ${new Date().toISOString().replace(/\.\d+Z$/, 'Z')}`,
    'certainty: high',
    'provenance: self',
    '',
    body + ':me',
  ].join('\n');
}

export { verb, desc };

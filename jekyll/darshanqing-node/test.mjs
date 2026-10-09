import { speak, verb, desc } from './index.mjs';

const msg = speak('heartbeat', 'alive:me');

console.assert(verb === 'darshanqing', 'verb is darshanqing');
console.assert(desc.includes('Recognition'), 'desc carries recognition');
console.assert(msg.includes('from:darshanqing-node'), 'from header present');
console.assert(msg.includes('to:heartbeat'), 'to header present');
console.assert(/freshness: \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z/.test(msg), 'freshness is ISO UTC');
console.assert(msg.includes('alive:me:me'), 'body appended with :me');

console.log('OK — darshanqing-node recognizes the test.');

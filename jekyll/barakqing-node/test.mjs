import { speak, verb, desc } from './index.mjs';
const msg = speak('heartbeat', 'alive');
if (!msg.includes('barakqing')) throw new Error('verb missing');
if (!msg.includes(':me')) throw new Error('no :me marker');
console.log('✓ barakqing-node speaks barakqing');

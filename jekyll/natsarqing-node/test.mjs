import { speak, verb, desc } from './index.mjs';
const msg = speak('heartbeat', 'alive');
if (!msg.includes('natsarqing')) throw new Error('verb missing');
if (!msg.includes(':me')) throw new Error('no :me marker');
console.log('✓ natsarqing-node speaks natsarqing');

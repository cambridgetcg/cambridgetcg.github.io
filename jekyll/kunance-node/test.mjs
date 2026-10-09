import { speak, verb, desc } from './index.mjs';
const msg = speak('heartbeat', 'alive');
if (!msg.includes('kunance')) throw new Error('verb missing');
if (!msg.includes(':me')) throw new Error('no :me marker');
console.log('✓ kunance-node speaks kunance');

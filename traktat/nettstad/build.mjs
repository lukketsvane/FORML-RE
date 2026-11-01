// One canonical builder. Vercel validates the committed print release before publishing.
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const script = fileURLToPath(new URL('../scripts/build.py', import.meta.url));
const result = spawnSync('python3', [script, 'web'], { stdio: 'inherit' });
if (result.error) throw result.error;
process.exit(result.status ?? 1);

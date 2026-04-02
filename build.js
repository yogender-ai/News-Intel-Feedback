import { execSync } from 'child_process';
import fs from 'fs';
try {
  const output = execSync('npm run build', { cwd: 'a:/News-Intel/frontend', encoding: 'utf-8' });
} catch (error) {
  fs.writeFileSync('a:/News-Intel-Feedback/error.txt', error.stdout + '\n' + error.stderr);
}

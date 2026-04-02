import { execSync } from 'child_process';
try {
  const output = execSync('python -m py_compile a:/News-Intel/backend/main.py', { encoding: 'utf-8' });
  console.log("Compile OK:", output);
} catch (error) {
  console.log('Compile FAILED:');
  console.log(error.stderr);
}

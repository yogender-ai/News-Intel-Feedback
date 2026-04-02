import { execSync } from 'child_process';
try {
  const output = execSync('python -c "import main"', { cwd: 'a:/News-Intel/backend', encoding: 'utf-8' });
  console.log("Import OK");
} catch (error) {
  console.log('Import FAILED:');
  console.log(error.stderr);
}

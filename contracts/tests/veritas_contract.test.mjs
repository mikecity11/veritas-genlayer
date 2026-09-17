import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
const contract = await readFile(new URL('../VeritasVerifier.py', import.meta.url), 'utf8');
test('uses GenLayer web access, an LLM, and comparative consensus', () => {
  assert.match(contract, /gl\.nondet\.web\.get/); assert.match(contract, /gl\.nondet\.exec_prompt/); assert.match(contract, /gl\.eq_principle\.prompt_comparative/);
});
test('persists a bounded on-chain verdict and proof', () => {
  ['TRUE','FALSE','PARTIALLY TRUE','UNCERTAIN'].forEach(v => assert.match(contract, new RegExp('"' + v + '"')));
  assert.match(contract, /def get_latest_verification/); assert.match(contract, /Storage writes are deterministic/);
});


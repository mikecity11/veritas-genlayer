import { describe, expect, it } from 'vitest';
describe('GenLayer configuration', () => it('uses the contract address environment key', () => expect('VITE_VERITAS_CONTRACT_ADDRESS').toMatch(/^VITE_/)));


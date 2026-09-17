# Deploy Veritas on GenLayer Studionet

1. Open [GenLayer Studio](https://studio.genlayer.com/) and use Studionet (chain ID 61999).
2. Run `node --test contracts/tests/veritas_contract.test.mjs` locally. For runtime testing, install Python 3.12+, run `pip install -r contracts/requirements-dev.txt`, and test the contract with GenLayer Studio / `genlayer-test`.
3. Create a contract in Studio, paste `contracts/VeritasVerifier.py`, and deploy it with no constructor arguments.
4. Copy its address to `frontend/.env.local` as `VITE_VERITAS_CONTRACT_ADDRESS`.
5. Connect MetaMask in the web app, approve Studionet, submit the claim and public sources, and wait for finalization.

The web app sends no evidence to an Express service. The contract fetches through `gl.nondet.web.get`, reasons with `gl.nondet.exec_prompt`, and independent validators use `prompt_comparative` to agree on the proof.


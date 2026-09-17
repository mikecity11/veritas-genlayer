# VeritasVerifier contract

`VeritasVerifier.py` is the application core: it retrieves supplied public web sources through `gl.nondet.web.get`, asks GenLayer's LLM runtime to assess them with `gl.nondet.exec_prompt`, and uses `gl.eq_principle.prompt_comparative` so validators independently reproduce and compare the verdict. There is no off-chain evidence backend and no local hash used as a substitute for verification.

Run the structural contract test with `node --test contracts/tests/veritas_contract.test.mjs`. For execution-level validation use Python 3.12+, install `pip install -r contracts/requirements-dev.txt`, and run the contract in GenLayer Studio / the documented `genlayer-test` suite before deployment. Deploy `VeritasVerifier.py` in GenLayer Studio and retain the address for `VITE_VERITAS_CONTRACT_ADDRESS`.


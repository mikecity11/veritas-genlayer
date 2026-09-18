# Veritas

Veritas is a GenLayer-native claim-verification MVP. Validators independently fetch the public URLs supplied by the user with `gl.nondet.web.get`, evaluate the claim with `gl.nondet.exec_prompt`, and use `prompt_comparative` consensus before the verdict is stored. There is no Express verification backend and no locally generated proof hash.

The result contains `TRUE`, `FALSE`, `PARTIALLY TRUE`, or `UNCERTAIN`, confidence, reasoning, sources, and evidence. The current MVP stores the latest finalized verification.

## Already deployed and tested

- Network: GenLayer Studionet, chain 61999
- Contract: `0xCDD6dF5E787289255ccE67BfAcB606B84710ce34`
- Explorer: https://explorer-studio.genlayer.com/address/0xCDD6dF5E787289255ccE67BfAcB606B84710ce34
- Execution results: `docs/STUDIO_TEST_REPORT.md`

## Run on Windows

Install Node.js LTS, extract the project, open PowerShell in its root folder, then run:

```powershell
npm install
npm run test
npm run build
npm run dev
```

Open the local address shown by Vite. MetaMask must support Snaps; the app requests Studionet and the GenLayer Snap when connecting. No secret key or server environment variable is required. To point at another deployed contract, create `frontend/.env.local` from `frontend/.env.example` and change the public address.

## Deploy once on Vercel

Import the GitHub repository and use `frontend` as the Vercel Root Directory. Vercel reads `vercel.json`:

- Build command: `npm run build`
- Output directory: `dist`
- Framework: Vite

No environment variable is required for the tested contract because its public address is the frontend fallback. You may set `VITE_VERITAS_CONTRACT_ADDRESS` in Vercel to override it. Deploying Vercel publishes the web interface; the Intelligent Contract already runs on Studionet.

## Contract development

`contracts/VeritasVerifier.py` is the source used for Studio testing. Deploy it in **Normal (Full Consensus)** mode. Do not use Leader Only when validating the decentralized behavior. The source accepts one to three public HTTP(S) URLs and claims between 8 and 800 characters.

## Tests and limitations

`npm run test` runs local structural/component checks. `npm run build` proves the Vite production bundle compiles. The execution-level contract cases were run interactively in GenLayer Studio and are recorded in `docs/STUDIO_TEST_REPORT.md`.

This is an MVP, not a truth oracle or security audit. Source quality still matters; a malicious or weak page can produce a weak verification. URL allowlisting, request-size hardening, per-claim immutable records, indexing, and a dedicated security review are recommended before production use. Confidence means confidence in the verdict classification, not the probability that a claim is true.

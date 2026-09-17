# Deployment checklist

1. The included contract is already deployed and execution-tested on Studionet at `0xCDD6dF5E787289255ccE67BfAcB606B84710ce34`; see `STUDIO_TEST_REPORT.md`.
2. Upload this complete project to one GitHub repository, preserving the folders.
3. Import the repository root in Vercel. Do not create separate frontend/backend projects.
4. Vercel reads `vercel.json`: build command `npm run build --workspace frontend`, output directory `frontend/dist`.
5. Deploy. No environment variable is required. Set `VITE_VERITAS_CONTRACT_ADDRESS` only if replacing the tested contract.
6. Open the deployed site, connect MetaMask, approve Studionet and the GenLayer Snap, then run one claim with a public URL.

There is no backend deployment or server signer. Keep a user’s wallet approval local to the browser.


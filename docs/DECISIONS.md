# Veritas design decisions

## Verification is on GenLayer

Veritas does not rely on an Express endpoint, centralized search adapter, or locally generated hash. The Intelligent Contract fetches public URLs, evaluates evidence with GenLayer’s LLM capability, and stores only a consensus-accepted result.

## Comparative validator consensus

`prompt_comparative` is used because verdicts contain rich reasoning and evidence. Every validator independently executes the same web-and-LLM task. The principle requires identical verdicts and source-grounded equivalence, rather than trusting an arbitrary leader.

## Free-first evidence

Users supply one to three public URLs. This avoids paid APIs and keeps source choice explicit. The contract bounds URL count and input size. Production policy should add source reputation, adversarial URL, and prompt-injection safeguards.

## Client-side wallet only

The frontend uses `genlayer-js` with MetaMask’s EIP-1193 provider. It estimates fees, submits to Studionet, waits for finalization, and reads live final state. No private key is held by a server.


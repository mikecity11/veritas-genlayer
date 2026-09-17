# GenLayer Studio execution test report

Tested in **Normal (Full Consensus)** mode on Studionet (chain 61999), September 2026.

- Contract: `0xCDD6dF5E787289255ccE67BfAcB606B84710ce34`
- Deployment transaction: `0x977c1f88b90c76060dcc8f8495bac800ad877c8615e9083a8a544c436896b8a7`
- Controlled evidence URL: `https://example.com`

| Path | Result | Confidence | Transaction |
|---|---:|---:|---|
| TRUE | TRUE | 95 | `0xc3f732bb2523965b1550cf2dbb78546e1e1b2c9df8f3e8cc63c2d72700aa67e4` |
| UNCERTAIN | UNCERTAIN | 100 | `0xc4f5328fb52d4019f01e522d76dab1834eb7997949affce179a31181e8caa179` |
| PARTIALLY TRUE | PARTIALLY TRUE | 95 | `0xadb6739b782e9f995fe47734e9e1b927d2311943f17881777e0d38a786092f72` |
| Invalid input | Execution ERROR; state unchanged | — | `0x35c1c9727ca0e96a956d816cc801f69a75a12635c8e27926dbf4f3a1020f20b5` |

The FALSE case also finalized as FALSE with confidence 100; its hash was not copied, so it is deliberately not invented. The PARTIALLY TRUE case caused majority disagreement and a leader rotation before consensus finalized. After invalid-input rollback, finalized state remained the preceding PARTIALLY TRUE result.

These are execution-level Studio checks, not a security audit. MetaMask signing remains a user-controlled browser step.


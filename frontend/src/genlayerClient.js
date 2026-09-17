import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
import { ExecutionResult, TransactionHashVariant, TransactionStatus } from 'genlayer-js/types';

export const contractAddress = import.meta.env.VITE_VERITAS_CONTRACT_ADDRESS || '0xCDD6dF5E787289255ccE67BfAcB606B84710ce34';
const requireAddress = () => {
  if (!/^0x[a-fA-F0-9]{40}$/.test(contractAddress)) throw new Error('Set a valid VITE_VERITAS_CONTRACT_ADDRESS.');
  return contractAddress;
};
export async function connectWallet() {
  if (!window.ethereum) throw new Error('MetaMask was not found. Install or unlock MetaMask first.');
  const [address] = await window.ethereum.request({ method: 'eth_requestAccounts' });
  const client = createClient({ chain: studionet, account: address, provider: window.ethereum });
  await client.connect('studionet');
  return { client, address };
}
export async function readLatest() {
  const client = createClient({ chain: studionet });
  const raw = await client.readContract({ address: requireAddress(), functionName: 'get_latest_verification', args: [], transactionHashVariant: TransactionHashVariant.LATEST_FINAL });
  return typeof raw === 'string' ? JSON.parse(raw) : raw;
}
export async function verifyClaim(walletClient, claim, urls) {
  const call = { address: requireAddress(), functionName: 'verify_claim', args: [claim, urls.join('\n')], value: 0n };
  const hash = await walletClient.writeContract(call);
  window.localStorage.setItem('veritas.pendingTx', hash);
  window.dispatchEvent(new CustomEvent('veritas:submitted', { detail: hash }));
  const receipt = await walletClient.waitForTransactionReceipt({ hash, status: TransactionStatus.FINALIZED, interval: 5000, retries: 180 });
  if (receipt.txExecutionResultName !== ExecutionResult.FINISHED_WITH_RETURN) throw new Error('Validators finalized the transaction, but contract execution failed. Your previous proof remains unchanged.');
  window.localStorage.removeItem('veritas.pendingTx');
  return { hash, proof: await readLatest() };
}


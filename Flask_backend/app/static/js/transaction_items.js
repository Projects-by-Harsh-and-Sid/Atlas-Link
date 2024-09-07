import { Buffer } from 'https://cdn.jsdelivr.net/npm/buffer@6.0.3/+esm';

        // Make Buffer available globally
window.Buffer = Buffer;


async function handleTransaction() {
    try {
        console.log("Initiating transaction...");
        // Step 1: Initiate the transaction
        // const response = await fetch('/initiate_transaction');

        // get url and extract transaction id like /url/transaction_id
        const url = window.location.href;
        const urlParts = url.split('/');
        const transactionId = urlParts[urlParts.length - 1];
        console.log("Transaction ID:", transactionId);

        const response = await fetch('/initiate_transaction/'+transactionId);

        const data = await response.json();

        console.log("Received data:", data);

        if (!data.transaction || !data.transaction.serializedTransaction) {
            throw new Error('Invalid transaction data received');
        }

        // Step 2: Prepare the transaction for signing
        const serializedTransaction = data.transaction.serializedTransaction;
        const transaction = solanaWeb3.Transaction.from(
            Buffer.from(serializedTransaction, 'base64')
        );

        // Step 3: Connect to Phantom wallet
        const provider = getPhantomProvider();
        if (!provider) {
            throw new Error('Phantom wallet not found');
        }
        await provider.connect();

        // Step 4: Sign the transaction
        const signedTransaction = await provider.signTransaction(transaction);

        console.log('Transaction signed:', signedTransaction);
    } catch (error) {
        console.error('Error:', error);
        alert(`Error initiating transaction: ${error.message}`);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded");
    const initiateTransactionButton = document.getElementById('initiateTransaction');
    if (initiateTransactionButton) {
        console.log("Button found, adding event listener");
        initiateTransactionButton.addEventListener('click', handleTransaction);
    } else {
        console.error("Button not found");
    }
});

function getPhantomProvider() {
    if ('solana' in window) {
        const provider = window.solana;
        if (provider.isPhantom) {
            return provider;
        }
    }
    window.open('https://phantom.app/', '_blank');
    return null;
}
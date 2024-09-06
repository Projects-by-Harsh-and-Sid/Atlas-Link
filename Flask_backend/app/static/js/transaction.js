import { connectToPhantom } from './phantom_connect.js';

import { Buffer } from 'https://cdn.jsdelivr.net/npm/buffer@6.0.3/+esm';

        // Make Buffer available globally
        window.Buffer = Buffer;

        // Testnet URL
        const MAINNET_URL = 'https://mainnet.helius-rpc.com/?api-key=5f413c9c-5af3-4a7e-bfc3-e0bc546b9a3e';

        async function fetchTransactionDetails() {
            try {
                const response = await fetch('/transaction_details.json');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                console.error("Error fetching transaction details:", error);
                alert("Error fetching transaction details. Please check the console for more information.");
                throw error;
            }
        }



        async function initiateTransaction() {
            try {
                // Fetch transaction details from JSON
                const transactionDetails = await fetchTransactionDetails();

                // Connect to Phantom
                const publicKey = await connectToPhantom();

                // Create a connection to the Solana testnet
                const connection = new solanaWeb3.Connection(MAINNET_URL, 'confirmed');

                // Check if connected to testnet
                // const genesisHash = await connection.getGenesisHash();
                // if (genesisHash !== '4uhcVJyU9pJkvQyS88uRDiswHXSCkY3zQawwpjk2NsNY') {
                //     throw new Error("Please switch to Solana Testnet in your Phantom wallet before proceeding.");
                // }

                // Create a new transaction
                const transaction = new solanaWeb3.Transaction();

                // Create transfer instruction
                const instruction = solanaWeb3.SystemProgram.transfer({
                    fromPubkey: publicKey,
                    toPubkey: new solanaWeb3.PublicKey(transactionDetails.to),
                    lamports: solanaWeb3.LAMPORTS_PER_SOL * transactionDetails.amount
                });

                // Add instruction to transaction
                transaction.add(instruction);

                // Get recent blockhash
                const { blockhash } = await connection.getLatestBlockhash();
                transaction.recentBlockhash = blockhash;

                // Set the paying account
                transaction.feePayer = publicKey;

                // Sign and send the transaction
                const { signature } = await window.solana.signAndSendTransaction(transaction);

                console.log("Transaction sent:", signature);
                alert("Testnet transaction sent successfully! Signature: " + signature);

                // Wait for confirmation
                const confirmation = await connection.confirmTransaction(signature);
                console.log("Transaction confirmed:", confirmation);
                alert("Testnet transaction confirmed successfully!");
            } catch (error) {
                console.error("Error:", error);
                alert("Error sending transaction: " + error.message);
            }
        }


        window.initiateTransaction = initiateTransaction;

document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('connectToPhantom');
    button.addEventListener('click', connectToPhantom);
});

document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('initiateTransaction');
    button.addEventListener('click', initiateTransaction);
});
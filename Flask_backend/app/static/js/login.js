import { connectToPhantom } from './phantom_connect.js';

async function handleWalletConnection() {
    try {
        const publicKey = await connectToPhantom();
        console.log('Connected to wallet. Public key:', publicKey);

        const response = await fetch('/api/publickey', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ publicKey }),
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Server response:', data);
            // Here you might want to redirect the user or update the UI
        } else {
            throw new Error(data.error || 'Failed to send public key to server');
        }

    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const connectButton = document.getElementById('connectWallet');
    if (connectButton) {
        connectButton.addEventListener('click', handleWalletConnection);
    } else {
        console.error("Connect to Wallet button not found");
    }
});
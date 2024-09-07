import { connectToPhantom } from './phantom_connect.js';
const { Connection, PublicKey, LAMPORTS_PER_SOL } = solanaWeb3;

const connectButton = document.getElementById('connectWallet');


async function handleWalletConnection() {
    try {
        const publicKey = await connectToPhantom();

        

        console.log('Connected to wallet. Public key:', publicKey);
        
        const Connection_request_url = "/login/"+ temp_code;
        
        const connection = new Connection('https://mainnet.helius-rpc.com/?api-key=5f413c9c-5af3-4a7e-bfc3-e0bc546b9a3e');

        // Fetch the balance
        // const balance = await connection.getBalance(new PublicKey(publicKey));
        // const solBalance = balance / LAMPORTS_PER_SOL;

        // USDC token address on Solana mainnet
        const USDC_MINT = new PublicKey('EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v');

        // Fetch the USDC token account
        const tokenAccounts = await connection.getParsedTokenAccountsByOwner(
            new solanaWeb3.PublicKey(publicKey),
            { mint: USDC_MINT }
        );

        let usdcBalance = 0;
        if (tokenAccounts.value.length > 0) {
            usdcBalance = tokenAccounts.value[0].account.data.parsed.info.tokenAmount.uiAmount;
        }
        console.log('USDC balance:', usdcBalance, 'USDC');
        // show only first 10 lettets of public key
        
        connectButton.textContent = String(publicKey).substring(0, 10) + '...';

        connectButton.classList.add('connected');

        const response = await fetch(Connection_request_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ publicKey,balance: usdcBalance  }),
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Server response:', data);
            // Here you might want to redirect the user or update the UI
            triggerMergeAnimation();

            showSnackbar();
        } else {
            throw new Error(data.error || 'Failed to send public key to server');
        }

    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    }
}

function showSnackbar() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
}

function triggerMergeAnimation() {
    const container = document.querySelector('.image-container');
    container.classList.add('merged');

    setTimeout(() => {
        container.classList.add('hidden');
        document.getElementById('tick-svg').style.display = 'block';
    }, 1000); // Adjust timing as needed (1000ms = 1s)
}


document.addEventListener('DOMContentLoaded', () => {
    const connectButton = document.getElementById('connectWallet');
    if (connectButton) {
        connectButton.addEventListener('click', handleWalletConnection);
    } else {
        console.error("Connect to Wallet button not found");
    }
});
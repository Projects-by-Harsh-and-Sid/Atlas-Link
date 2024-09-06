const { Connection, PublicKey } = require('@solana/web3.js');

async function connectToPhantom() {
    if (typeof window.solana === 'undefined') {
        throw new Error("Phantom wallet is not installed!");
    }

    try {
        const resp = await window.solana.connect();
        const publicKey = resp.publicKey.toString();
        console.log("Connected to Phantom. Public key:", publicKey);
        return publicKey;
    } catch (err) {
        console.error("Error connecting to Phantom:", err);
        throw new Error("Failed to connect to Phantom wallet.");
    }
}

module.exports = { connectToPhantom };
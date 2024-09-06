



export async function connectToPhantom() {
    if (typeof window.solana === 'undefined') {
        throw new Error("Phantom wallet is not installed!");
    }

    try {
        console.log("Connecting to Phantom...");
        const resp = await window.solana.connect();
        console.log("Connected to Phantom. Public key:", resp.publicKey.toString());
        return resp.publicKey;
    } catch (err) {
        console.error("Error connecting to Phantom:", err);
        throw new Error("Failed to connect to Phantom wallet.");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('connectToPhantom');
    button.addEventListener('click', connectToPhantom);
});
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
// add event listener whenever you use directly function call to button. for using this function as a module, you don't add event listener
//as it wont have any id to refer to. if you want to add make sure the id of the button is always connectToPhantom and on the import file dont 
// add an event listener



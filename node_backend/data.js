const { Connection, clusterApiUrl, PublicKey } = require('@solana/web3.js');
const { GmClientService } = require('@staratlas/factory');
const fs = require('fs');


async function main() {
    const connection = new Connection('https://mainnet.helius-rpc.com/?api-key=5f413c9c-5af3-4a7e-bfc3-e0bc546b9a3e');
    // Replace with your actual program ID
    const programId = new PublicKey('traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg');

    const gmClientService = new GmClientService();

    try {
        const allOrders = await gmClientService.getAllOpenOrders(connection, programId);
        console.log('All open orders:', allOrders);
        // print len of orders
        console.log('Number of open orders:', allOrders.length);
        console.log('All open orders:');

        // save this to json
        fs.writeFileSync('open_orders.json', JSON.stringify(allOrders, null, 2));
        
    } catch (error) {
        console.error('Error:', error);
    }
}

main();

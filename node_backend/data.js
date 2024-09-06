const { Connection, PublicKey } = require('@solana/web3.js');
const { GmClientService } = require('@staratlas/factory');
const express = require('express');
const fs = require('fs');

// Create an Express app
const app = express();
const port = 3000;

// Replace with your actual Solana RPC endpoint and program ID
const connection = new Connection('https://mainnet.helius-rpc.com/?api-key=5f413c9c-5af3-4a7e-bfc3-e0bc546b9a3e');
const programId = new PublicKey('traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg');
const gmClientService = new GmClientService();

// Define a route to get all open orders
app.get('/api/get_open_orders', async (req, res) => {
    try {
        const allOrders = await gmClientService.getAllOpenOrders(connection, programId);
        
        // Save the open orders to a file
        fs.writeFileSync('open_orders.json', JSON.stringify(allOrders, null, 2));

        // Send the orders as the API response
        res.json({
            message: 'Open orders retrieved successfully',
            orders: allOrders,
            count: allOrders.length
        });

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({
            message: 'An error occurred while fetching open orders',
            error: error.toString()
        });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

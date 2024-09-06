const { Connection, PublicKey } = require('@solana/web3.js');
const { GmClientService, Factory  } = require('@staratlas/factory');
const express = require('express');
const fs = require('fs');

// Create an Express app
const app = express();
const port = 3000;

const factory = Factory;

// Replace with your actual Solana RPC endpoint and program ID
const connection = new Connection('https://mainnet.helius-rpc.com/?api-key=5f413c9c-5af3-4a7e-bfc3-e0bc546b9a3e');
const programId = new PublicKey('traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg');
const gmClientService = new GmClientService();

// Define a route to get all open orders
app.get('/api/get_all_open_orders', async (req, res) => {
    try {
        const allOrders = await gmClientService.getAllOpenOrders(connection, programId);
        
        // Save the open orders to a file
        // fs.writeFileSync('open_orders.json', JSON.stringify(allOrders, null, 2));

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


app.post('/api/get_open_orders_from_asset', async (req, res) => {
    try {


        // get asse_id from request
        let assetId = req.query.asset_id;

        assetId = new PublicKey(assetId);

        const allOrders = await gmClientService.getOpenOrdersForAsset(connection,assetId ,programId);
        
        // Save the open orders to a file
        // fs.writeFileSync('open_orders.json', JSON.stringify(allOrders, null, 2));

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

app.post('/api/get_account_details', async (req, res) => {
    try {
        // Get the account parameter from request query
        const account = req.query.account;

        console.log("account",account);

        if (!account) {
            return res.status(400).json({
                message: 'Account parameter is required'
            });
        }

        // Convert the account string to a PublicKey object
        const publicKey = new PublicKey(account);

        // Fetch account details using the publicKey
        const accountDetails = await factory.getAccountInfo(connection, publicKey);
        // Send the orders as the API response
        res.json({
            message: 'Account retrieved successfully',
            account: accountDetails,
            count: accountDetails.length
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

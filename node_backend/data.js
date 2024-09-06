const { Connection, PublicKey } = require('@solana/web3.js');
const { GmClientService, getPlayer } = require('@staratlas/factory');
const express = require('express');
const fs = require('fs');

// Create an Express app
const app = express();
const port = 3000;

// const factory = Factory;

// Replace with your actual Solana RPC endpoint and program ID
const connection = new Connection('https://mainnet.helius-rpc.com/?api-key=5f413c9c-5af3-4a7e-bfc3-e0bc546b9a3e');
const marketplace_programId = new PublicKey('traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg');
const gmClientService = new GmClientService();

const factiondata_programid = new PublicKey('FACTNmq2FhA2QNTnGM2aWJH3i7zT3cND5CgvjYTjyVYe');
const playeritems_programid = new PublicKey('pv1ttom8tbyh83C1AVh6QH2naGRdVQUVt3HY1Yst5sv');
const playerprofile_programid = new PublicKey('pprofELXjL5Kck7Jn5hCpwAL82DpTkSYBENzahVtbc9');



// Define a route to get all open orders
app.get('/api/get_all_open_orders', async (req, res) => {
    try {
        const allOrders = await gmClientService.getAllOpenOrders(connection, marketplace_programId);
        
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

        const allOrders = await gmClientService.getOpenOrdersForAsset(connection,assetId ,marketplace_programId);
        
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

// app.post('/api/get_account_details', async (req, res) => {
//     try {
//         // Get the account parameter from request query
//         const account = req.query.account;

//         console.log("account",account);

//         if (!account) {
//             return res.status(400).json({
//                 message: 'Account parameter is required'
//             });
//         }

//         // Convert the account string to a PublicKey object
//         const publicKey = new PublicKey(account);

//         // Fetch account details using the publicKey
//         const accountDetails = await getPlayer(connection, publicKey,playerprofile_programid);
//         // Send the orders as the API response
//         res.json({
//             message: 'Account retrieved successfully',
//             account: accountDetails,
//             count: accountDetails.length
//         });

//     } catch (error) {
//         console.error('Error:', error);
//         res.status(500).json({
//             message: 'An error occurred while fetching open orders',
//             error: error.toString()
//         });
//     }
// });

app.get('/api/initiate_transaction', async (req, res) => {
    try {
        // Extract parameters from the request
        const { 
            orderCreator,
            itemMint,
            quoteMint,
            quantity,
            uiPrice,
            programId,
            orderSide
        } = req.query;

        // Validate input parameters
        if (!orderCreator || !itemMint || !quoteMint || !quantity || !uiPrice || !programId || !orderSide) {
            return res.status(400).json({ message: 'Missing required parameters' });
        }

        // Convert parameters to appropriate types
        const orderCreatorPubkey = new PublicKey(orderCreator);
        const itemMintPubkey = new PublicKey(itemMint);
        const quoteMintPubkey = new PublicKey(quoteMint);
        const programIdPubkey = new PublicKey(programId);
        const quantityNum = parseInt(quantity);
        const uiPriceNum = parseFloat(uiPrice);
        const orderSideEnum = orderSide.toLowerCase() === 'sell' ? OrderSide.Sell : OrderSide.Buy;

        // Get the price in the correct format
        const price = await gmClientService.getBnPriceForCurrency(
            connection,
            uiPriceNum,
            quoteMintPubkey,
            programIdPubkey
        );

        // Get the initialize order transaction
        const orderTx = await gmClientService.getInitializeOrderTransaction(
            connection,
            orderCreatorPubkey,
            itemMintPubkey,
            quoteMintPubkey,
            quantityNum,
            price,
            programIdPubkey,
            orderSideEnum
        );

        // Serialize the transaction
        const serializedTransaction = orderTx.serialize({requireAllSignatures: false}).toString('base64');

        res.json({
            message: 'Transaction created successfully',
            transaction: serializedTransaction,
            orderCreator: orderCreator,
            itemMint: itemMint,
            quoteMint: quoteMint,
            quantity: quantityNum,
            uiPrice: uiPriceNum,
            programId: programId,
            orderSide: orderSide
        });

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({
            message: 'An error occurred while creating the transaction',
            error: error.toString()
        });
    }
});







// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

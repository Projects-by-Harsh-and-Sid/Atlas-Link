const { PublicKey } = require('@solana/web3.js');
const { GmClientService } = require('@staratlas/factory');

const gmClientService = new GmClientService();

async function initiateTransaction(connection, params) {
    const { 
        orderCreator,
        itemMint,
        quoteMint,
        quantity,
        uiPrice,
        programId,
        orderSide
    } = params;

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
    return orderTx.serialize({requireAllSignatures: false}).toString('base64');
}

module.exports = { initiateTransaction };
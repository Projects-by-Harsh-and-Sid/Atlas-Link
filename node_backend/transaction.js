const { PublicKey ,Transaction } = require('@solana/web3.js');
const { GmClientService,OrderSide, Order  } = require('@staratlas/factory');

const gmClientService = new GmClientService();

// async function signAndSendTransaction(transaction, connection) {
//     const provider = await window.solana;
//     if (!provider) {
//         throw new Error("Phantom provider not found");
//     }

//     try {
//         // Add a recent blockhash to the transaction
//         transaction.recentBlockhash = (await connection.getRecentBlockhash()).blockhash;
        
//         // Request Phantom to sign the transaction
//         const signedTransaction = await provider.signTransaction(transaction);
        
//         // Send the signed transaction
//         const signature = await connection.sendRawTransaction(signedTransaction.serialize());
        
//         console.log("Transaction sent:", signature);
//         return signature;
//     } catch (error) {
//         console.error("Error signing and sending transaction:", error);
//         throw error;
//     }
// }


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
    const Orderside = OrderSide.Sell;

    console.log("orderCreatorPubkey",orderCreatorPubkey);
    console.log("itemMintPubkey",itemMintPubkey);
    console.log("quoteMintPubkey",quoteMintPubkey);
    console.log("programIdPubkey",programIdPubkey);
    console.log("quantityNum",quantityNum);
    console.log("uiPriceNum",uiPriceNum);
    console.log("Orderside",Orderside);

    console.log("connection",connection);
    // Get the price in the correct format

    const price = await gmClientService.getBnPriceForCurrency(
        connection,
        uiPriceNum,
        quoteMintPubkey,
        programIdPubkey
    );

    // const allCurrencyInfo = await gmClientService.getRegisteredCurrencies(
    //     connection,
    //     programIdPubkey,
    //   );

    //   console.log("allCurrencyInfo",allCurrencyInfo);
    //   const { decimals } = allCurrencyInfo.find(
    //     (info) => info.mint.toString() === quoteMintPubkey.toString(),
    //   );
    //   console.log("decimals",decimals);
    // // console.log("price",price);

    // const price = 1;

    // Get the initialize order transaction
    const orderTx = await gmClientService.getInitializeOrderTransaction(
        connection,
        orderCreatorPubkey,
        itemMintPubkey,
        quoteMintPubkey,
        quantityNum,
        price,
        programIdPubkey,
    OrderSide
    );

    console.log("orderTx",orderTx);

    // Sign and send the transaction
    
    // Serialize the transaction
    const transaction = orderTx.transaction;
  
    // Add a recent blockhash to the transaction
    const { blockhash } = await connection.getRecentBlockhash();
    transaction.recentBlockhash = blockhash;
    transaction.feePayer = new PublicKey(orderCreator);
  
    // Serialize the transaction
    const serializedTransaction = transaction.serialize({requireAllSignatures: false}).toString('base64');
    console.log("serializedTransaction",serializedTransaction);
    return {
      serializedTransaction,
      signers: orderTx.signers
    };
  }
  
module.exports = { initiateTransaction };
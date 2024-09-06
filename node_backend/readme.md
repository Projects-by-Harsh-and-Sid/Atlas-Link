# Solana Open Orders API

This project is a Node.js application that provides an API for retrieving open orders and account details from the Solana blockchain, specifically for the Star Atlas game.

## Features

- Retrieve all open orders from the Star Atlas marketplace
- Get open orders for a specific asset
- Fetch account details for a given public key

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Node.js installed (version 12.x or higher recommended)
- npm (Node Package Manager) installed

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/solana-open-orders-api.git
   cd solana-open-orders-api
   ```

2. Install the dependencies:
   ```
   npm install
   ```

3. Create a `.env` file in the root directory and add your Helius RPC endpoint API key:
   ```
   HELIUS_API_KEY=your_api_key_here
   ```

## Configuration

The application uses the following Solana program IDs and connections:

- Solana RPC Endpoint: `https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY`
- Marketplace Program ID: `traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg`
- Faction Data Program ID: `FACTNmq2FhA2QNTnGM2aWJH3i7zT3cND5CgvjYTjyVYe`
- Player Items Program ID: `pv1ttom8tbyh83C1AVh6QH2naGRdVQUVt3HY1Yst5sv`

Ensure these values are correct for your use case.

## Usage

To start the server, run:

```
npm start
```

The server will start on `http://localhost:3000`.

### API Endpoints

1. Get All Open Orders
   - Method: GET
   - Endpoint: `/api/get_all_open_orders`
   - Description: Retrieves all open orders from the Star Atlas marketplace.

2. Get Open Orders for a Specific Asset
   - Method: POST
   - Endpoint: `/api/get_open_orders_from_asset`
   - Query Parameter: `asset_id` (Solana public key of the asset)
   - Description: Retrieves open orders for a specific asset.

3. Get Account Details
   - Method: POST
   - Endpoint: `/api/get_account_details`
   - Query Parameter: `account` (Solana public key of the account)
   - Description: Fetches account details for a given public key.


## API endpoints for Galaxy APIs



## Error Handling

The API includes basic error handling. If an error occurs, the server will respond with a 500 status code and an error message.

## Resoucres

https://github.com/staratlasmeta/factory/blob/main/src/factions.ts

https://build.staratlas.com/dev-resources/apis-and-data


https://www.npmjs.com/package/@staratlas/factory


https://build.staratlas.com/dev-resources/apis-and-data/galactic-marketplace
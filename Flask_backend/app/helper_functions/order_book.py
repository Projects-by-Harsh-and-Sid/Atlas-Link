

import numpy as np


def process_orders_assets(data):
    usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    buy_orders = []
    sell_orders = []

    for order in data.get('orders', []):
        if order['currencyMint'] == usdc_mint:
            price_usdc = int(order['price'], 16) / 10**order['currencyDecimals']
            processed_order = {
                'id': order['id'],
                'price_usdc': price_usdc,
                'quantity': order['orderQtyRemaining']
            }
            
            if order['orderType'] == 'buy':
                buy_orders.append(processed_order)
            elif order['orderType'] == 'sell':
                sell_orders.append(processed_order)

    return {
        'buy_orders': sorted(buy_orders, key=lambda x: x['price_usdc'], reverse=True),
        'sell_orders': sorted(sell_orders, key=lambda x: x['price_usdc'])
    }

def calculate_orderbook_summary(orders):
    if not orders:
        return {
            'count': 0,
            'min_price': None,
            'max_price': None,
            'avg_price': None,
            'median_price': None,
            'total_quantity': 0,
            'price_quartiles': None,
            'price_histogram': None,
        }
    
    prices = [order['price_usdc'] for order in orders]
    quantities = [order['quantity'] for order in orders]
    
    hist, bin_edges = np.histogram(prices, bins=10)
    
    return {
        'count': len(orders),
        'min_price': float(min(prices)),
        'max_price': float(max(prices)),
        'avg_price': float(np.mean(prices)),
        'median_price': float(np.median(prices)),
        'total_quantity': int(sum(quantities)),
        'price_quartiles': [float(q) for q in np.percentile(prices, [25, 50, 75])],
        'price_histogram': {
            'counts': hist.tolist(),
            'bin_edges': bin_edges.tolist()
        },
    }
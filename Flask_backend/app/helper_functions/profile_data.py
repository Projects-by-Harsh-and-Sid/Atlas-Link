import requests

def format_balance(balance):
    return f"{balance:.6f}"  # Format to 6 decimal places

def format_total_value(value):
    return f"{value:.3f}"  # Format to 3 decimal places

def get_item_details(mint, reverse_map):
    item_details = reverse_map.get(mint)
    if not item_details:
        return None
    return {
        "name": item_details.get("name", "Unknown"),
        "symbol": item_details.get("symbol", "Unknown"),
        "itemType": item_details.get("itemType", "Unknown"),
        "rarity": item_details.get("rarity", "Unknown"),
        "category": item_details.get("category", "Unknown"),
        "image": item_details.get("image", "")
    }

def fetch_star_atlas_data(account):
    star_atlas_url = f"https://galaxy.staratlas.com/players/{account}"
    response = requests.get(star_atlas_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Star Atlas API. Status code: {response.status_code}")
    return response.json()

def format_player_data(data):
    return {
        "publicKey": data["publicKey"],
        "avatarId": data["avatarId"],
        "factionRank": data["factionRank"],
        "rank": data["rank"],
        "country": data["country"],
        "registrationDate": data["registrationDate"],
        "items": [],
        "total_value_of_account": "0.000"  # Initialize with zero
    }

def process_player_items(data, reverse_map):
    items = []
    total_value = 0
    for balance in data["balances"]:
        mint = balance["mint"]
        item_details = get_item_details(mint, reverse_map)
        if item_details and item_details["category"] != "resource":  # Skip resources
            quantity = float(balance["quantity"])
            value_per_asset = float(balance["valuePerAsset"])
            total_asset_value = quantity * value_per_asset
            total_value += total_asset_value
            formatted_item = {
                "quantity": format_balance(quantity),
                "valuePerAsset": format_balance(value_per_asset),
                "totalValue": format_total_value(total_asset_value),
                **item_details
            }
            items.append(formatted_item)
    
    # Sort items based on total value (descending order)
    items.sort(key=lambda x: float(x["totalValue"]), reverse=True)
    
    return items, format_total_value(total_value)

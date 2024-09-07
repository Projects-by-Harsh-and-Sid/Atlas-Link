from flask import Flask
from app.instructions.generate_instructions import get_instruction_dictionary

import yaml
import json

app = Flask(__name__)


info = yaml.load(open('info.yaml'), Loader=yaml.FullLoader)

app.config["URL"] = info['ngrok_url']
app.config["Atlas_data"] = info['atlas_data']

app.config["Item_data"] = json.load(open(r'resources\detial_items.json'))
app.config["reverse_map"] = json.load(open(r'resources\reverse_map.json'))
app.config["user_pairs"] = {"abc123": "6Senu4mrPDM1Mb1xJYFXSDg2CggWkFLC9VCNzp1LEHBX",
                            "abc1234": "Ad8yNpE3seJKHoNstbDHjG5F5ZCapapuxtpKKMWPGML5"}
app.config["balance"] = {'6Senu4mrPDM1Mb1xJYFXSDg2CggWkFLC9VCNzp1LEHBX': 100}

TRANSACTION_PARAMS = {
    'orderCreator': '6Senu4mrPDM1Mb1xJYFXSDg2CggWkFLC9VCNzp1LEHBX',
    'itemMint': 'Ev3xUhc1Leqi4qR2E5VoG9pcxCvHHmnAaSRVPg485xAT',
    'quoteMint': 'ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx',
    'quantity': '1',
    'uiPrice': '10.5',
    'programId': 'traderDnaR5w6Tcoi3NFm53i48FTDNbGjBSZwWXDRrg',
    'orderSide': 'sell'
}


app.config["build_transactions"] = { "abc": TRANSACTION_PARAMS }
app.config['instructions'] = get_instruction_dictionary()



from app import (routes, 
                 data_routes, 
                 order_book, 
                 transactions, 
                 profile_data, 
                 item_data)

from app.instructions import instructions

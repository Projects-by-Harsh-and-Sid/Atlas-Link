from flask import Flask

import yaml
import json

app = Flask(__name__)


info = yaml.load(open('info.yaml'), Loader=yaml.FullLoader)

app.config["URL"] = info['ngrok_url']
app.config["Atlas_data"] = info['atlas_data']

app.config["Item_data"] = json.load(open(r'resources\detial_items.json'))
app.config["user_pairs"] = {"abc123": "6Senu4mrPDM1Mb1xJYFXSDg2CggWkFLC9VCNzp1LEHBX"}


from app import routes
from app import data_routes
from app import order_book
from app import transactions
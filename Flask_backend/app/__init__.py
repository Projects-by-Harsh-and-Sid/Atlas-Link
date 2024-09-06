from flask import Flask

import yaml


app = Flask(__name__)


info = yaml.load(open('info.yaml'), Loader=yaml.FullLoader)

app.config["URL"] = info['ngrok_url']
app.config["Atlas_data"] = info['atlas_data']

from app import routes
from app import data_routes
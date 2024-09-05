from flask import Flask

import yaml


app = Flask(__name__)


info = yaml.load(open('info.yaml'), Loader=yaml.FullLoader)

app.config["URL"] = info['ngrok_url']

from app import routes
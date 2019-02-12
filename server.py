from os import environ
from flask import Flask

app = Flask('warm-atoll-45971')
app.run(host= '0.0.0.0', port=environ.get('PORT'))
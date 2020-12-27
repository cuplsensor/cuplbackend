from backendapp.api.consumer.version import versioninfo
import os

f = open(os.path.join(os.path.dirname(__file__), 'logostr.txt'), 'r')
logostr = f.read()

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

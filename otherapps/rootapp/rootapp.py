from backendapp.api.consumer.version import versioninfo
import os

f = open(os.path.join(os.path.dirname(__file__), 'logostr.txt'), 'r')
logostr = f.read()

from flask import Flask
rootapp = Flask(__name__)

@rootapp.route('/')
def hello_world():
    return 'Hello, World!'

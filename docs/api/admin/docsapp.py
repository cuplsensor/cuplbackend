from flask import Flask, send_from_directory
docsapp = Flask(__name__)

@docsapp.route('/api.yaml')
def apiyaml():
    return send_from_directory('.', 'api.yaml')

@docsapp.route('/')
def index():
    return send_from_directory('.', 'index.html')

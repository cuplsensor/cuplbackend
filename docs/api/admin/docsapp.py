from flask import Flask, send_from_directory
docsapp = Flask(__name__)

@docsapp.route('/')
def index():
    return send_from_directory('.', 'index.html')
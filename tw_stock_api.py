from flask import Flask, jsonify
import time
from datetime import datetime
import pandas as pd
import requests
import json
import pymongo
from pymongo import MongoClient
import urllib
from sshtunnel import SSHTunnelForwarder
import os

app = Flask(__name__)
username = os.getenv("MONGODB_ACCOUNT")
password = os.getenv("MONGODB_PASSWORD")
mongodb_host = os.getenv("MONGODB_HOST")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 0
    })

@app.route('/tw_stock/<string:stock_id>/<int:kline_type>', methods=['GET'])
def get_youbike_sno_data(stock_id, kline_type):
    client = MongoClient('mongodb://{username}:{password}@{host}'.format(username=username, password=password, host=mongodb_host))
    db = client['tw_stock']
    collection = db['kline']
    result = collection.find({'stock_id': stock_id, 'kline_type': kline_type}, {'_id': False})
    ls_result = list(result)
    return json.dumps({
        'status': 0,
        'data': [{
            'open': data['open'],
            'high': data['high'],
            'low': data['low'],
            'close': data['close'],
            'volume': data['volume'],
            'stock_id': data['stock_id'],
            'stock_name': data['stock_name'],
            'kline_type': data['kline_type'],
            'datetime': str(data['datetime'])
        } for data in ls_result]
    }, ensure_ascii=False)

app.run(host='0.0.0.0', port=5566)


from flask import Flask
from flask.ext.pymongo import PyMongo, MongoClient
import base64

app = Flask(__name__)

client = MongoClient('<YOUR-MONGO-URI>')
mongo = client['<YOUR-MONGODB-NAME']


""" Routes """
@app.route("/")
def hello():
    headers = create_headers()
    columns = create_columns()
    data = {'some_id': 1, 'headers': headers, 'columns': columns}
    user = mongo.db.users
    user.insert(data)
    return 'added data'


@app.route("/get")
def get():
    user = mongo.db.users
    data = user.find_one({'some_id': 1})
    headers = decode_headers(data['headers'])
    columns = decode_columns(data['columns'])
    print headers
    for col in columns:
        print '*' * 60
        print col
    return 'get'


""" Functions """
def decode_headers(headers):
    headers = base64.b64decode(headers)
    headers = bytearray(headers)
    return list(headers)

def decode_columns(columns):
    result = []
    for col in columns:
        col = base64.b64decode(col)
        col = bytearray(col)
        result.append(list(col))
    return result


def create_headers():
    big_array = [((i + 1) % 255) for i in xrange(500)]
    big_array = bytearray(big_array)
    big_array = base64.b64encode(big_array)
    return big_array

def create_columns():
    big_matrix = [[((y + 1) % 255) for y in xrange(500)] for x in xrange(10000)]

    result = []
    for row in big_matrix:
        # row=bytes(row)
        # result2.append(bytes(row))
        row = bytearray(row)
        result.append(base64.b64encode(row))
    return result

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
    result = [((i + 1) % 255) for i in xrange(500)]
    result = bytearray(result)
    result = base64.b64encode(result)
    return result

def create_columns():
    result = [[((y + 1) % 255) for y in xrange(500)] for x in xrange(10000)]
    # result = [['a' for y in xrange(500)] for x in xrange(10000)]

    result2 = []
    for row in result:
        # row=bytes(row)
        # result2.append(bytes(row))
        row = bytearray(row)
        result2.append(base64.b64encode(row))
    return result2

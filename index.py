'''
 Created on Fri Oct 19 2018

 The MIT License (MIT)
 Copyright (c) 2018 joans321

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
import json

HTTP_URL = "/api/v1/"

app = Flask(__name__)
api = Api(app)
db_client = MongoClient('localhost', 27017)
finance_db = db_client['finance']

def json_status(status, message):
    return {'status': status, 'message': message}

def json_ok(message):
    return json_status(0, message)

def json_failed(message):
    return json_status(-1, message)

def db_tojson(result):
    return json.loads(json_util.dumps(result))

def acc_parser(required):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=required, 
        location='json', help='username')
    parser.add_argument('password', type=str, required=required,
        location='json', help='password')
    parser.add_argument('type', type=str, required=required,
        location='json', help='ctp')
    parser.add_argument('brokerId', type=str, required=required,
        location='json', help='brokerId')
    parser.add_argument('mdserver', type=str, required=required,
        location='json', help='mdserver=tcp://180.168.146.187:10031')
    parser.add_argument('tdserver', type=str, required=required,
        location='json', help='tdserver=tcp://180.168.146.187:10030')
    return parser

class Accounts(Resource):
    def __init__(self):
        self.accounts = finance_db['account']
        self.parser = acc_parser(True)
        super(Accounts, self).__init__()

    def same_account(self, args):
        result = self.accounts.find_one({
            'username': args['username'],
            'tdserver': args['tdserver'],
            'type': args['type']})

        if result is not None:
            return True
        return False

    ## Get all accounts
    def get(self):
        result = self.accounts.find()
        status = json_ok('get all accounts success')
        status['accounts'] = db_tojson(result)
        return status

    ##  Add Account
    def post(self):
        args = self.parser.parse_args()
        if self.same_account(args):
            return json_failed('add account failed, account exists'), 409

        self.accounts.insert_one(args)
        return json_ok("add account success")

class Account(Resource):
    def __init__(self):
        self.accounts = finance_db['account']
        self.parser = acc_parser(False)
        super(Account, self).__init__()

    def get(self, id):
        print(id)
        acc = self.accounts.find_one({'_id': ObjectId(id)})
        if acc is None:
            return http_failed('account not exists'), 404

        status = json_ok('get account success')
        status['accounts'] = db_tojson(acc)
        return status
        
    def put(self, id):
        accounts[id] = request.form['data']
        return {id : accounts[id]}
    
    def delete(self, id):
        return '', 204

api.add_resource(Accounts, HTTP_URL + 'accounts', endpoint='accounts')
api.add_resource(Account, HTTP_URL + 'account/<string:id>', endpoint = 'account')

if __name__ == '__main__':
    app.run(debug=True)

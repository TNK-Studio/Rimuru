# -*- coding: utf-8 -*-
__author__ = 'gzp'

import json
from flask import Flask, request, Response

app = Flask(__name__)

book_data = [{
    'id': 1,
    'name': 'A'
}, {
    'id': 2,
    'name': 'B'
}, {
    'id': 3,
    'name': 'C'
}]


@app.route("/api/books", methods=['GET', ])
def books():
    name = request.args.get('name')
    data = book_data
    if name:
        data = [each for each in filter(lambda r: r['name'] == name, book_data)]

    return Response(json.dumps(data), mimetype='application/json')


@app.route('/api/books/<int:id>', methods=['GET', ])
def book_detail(id):
    data = [each for each in filter(lambda r: r['id'] == id, book_data)]
    if data:
        response = Response(json.dumps(data[0]), mimetype='application/json')
    else:
        response = Response(json.dumps({'msg': 'Not Found'}), mimetype='application/json', status=404)

    return response

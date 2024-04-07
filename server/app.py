#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

#GET /bakeries: returns a list of JSON objects for all bakeries in the database.
@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [bakery.serialize() for bakery in bakeries]
    return jsonify(bakery_list)

#GET /bakeries/<int:id>: returns a single bakery as JSON with its baked goods nested in a list. Use the id from the URL to look up the correct bakery.
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if bakery is None:
        abort(404)  # Returns a 404 error response if bakery is None
    return jsonify(bakery.serialize())

#GET /baked_goods/by_price: returns a list of baked goods as JSON, sorted by price in descending order.
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_data = [baked_good.serialize() for baked_good in baked_goods]
    return jsonify(baked_goods_data)

#GET /baked_goods/most_expensive: returns the single most expensive baked good as JSON.
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return jsonify(most_expensive.serialize())

if __name__ == '__main__':
    app.run(port=5555, debug=True)

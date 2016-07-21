#!/usr/bin/python3
#
# Copyright (c) 2016, Fabian Affolter <fabian@affolter-engineering.ch>
# Released under the MIT license. See LICENSE file for details.
#
import random
from datetime import datetime

from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask('home-assistant-rest-tester')
api = Api(app)

state1 = [1, 0]
state2 = ['1', '0']
state3 = ['true', 'false']
state4 = ['TRUE', 'FALSE']
state5 = ['on', 'off']
state6 = ['Open', 'Close']
sensor2 = {'name': 'Sensor2', 'value': 0}

class Api(Resource):
    def get(self):
        return {'hello': 'home-assistant'}

api.add_resource(Api, '/')

# Binary sensor
class BinarySensor(Resource):
    def get(self):
        return {'name': 'Binary sensor',
                'state1': random.choice(state1),
                'state2': random.choice(state2),
                'state3': {'open': random.choice(state3),
                           'timestamp': str(datetime.now())},
                'state4': random.choice(state4),
                'state5': random.choice(state5),
                'state6': random.choice(state6),
                }

api.add_resource(BinarySensor, '/binary_sensor')

# Sensor
class Sensor(Resource):
    def get(self):
        return {'name': 'Sensor',
                'value': random.randrange(0, 30, 1)}

api.add_resource(Sensor, '/sensor')

# Sensor2 for POST
parser = reqparse.RequestParser()
parser.add_argument('value')

class Sensor2(Resource):
    def get(self):
        return sensor2

    def post(self):
        args = parser.parse_args()
        sensor2['value'] = int(args['value'])
        return sensor2

api.add_resource(Sensor2, '/sensor2')


# aREST
class Arest(Resource):
    def get(self):
        return {'message': 'Pin D6 set to 1',
                'id': 'test',
                'name': 'ha-arest',
                'connected': True}

api.add_resource(Arest, '/arest_sensor')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

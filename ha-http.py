# Copyright (c) 2016-2023, Fabian Affolter <fabian@affolter-engineering.ch>
# Released under the ASL 2.0 license. See LICENSE.md file for details.
#
import random
from datetime import datetime

from flask import Flask, jsonify, Response, render_template
from flask_restful import Resource, Api, reqparse, request
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth

app = Flask('home-assistant-rest-tester')
app.config[
    'SECRET_KEY'] = 'c846b95c4eb4f8f5a76e52d8fdcee815e7f1b19f799aed511a0616115bb87694'
auth_basic = HTTPBasicAuth()
auth_digest = HTTPDigestAuth()

api = Api(app)

state1 = [1, 0]
state2 = ['1', '0']
state3 = ['true', 'false']
state4 = ['TRUE', 'FALSE']
state5 = ['on', 'off']
state6 = ['Open', 'Close']
sensor2 = {'name': 'Sensor2', 'value': 0}

WEATHER_DATA = {
    'name': 'AwesomeWeather',
    'details': {'lat': 46.941257, 'long': 7.431203},
    'temp': None,
    'hum': None,
    'sun': None,
    'led': None,
}

USERS = {
    'ha1': 'test',
    'ha2': 'test'
}


parser = reqparse.RequestParser()
parser.add_argument('value')


def generate_sensor():
    return random.randrange(0, 30, 1)


@auth_basic.get_password
@auth_digest.get_password
def get_pw(username):
    if username in USERS:
        return USERS.get(username)
    return None


class Api(Resource):
    def get(self):
        return {'hello': 'home-assistant'}


api.add_resource(Api, '/')


# IP address
class IpAddress(Resource):
    def get(self):
        return jsonify({'ip': request.remote_addr})


api.add_resource(IpAddress, '/ip')


# Condition
class AwesomeWeather(Resource):
    def get(self):
        WEATHER_DATA['temp'] = generate_sensor()
        WEATHER_DATA['hum'] = generate_sensor()
        WEATHER_DATA['sun'] = random.choice(state2)
        return WEATHER_DATA

    def post(self):
        args = parser.parse_args()
        print(args)
        WEATHER_DATA['led'] = int(args['value'])
        return WEATHER_DATA


api.add_resource(AwesomeWeather, '/weather')


# Binary sensor
class BinarySensor(Resource):
    def get(self):
        return random.choice(state3)


api.add_resource(BinarySensor, '/binary_sensor')


class BinarySensor1(Resource):
    def get(self):
        return {
            'name': 'Binary sensor',
            'state1': random.choice(state1),
            'state2': random.choice(state2),
            'state3': {'open': random.choice(state3),
                       'timestamp': str(datetime.now())},
            'state4': random.choice(state4),
            'state5': random.choice(state5),
            'state6': random.choice(state6),
            'state_6': random.choice(state6),
        }


api.add_resource(BinarySensor1, '/binary_sensor1')


# Sensor
class Sensor(Resource):
    def get(self):
        return {'name': 'Sensor', 'value': generate_sensor()}


api.add_resource(Sensor, '/sensor')


class Sensor1(Resource):
    def get(self):
        return {
            'sensor+data': generate_sensor(),
            'sensor_data': generate_sensor(),
            'sensor-data': generate_sensor(),
            'string': 'a string',
            'float': float(1.00000001)
        }


api.add_resource(Sensor1, '/sensor1')


class SensorData(Resource):
    def get(self):
        return Response(str(generate_sensor()), mimetype='application/text')


api.add_resource(SensorData, '/sensor_data.txt')


class Sensor2(Resource):
    def get(self):
        value = generate_sensor()
        return render_template('sensor.html', name='Sensor2', value=value)


api.add_resource(Sensor2, '/sensor2')


class Sensor3(Resource):
    def get(self):
        return '12'


api.add_resource(Sensor3, '/sensor3')


class SensorAuth(Resource):
    @auth_basic.login_required
    def get(self):
        value = generate_sensor()
        return render_template('sensor.html', name='Sensor Auth', value=value)


api.add_resource(SensorAuth, '/sensor_auth')


# Switch POST for setting
switch_state = {'name': 'Switch', 'value': None}


class Switch(Resource):
    def get(self):
        return switch_state

    def post(self):
        args = parser.parse_args()
        switch_state['value'] = int(args['value'])
        return switch_state


api.add_resource(Switch, '/switch')

# Switch Auth POST for setting
switch_auth_state = {'name': 'Switch Auth', 'value': None}


class SwitchAuth(Resource):
    @auth_basic.login_required
    def get(self):
        return switch_auth_state

    @auth_basic.login_required
    def post(self):
        args = parser.parse_args()
        switch_state['value'] = int(args['value'])
        return switch_auth_state


api.add_resource(SwitchAuth, '/switch_auth')


# Authentication
class auth_basic(Resource):
    @auth_basic.login_required
    def get(self):
        print(request.headers)
        return {'name': 'Sensor', 'value': generate_sensor()}


api.add_resource(auth_basic, '/auth_basic')


class auth_digest(Resource):
    @auth_digest.login_required
    def get(self):
        return {'name': 'Sensor', 'value': generate_sensor()}


api.add_resource(auth_digest, '/auth_digest')


# aREST
class Arest(Resource):
    def get(self):
        return {
            'message': 'Pin D6 set to 1',
            'id': 'test',
            'name': 'ha-arest',
            'connected': True,
        }


api.add_resource(Arest, '/arest_sensor')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

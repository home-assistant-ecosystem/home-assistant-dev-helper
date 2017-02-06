#!/usr/bin/python3
#
# Copyright (c) 2016-2017, Fabian Affolter <fabian@affolter-engineering.ch>
# Released under the ASL 2.0 license. See LICENSE.md file for details.
#
import random

from flask import Flask, Response, render_template


app = Flask('home-assistant-web-tester')

def generate_sensor():
    return random.randrange(0, 30, 1)

@app.route('/')
def root():
    return 'Home Assistant Web Tester'


@app.route('/sensor_data.txt')
def sensor_data():
    return Response(str(generate_sensor()), mimetype='application/text')

@app.route('/sensor')
@app.route('/sensor/<name>')
def sensor(name=None):
    value = generate_sensor()
    return render_template('sensor.html', name=name, value=value)


@app.route('/sensor1')
def sensor1():
    return "12"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

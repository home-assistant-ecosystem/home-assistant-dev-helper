Home Assistant Developer Helper
===============================

This repository contains little helpers for testing and developing platform
and/or components for `Home Assistant <https://home-assistant.io>`__. 


REST (``ha-rest.py``)
---------------------

The `Flask-RESTful <http://flask-restful.readthedocs.io>`__ extension for 
`Flask <http://flask.pocoo.org/>`__ can be used to simulate devices locally. 

.. code:: bash

    $ ./ha-rest.py

Flask is running on Port 5000. The response contains various attributes with 
random assigned values.

.. code:: bash

    $ curl -X GET http://127.0.0.1:5000/binary_sensor
    {
        "name": "Binary sensor",
        "state1": 0,
        "state2": "0",
        "state3": {
            "open": "true",
            "timestamp": "2016-06-14 15:32:10.253225"
        },
        "state4": "FALSE",
        "state5": "off",
        "state6": "Close"
    }

A sample entry for a binary sensor for the ``configuration.yaml`` file could
like this:

.. code:: yaml

    binary_sensor:
      - platform: rest
        resource: http://127.0.0.1:5000/binary_sensor
        name: REST test
        sensor_class: opening
        value_template: '{{ value_json.state1 }}'

The available endpoints are:

- ``/binary_sensor``
- ``/binary_sensor1``
- ``/sensor``
- ``/weather``
- ``/sensor1``
- ``/sensor2`` incl. support for POST requests
- ``/auth_basic`` usable with username 'ha1' and password 'test1' or 'ha2'/'test2'
- ``/auth_digest`` usable with username 'ha1' and password 'test1' or 'ha2'/'test2'

Web (``ha-web.py``)
-------------------

This script provides a `Flask <http://flask.pocoo.org/>`__ based web server
that is storing sensor values in various ways. The server is running on
http://127.0.0.1:5000/

- ``/sensor`` and ``/sensor/<name>``
- ``/sensor_data.txt``


License
-------
``home-assistant-dev-helper`` is licensed under MIT, for more details check
LICENSE.


#!/usr/bin/python3
"""
Copyright (c) 2016-2023, Fabian Affolter <fabian@affolter-engineering.ch>

Released under the ASL 2.0 license. See LICENSE.md file for details.

This script creates and updates MQTT platforms which can be used through the
MQTT discovery in Home Assistant.
"""
import json
import random
import time
import paho.mqtt.client as mqtt

timestamp = int(time.time())

broker = "127.0.0.1"
port = 1883
topic_prefix = "homeassistant"

mqttclient = mqtt.Client("ha-mqtt-demo", protocol=mqtt.MQTTv311)
mqttclient.connect(broker, port=int(port))

entities = {
    "front_door": ["binary_sensor", {"name": "Front Door", "device_class": "motion"}],
    "back_door": ["binary_sensor", {"name": "Back Door"}],
    "temperature": ["sensor", {"name": "Temperature"}],
    "living_room": ["switch", {"name": "Living room"}],
    "bed_room": ["light", {"name": "Bed room"}],
}

commands = ["ON", "OFF"]

print("Demo is running... -> CTRL + C to shutdown")

# Setup the entities
for entity, value in entities.items():
    topic = "{}/{}/{}/{}".format(topic_prefix, value[0], entity, "config")
    if value[0] not in ["binary_sensor", "sensor"]:
        value[1]["command_topic"] = "{}/{}/{}/{}".format(
            topic_prefix, value[0], entity, "set"
        )
    message = json.dumps(value[1])
    mqttclient.publish(topic, message)
    time.sleep(0.2)

# Change the state of the entities
while True:
    for entity, value in entities.items():
        topic = "{}/{}/{}/{}".format(topic_prefix, value[0], entity, "state")
        if value[0] in ["binary_sensor", "switch", "light"]:
            message = random.choices(["OFF", "ON"])[0]
        if value[0] in ["sensor"]:
            message = random.randint(5, 30)
        mqttclient.publish(topic, message)
        time.sleep(1)

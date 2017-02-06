#!/usr/bin/python3
#
# Copyright (c) 2017, Fabian Affolter <fabian@affolter-engineering.ch>
# Released under the ASL 2.0 license. See LICENSE.md file for details.
#
import asyncio
import asyncws
import json

@asyncio.coroutine
def echo():
    websocket = yield from asyncws.connect('ws://localhost:8123/api/websocket')

    yield from websocket.send(json.dumps(
        {'id': 1, 'type': 'subscribe_events', 'event_type': 'state_changed'}))

    while True:
        message = yield from websocket.recv()
        if message is None:
            break
        print (message)

asyncio.get_event_loop().run_until_complete(echo())
asyncio.get_event_loop().close()


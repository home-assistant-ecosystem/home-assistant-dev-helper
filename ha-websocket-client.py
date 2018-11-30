#!/usr/bin/python3
#
# Copyright (c) 2017-2018, Fabian Affolter <fabian@affolter-engineering.ch>
# Released under the ASL 2.0 license. See LICENSE.md file for details.
#
import asyncio
import json

import asyncws

ACCESS_TOKEN = 'ABCDE'


async def main():
    """Simple echo WebSocket client for Home Assistant."""
    websocket = await asyncws.connect('ws://localhost:8123/api/websocket')

    await websocket.send(json.dumps(
        {'type': 'auth',
         'access_token': ACCESS_TOKEN}
    ))

    await websocket.send(json.dumps(
        {'id': 1, 'type': 'subscribe_events', 'event_type': 'state_changed'}
    ))

    while True:
        message = await websocket.recv()
        if message is None:
            break
        print (message)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

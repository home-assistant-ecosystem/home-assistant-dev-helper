#!/usr/bin/python3
#
# Copyright (c) 2017-2021, Fabian Affolter <fabian@affolter-engineering.ch>
# Released under the ASL 2.0 license. See LICENSE.md file for details.
#
import asyncio
import json

import asyncws

ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3ZDg2Mzc3NzIwYjQ0M2YyOWI2MzE2ZTdmMjI3Njc0OCIsImlhdCI6MTU0MzYwMTY1OCwiZXhwIjoxODU4OTYxNjU4fQ.uSatzdHOC-ozC9OnI0pUk63Mtuawy7bauRG6k-swP9g'


async def main():
    """Simple WebSocket client for Home Assistant."""
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

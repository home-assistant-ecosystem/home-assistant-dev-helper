#!/usr/bin/python3
#
# Copyright (c) 2018, Max Rydahl Andersen <max@xam.dk>
# Released under the ASL 2.0 license. See LICENSE.md file for details.
#
import asyncio
import json

import aiohttp

ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3ZDg2Mzc3NzIwYjQ0M2YyOWI2MzE2ZTdmMjI3Njc0OCIsImlhdCI6MTU0MzYwMTY1OCwiZXhwIjoxODU4OTYxNjU4fQ.uSatzdHOC-ozC9OnI0pUk63Mtuawy7bauRG6k-swP9g'


async def main():
    """Simple WebSocket client for Home Assistant."""
    async with aiohttp.ClientSession().ws_connect(
            'http://localhost:8123/api/websocket') as ws:
            
            await ws.send_str(json.dumps(
                {'type': 'auth', 
                 'access_token': ACCESS_TOKEN}
            ))
        
            await ws.send_str(json.dumps(
                {'id': 1, 'type': 'subscribe_events',
                 'event_type': 'state_changed'}
            ))
            
            while True:
                msg = await ws.receive()
                print(msg)
                if msg.type == aiohttp.WSMsgType.ERROR:
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break
                    
loop = asyncio.get_event_loop()  
loop.run_until_complete(main())
loop.close()  

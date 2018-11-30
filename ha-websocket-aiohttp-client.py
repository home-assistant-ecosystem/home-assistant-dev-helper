#!/usr/bin/python3
#
# Copyright (c) 2018, Max Rydahl Andersen <max@xam.dk>
# Released under the ASL 2.0 license. See LICENSE.md file for details.
#
import asyncio
import aiohttp
import json

async def echo():

    async with aiohttp.ClientSession().ws_connect('http://localhost:8123/api/websocket') as ws:
            
            await ws.send_str(json.dumps(
                {'type': 'auth', 
                  'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIzZTI0MWZiNGQzN2M0YjA5YTZiMzBmNzZiZDkzMDRjNiIsImlhdCI6MTU0MzU4NDM1OSwiZXhwIjoxODU4OTQ0MzU5fQ.fcB9Rb7sQ3Z1E1c9jRLM8DZHrmulPVVNtdJaxvW7wsg'}
                  ))
        
            await ws.send_str(json.dumps(
            {'id': 1, 'type': 'subscribe_events', 'event_type': 'state_changed'}))
            
            while True:
                msg = await ws.receive()
                print(msg)
                if msg.type == aiohttp.WSMsgType.ERROR:
                    break
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break
                    
loop = asyncio.get_event_loop()  
loop.run_until_complete(echo())  
loop.close()  

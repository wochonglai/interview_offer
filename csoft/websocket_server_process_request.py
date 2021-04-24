#!/usr/bin/env python

# WS server example
# https://websockets.readthedocs.io/en/stable/faq.html

import asyncio
import websockets

# async def process_request(self, path, request_headers):
#     access_token = request_headers["access-token"]

async def hello(websocket, path):
    print(websocket.request_headers)
    access_token = websocket.request_headers["access-token"]
    print(access_token)
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
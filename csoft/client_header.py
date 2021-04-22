#!/usr/bin/env python

# WS client example

import asyncio
import websockets


async def hello():
    uri = "ws://localhost:8765"
    extra_headers = {"access-token": "test_cookie"}
    async with websockets.connect(uri, extra_headers=extra_headers) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(hello())
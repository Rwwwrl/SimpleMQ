from typing import List
import asyncio

# annotations
from asyncio.base_events import Server
from asyncio.streams import StreamReader, StreamWriter
from asyncio.trsock import TransportSocket

from collections import deque
import json

FOLLOWERS: List[StreamWriter] = []


async def start_callback(reader: StreamReader, writer: StreamWriter):

    while True:

        try:
            request_message = (await reader.read(255)).decode('utf-8')
        except ConnectionResetError:
            break

        if not request_message:
            break

        try:
            deserialized_message = json.loads(request_message)
        except Exception:
            print('required json like message')
            continue

        if deserialized_message['type'] == 'follower':
            if not writer in FOLLOWERS:
                print('follower added')
                FOLLOWERS.append(writer)

        if deserialized_message['type'] == 'publisher':
            for follower in FOLLOWERS:
                try:
                    follower.write(deserialized_message['data'].encode('utf-8'))
                    await writer.drain()
                    print('publisher handled')
                except Exception:
                    continue

    writer.close()


async def run_server():

    server: Server = await asyncio.start_server(
        client_connected_cb=start_callback,
        host='localhost',
        port=9090,
        limit=4,
    )
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(run_server())

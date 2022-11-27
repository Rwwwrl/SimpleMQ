from typing import List
import asyncio
from asyncio.base_events import Server
from asyncio.streams import StreamReader, StreamWriter

from .message_deserializer import message_deserializer
from .message.message import PossibleSenderTypes
from .request_message_convert_to_server_message import request_message_convert_to_server_message
from .logger_conf import logger


FOLLOWERS: List[StreamWriter] = []


async def start_callback(reader: StreamReader, writer: StreamWriter):

    while True:

        try:
            request_message = (await reader.read(255))
        except ConnectionResetError:
            break

        if not request_message:
            break

        try:
            message = message_deserializer(message=request_message)
        except Exception:
            logger.exception(f'request_message should be deserialible, received: "{request_message}"')
            continue

        logger.debug(f'message received from {type(message)}')
        if message.sender_type == PossibleSenderTypes.FOLLOWER:
            if not writer in FOLLOWERS:
                logger.debug('new follower was added')
                FOLLOWERS.append(writer)

        if message.sender_type == PossibleSenderTypes.PUBLISHER:
            message_from_server = request_message_convert_to_server_message(message=message)
            for follower in FOLLOWERS:
                try:
                    follower.write(message_from_server.as_bytes)
                    await writer.drain()
                    logger.debug(f'message to {follower} were delived')
                except Exception:
                    logger.exception('some exception')
                    continue

    writer.close()


async def run_server():
    HOST = 'localhost'
    PORT = 9090

    server: Server = await asyncio.start_server(
        client_connected_cb=start_callback,
        host=HOST,
        port=PORT,
        limit=4,
    )
    async with server:
        logger.debug(f'server was started at {HOST}:{PORT}')
        await server.serve_forever()

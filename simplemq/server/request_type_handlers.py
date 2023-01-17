from __future__ import annotations

import abc
import asyncio
import re
from asyncio.streams import StreamWriter
from collections import deque
from typing import Callable, Iterator, List

from . import exceptions
from .data import PELS, STREAMS
from .stream_writer_wrapper import StreamWriterWrapper
from .. import hints
from ..bind import BindTypes
from ..logger_conf import LOGGER
from ..message_package import convert_message_to_json, create_server_message
from ..message_package import message_classes as message_module


def get_streams(message: message_module.MessageFromFollower) -> List[hints.Stream]:
    if message.bind.bind_type == BindTypes.DIRECT:
        stream_name = message.bind.route_string
        try:
            streams = [STREAMS[stream_name]]
        except KeyError:
            return []
        else:
            return streams
    if message.bind.bind_type == BindTypes.REGEX_BASED:
        return streams_iterator(routing_string=message.bind.route_string)


def streams_iterator(routing_string: hints.RouteString) -> Iterator[hints.Stream]:
    pattern = re.compile(routing_string)
    for stream_name in STREAMS.keys():
        if re.search(pattern=pattern, string=stream_name):
            yield STREAMS[stream_name]


def get_method_by_request_type(instance: IHandler, request_type: message_module.PossibleRequestType) -> Callable:
    attr = f'handle__{request_type.value.lower()}'
    return getattr(instance, attr)


class IHandler(abc.ABC):
    @abc.abstractmethod
    async def handle_message(self, message: message_module.IMessage, writer: StreamWriter) -> None:
        pass


class BaseHandler(IHandler):
    async def handle_message(self, message: message_module.IMessage, writer: StreamWriter) -> None:
        method = get_method_by_request_type(self, message.request_type)
        await method(message, writer)


class HandlerMessagesFromFollower(BaseHandler):
    async def handle__give_me_new_message(
        self,
        message: message_module.MessageFromFollower,
        writer: StreamWriter,
    ) -> None:
        follower = StreamWriterWrapper(member_name=message.sender_member_name, stream_writer=writer)
        message_to_follower_have_delivered = False
        while not message_to_follower_have_delivered:
            streams = get_streams(message=message)
            streams_are_empty = True
            for stream in streams:
                streams_are_empty = False
                try:
                    new_message = stream.popleft()
                except IndexError:
                    await asyncio.sleep(0)
                else:
                    try:
                        await self._send_message_to_follower(
                            follower=follower,
                            message_from_server=new_message,
                        )
                        message_to_follower_have_delivered = True
                        PELS.setdefault(message.sender_member_name, hints.PEL(deque([])))
                        PELS[message.sender_member_name].append(new_message)
                    except Exception as e:
                        # если нам не удалось доставить сообщение по какой-либо причине,
                        # то мы возвращаем его обратно в стрим
                        stream.appendleft(new_message)
                        LOGGER.error('Неизвестная ошибка')
                        raise e
                    else:
                        break
            if streams_are_empty:
                await asyncio.sleep(0)

    async def handle__ack_message(self, message: message_module.MessageFromFollower, writer: StreamWriter) -> None:
        follower_PEL = PELS[message.sender_member_name]
        message_id_to_delete = message.message_body
        for message in follower_PEL.copy():
            if message.id == message_id_to_delete:
                follower_PEL.remove(message)
        LOGGER.debug(f'Обработка сообщения с id: {message_id_to_delete} была подтвеждена')

    async def _send_message_to_follower(
        self,
        follower: StreamWriterWrapper,
        message_from_server: message_module.MessageFromServer,
    ) -> None:
        try:
            follower.stream_writer.write(message_from_server.as_bytes)
            await follower.stream_writer.drain()
            LOGGER.debug(f'сообщение к подписчику: "{follower.member_name}" было успешно доставлено')
        except ConnectionResetError:
            LOGGER.warning(f'сразу доставить сообщения подписчику {follower.member_name} не удалось')
            raise exceptions.ConnectionToFollowerHasLost

        except Exception as e:
            LOGGER.exception('Какая-то ошибка!')
            raise e


class HandlerMessagesFromPublisher(BaseHandler):
    async def handle__new_message(self, message: message_module.MessageFromPublisher, writer: StreamWriter) -> None:
        message_from_server = create_server_message(message_body=message.message_body)
        if message.bind.bind_type == BindTypes.DIRECT:
            stream_name = message.bind.route_string
            STREAMS[stream_name].append(message_from_server)
        if message.bind.bind_type == BindTypes.REGEX_BASED:
            streams = streams_iterator(routing_string=message.bind.route_string)
            for stream in streams:
                stream.append(message_from_server)
                await asyncio.sleep(0)


class HandlerMessagesFromCursor(BaseHandler):
    async def handle__create_stream(self, message: message_module.MessageFromCursor, writer: StreamWriter) -> None:
        stream_name = message.message_body
        try:
            STREAMS[stream_name]
        except KeyError:
            STREAMS[stream_name] = deque([])
            LOGGER.debug(f'был создан новый стрим с наименованием: {stream_name}')

    async def handle__get_pels(self, message: message_module.MessageFromCursor, writer: StreamWriter) -> None:
        json_serializable_pels = {}
        for member_name, pel in PELS:
            json_serializable_pels[member_name] = [convert_message_to_json(m) for m in pel]

        message_from_server = create_server_message(message_body=json_serializable_pels)
        writer.write(message_from_server.as_bytes)
        await writer.drain()

    async def handle__get_streams(self, message: message_module.MessageFromCursor, writer: StreamWriter) -> None:
        json_serializable_streams = {}
        for stream_name, stream in STREAMS.items():
            json_serializable_streams[stream_name] = [convert_message_to_json(m) for m in stream]

        message_from_server = create_server_message(message_body=json_serializable_streams)
        writer.write(message_from_server.as_bytes)
        await writer.drain()

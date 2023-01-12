import json
from dataclasses import asdict
from enum import Enum
from uuid import UUID

from .message_classes import IMessage

END_OF_MESSAGE = '\n'


def convert_message_to_bytes(message: IMessage) -> bytes:

    as_dict = asdict(message)
    for key, key_value in as_dict.items():
        if isinstance(key_value, Enum):
            as_dict[key] = key_value.value
        if isinstance(key_value, UUID):
            as_dict[key] = str(key_value)

    as_json_string = json.dumps(as_dict) + END_OF_MESSAGE
    return as_json_string.encode('utf-8')

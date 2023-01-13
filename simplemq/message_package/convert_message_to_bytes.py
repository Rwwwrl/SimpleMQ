import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from uuid import UUID

from .message_classes import IMessage

END_OF_MESSAGE = '\n'


def get_json_serializable_object_from_dataclass(dataclass):
    as_dict = asdict(dataclass)

    def normalize_dict(d: dict) -> dict:
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result[key] = normalize_dict(value)
                continue
            if isinstance(value, Enum):
                result[key] = value.value
                continue
            if isinstance(value, UUID):
                result[key] = str(value)
                continue
            result[key] = value
        return result

    as_dict = normalize_dict(d=as_dict)
    return as_dict


def convert_message_to_json(message: IMessage) -> dict:
    return get_json_serializable_object_from_dataclass(dataclass=message)


def convert_message_to_bytes(message: IMessage) -> bytes:
    assert is_dataclass(message)

    json_serializable_object = convert_message_to_json(message)

    as_json_string = json.dumps(json_serializable_object) + END_OF_MESSAGE
    return as_json_string.encode('utf-8')

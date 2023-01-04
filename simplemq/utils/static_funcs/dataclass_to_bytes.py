import json
from dataclasses import asdict
from enum import Enum
from uuid import UUID


def dataclass_to_bytes(dataclass_object) -> bytes:
    as_dict = asdict(dataclass_object)
    for key, key_value in as_dict.items():
        if isinstance(key_value, Enum):
            as_dict[key] = key_value.value
        if isinstance(key_value, UUID):
            as_dict[key] = str(key_value)

    as_json_string = json.dumps(as_dict)
    return as_json_string.encode('utf-8')

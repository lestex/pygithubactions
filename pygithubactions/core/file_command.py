import os
from typing import Any
import uuid

from pygithubactions.core.utils import to_command_value


def issue_file_command(command: str, message: Any) -> None:
    env_path = os.environ.get(f'GITHUB_{command}', None)
    if not env_path:
        raise Exception(
            f'Unable to find environment variable for file command: {command}'
        )

    if not os.path.isfile(env_path):
        raise Exception(f'Missing file at path: {env_path}')

    with open(env_path, 'a', encoding='utf8') as f:
        message = to_command_value(message)
        to_write = f'{message}{os.linesep}'
        f.write(to_write)


def prepare_key_value_message(key: str, value: Any) -> str:
    delimiter = f'ghadelimiter_{uuid.uuid4()}'
    converted_value = to_command_value(value)

    # These should realistically never happen, but just in case
    # someone finds a way to exploit uuid generation let's not
    # allow keys or values that contain the delimiter.
    if delimiter in key:
        raise Exception(
            f'Unexpected input: name should not contain '
            f'the delimiter: {delimiter}'
        )

    if delimiter in converted_value:
        raise Exception(
            f'Unexpected input: value should not contain '
            f'the delimiter: {delimiter}'
        )

    return f'{key}<<{delimiter}{os.linesep}{converted_value}{os.linesep}{delimiter}'

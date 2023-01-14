import os
from typing import Any

from pygithubactions.core.utils import to_command_value

CMD_STRING = '::'


class Command:
    """Produces command as output

    Command format:
        ::name key=value,key=value::message

    Examples:
        ::warning::This is the message
        ::set-env name=MY_VAR::some value
    """

    def __init__(
        self,
        command: str | None,
        properties: dict[str, Any] | None,
        message: str | None,
    ) -> None:
        self.command = command or 'missing.command'
        self.properties = properties
        self.message = message

    def __str__(self) -> str:
        cmd_str = f'{CMD_STRING}{self.command}'
        if self.properties:
            cmd_str += ' '
            for key, value in self.properties.items():
                value = escape_property(value)
                cmd_str += f'{key}={value},'
            # remove last comma
            cmd_str = cmd_str[:-1]

        message = escape_data(self.message)
        cmd_str += f'{CMD_STRING}{message}'
        return cmd_str


def issue_command(command: str, props: dict[str, Any], message: str) -> None:
    cmd = Command(command, props, message)
    print(cmd, end=os.linesep)


def issue(name: str, message: str = '') -> None:
    issue_command(name, {}, message)


def escape_data(d: Any) -> str:
    s = to_command_value(d)
    s = s.replace('%', '%25')
    s = s.replace('\r', '%0D')
    s = s.replace('\n', '%0A')
    return s


def escape_property(d: Any) -> str:
    s = to_command_value(d)
    s = s.replace('%', '%25')
    s = s.replace('\r', '%0D')
    s = s.replace('\n', '%0A')
    s = s.replace(':', '%3A')
    s = s.replace(',', '%2C')
    return s

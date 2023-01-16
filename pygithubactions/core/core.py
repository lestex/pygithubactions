import os
from typing import Any, Callable, List, Optional

from pygithubactions.core.command import issue
from pygithubactions.core.command import issue_command
from pygithubactions.core.file_command import issue_file_command
from pygithubactions.core.file_command import prepare_key_value_message
from pygithubactions.core.utils import AnnotationProperties
from pygithubactions.core.utils import to_command_properties
from pygithubactions.core.utils import to_command_value

# define exit codes
SUCCESS = 0
FAILURE = 1


def export_variable(name: str, value: Any) -> None:
    """Sets env variable for this action and future actions in the job.

    Args:
        name (str): Name of the variable.
        value (Any): Value of the variable.

        Non-string values will be converted to string with json.dumps().

    Returns:
         None:
    """
    converted = to_command_value(value)
    os.environ[name] = converted

    if 'GITHUB_ENV' in os.environ:
        issue_file_command('ENV', prepare_key_value_message(name, converted))
        return

    issue_command('set-env', {'name': name}, converted)


def set_secret(secret: str) -> None:
    """Registers a secret which will get masked from logs"""
    issue_command('add-mask', {}, secret)


def add_path(path: str) -> None:
    env_path = os.environ.get('GITHUB_PATH', None)
    if env_path:
        issue_file_command('PATH', path)
    else:
        issue_command('add-path', {}, path)

    old_path = os.environ['PATH']
    os.environ['PATH'] = f'{path}{os.pathsep}{old_path}'


def get_input(
    name: str, required: bool = False, trim_whitespace: bool = True
) -> str:
    """Gets the value of an input.

    Args:
        name (str): Name of the input to get.
        required (bool, optional): Whether the input is required (defaults to False).
        trim_whitespace (bool, optional): Whether leading/trailing whitespace will
        be trimmed for the input. Defaults to true.

    Returns:
        value (str): - Input value.
    """
    norm_name = name.replace(' ', '_').upper()
    value = os.environ.get(f'INPUT_{norm_name}', '')

    if required and not value:
        raise Exception(f'Input required and not supplied: {name}')

    if trim_whitespace:
        return value.strip()

    return value


def get_boolean_input(
    name: str, required: bool = False, trim_whitespace: bool = True
) -> bool:
    """Gets the input value of the boolean type in the
    YAML 1.2 "core schema" specification.

    Args:
        name (str): Name of the input to get.
        required (bool, optional): Whether the input is required (defaults to False).
        trim_whitespace (bool, optional): Whether leading/trailing whitespace will
        be trimmed for the input. Defaults to true.

    Returns:
        bool
    """
    true_values = ['true', 'True', 'TRUE']
    false_values = ['false', 'False', 'FALSE']
    value = get_input(name, required, trim_whitespace)

    if value in true_values:
        return True

    elif value in false_values:
        return False

    else:
        raise ValueError(
            f'Input does not meet YAML 1.2 "Core Schema" specification: {name}'
            f'Supported values: true | True | TRUE | false | False | FALSE'
        )


def get_multiline_input(
    name: str, required: bool = False, trim_whitespace: bool = True
) -> List[str]:
    """Gets the values of an multiline input.  Each value is also trimmed.

    Args:
        name (str): Name of the input to get.
        required (bool, optional): Whether the input is required (defaults to False).
        trim_whitespace (bool, optional): Whether leading/trailing whitespace will
        be trimmed for the input. Defaults to true.

    Returns:
        list[str]: List of inputs.
    """
    inputs = get_input(name, required, trim_whitespace)
    inputs_list = [i for i in inputs.split('\n') if i != '']

    if not trim_whitespace:
        return inputs_list

    return [i.strip() for i in inputs_list]


def set_output(name: str, value: Any) -> None:
    """Sets the value of an output.

    Args:
        name (str): Name of the output to set
        value (Any): Value to store.

        Non-string values will be converted to a string via json.dumps()

    Returns:
        None.
    """
    env_path = os.environ.get('GITHUB_OUTPUT', None)
    if env_path:
        issue_file_command('OUTPUT', prepare_key_value_message(name, value))
        return

    print()
    issue_command('set-output', {'name': name}, to_command_value(value))


def set_command_echo(enabled: bool) -> None:
    """Enables or disables the echoing of commands into stdout
    for the rest of the step.
    Echoing is disabled by default if ACTIONS_STEP_DEBUG is not set.
    """
    msg = 'on' if enabled else 'off'
    issue('echo', msg)


def set_failed(message: str) -> None:
    """Sets the action status to failed.

    Args:
        message (str): Add error issue message
    """
    error(message)
    exit(FAILURE)


# -----------------------------------------------------------------------
# Logging Commands
# -----------------------------------------------------------------------


def is_debug() -> bool:
    """Gets whether Actions Step Debug is on or not

    Returns:
        bool: is Debug
    """
    is_debug = os.environ.get('RUNNER_DEBUG')
    return True if is_debug else False


def debug(message: str) -> None:
    """Writes debug message to user log

    Args:
        message (str): debug message
    """
    issue_command('debug', {}, message)


def error(
    message: str, properties: Optional[AnnotationProperties] = None
) -> None:
    """Adds an error issue.

    Args:
        message (str): issue message.
        properties (AnnotationProperties, optional): optional properties
        to add to the annotation.
    """
    issue_command(
        'error',
        to_command_properties(properties),
        message,
    )


def warning(
    message: str, properties: Optional[AnnotationProperties] = None
) -> None:
    """Adds a warning issue.

    Args:
        message (str): issue message.
        properties (AnnotationProperties, optional): properties to add
        to the annotation. Defaults to None.
    """
    issue_command(
        'warning',
        to_command_properties(properties),
        message,
    )


def notice(
    message: str, properties: Optional[AnnotationProperties] = None
) -> None:
    """Adds a notice issue

    Args:
        message (str): issue message.
        properties (AnnotationProperties, optional): optional properties
        to add to the annotation.. Defaults to None.
    """
    issue_command(
        'notice',
        to_command_properties(properties),
        message,
    )


def info(message: str) -> None:
    """Writes info to stdout

    Args:
        message (str): info message.
    """
    print(message, end=os.linesep)


def start_group(name: str) -> None:
    """Begin an output group.
    Output until the next `groupEnd` will be foldable in this group.

    Args:
        message (str): The name of the output group.
    """
    issue('group', name)


def end_group() -> None:
    """End an output group."""
    issue('endgroup')


def group(name: str, func: Callable) -> Any:
    """Wrap an asynchronous function call in a group.
    Returns the same type as the function itself.

    Args:
        name (str): The name of the group.
        func (Callable): The function to wrap in the group.
    """
    start_group(name)

    try:
        result = func()
    finally:
        end_group()

    return result


# -----------------------------------------------------------------------
# Wrapper action state
# -----------------------------------------------------------------------


def save_state(name: str, value: Any) -> None:
    """Saves state for current action, the state
    can only be retrieved by this action's post job execution.

    Args:
        name (str): name of the state to store
        value (Any): value to store.
        Non-string values will be converted to a string via json.dumps()

    Returns:
        None:
    """
    env_path = os.environ.get('GITHUB_STATE', None)
    if env_path:
        issue_file_command('STATE', prepare_key_value_message(name, value))
        return

    issue_command('save-state', {'name': name}, to_command_value(value))


def get_state(name: str) -> str:
    """Gets the value of an state set by this action's main execution.

    Args:
        name (str): name of the state to get

    Returns:
        (str):
    """
    return os.environ.get(f'STATE_{name}', '')

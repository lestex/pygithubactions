### pygithubactions/core
> Core functions for setting results, logging, registering secrets and exporting variables across actions

### Usage

### Import the package

```python
from pygithubactions import core
```

### Inputs/Outputs

Action inputs can be read with `get_input` which returns a `str` or `get_boolean_input` which parses a boolean based on the [yaml 1.2 specification](https://yaml.org/spec/1.2/spec.html#id2804923). If `required` set to be false, the input should have a default value in `action.yml`.

Outputs can be set with `set_output` which makes them available to be mapped into inputs of other actions to ensure they are decoupled.

```python
from pygithubactions import core

my_input = core.get_input('inputName', required=True)
boolean_input = core.get_boolean_input('booleanInputName', required=True)
multiline_input = core.get_multiline_input('multilineInputName', required=True)

core.set_output('outputkey', 'outputval')
```

### Exporting variables

Since each step runs in a separate process, you can use `export_variable` to add it to this step and future steps environment blocks.

```python
from pygithubactions import core

core.export_variable('envvar', 'val')
```

### Setting a secret

Setting a secret registers the secret with the runner to ensure it is masked in logs.

```python
from pygithubactions import core

core.set_secret('mypassword')
```

### PATH Manipulation

To make a tool's path available in the path for the remainder of the job (without altering the machine or containers state), use `add_path`.  The runner will prepend the path given to the jobs PATH.

```python
from pygithubactions import core

core.add_path('/path/to/mytool')
```

### Exit codes

You should use this library to set the failing exit code for your action.  If status is not set and the script runs to completion, that will lead to a success.

```python
from pygithubactions import core

try:
    # Do stuff
    # ...

except Exception as e:
    # set_failed logs the message and sets a failing exit code
    core.set_failed(f'Action failed with error {e}')
```

### Logging

Finally, this library provides some utilities for logging. Note that debug logging is hidden from the logs by default. This behavior can be toggled by enabling the [Step Debug Logs](../../docs/action-debugging.md#step-debug-logs).

```python
from pygithubactions import core


my_input = core.get_input('input')

try:
    core.debug('Inside try block')

    if not my_input:
        core.warning('my_input was not set')

    if core.is_debug():
        # do something
    else:
        # do something

    # Do stuff
    core.info('Output to the actions build log')
    core.notice('This is a message that will also emit an annotation')

except Exception as e:
    core.error(f'Error: {e}, action may still succeed though')
```

This library can also wrap chunks of output in foldable groups.

```python
from pygithubactions import core

# Manually wrap output
core.start_group('Do some function')
do_some_job()
core.end_group()

# Wrap a function call
def do_some_job():
    ...
    return result

result = core.group('Do something async', do_some_job)
```

#### Annotations

This library has 3 methods that will produce [annotations](https://docs.github.com/en/rest/reference/checks#create-a-check-run).
```python
from pygithubactions import core

core.error('This is a bad error, action may still succeed though.')
core.warning('Something went wrong, but it\'s not bad enough to fail the build.')
core.notice('Something happened that you might want to know about.')
```

These will surface to the UI in the Actions page and on Pull Requests. They look something like this:

![Annotations Image](/docs/annotations.png)

These annotations can also be attached to particular lines and columns of your source files to show exactly where a problem is occuring.

These options are:
```python
@dataclass
class AnnotationProperties:
    # A title for the annotation.
    title: str = ''

    # The path of the file for which the annotation should be created.
    file: str = ''

    # The start line for the annotation.
    startLine: int = 0

    # The end line for the annotation. Defaults to `startLine`
    # when `startLine` is provided.
    endLine: int = 0

    # The start column for the annotation. Cannot be sent when
    # `startLine` and `endLine` are different values.
    startColumn: int = 0

    # The end column for the annotation. Cannot be sent when
    # `startLine` and `endLine` are different values.
    # Defaults to `startColumn` when `startColumn` is provided.
    endColumn: int = 0
```

#### Styling output

Colored output is supported in the Action logs via standard [ANSI escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code). 3/4 bit, 8 bit and 24 bit colors are all supported.

Foreground colors:
```python
# 3/4 bit
core.info('\u001b[35mThis foreground will be magenta')

# 8 bit
core.info('\u001b[38;5;6mThis foreground will be cyan')

# 24 bit
core.info('\u001b[38;2;255;0;0mThis foreground will be bright red')
```

Background colors:
```python
# 3/4 bit
core.info('\u001b[43mThis background will be yellow')

# 8 bit
core.info('\u001b[48;5;6mThis background will be cyan')

# 24 bit
core.info('\u001b[48;2;255;0;0mThis background will be bright red')
```

Special styles:
```python
core.info('\u001b[1mBold text')
core.info('\u001b[3mItalic text')
core.info('\u001b[4mUnderlined text')
```

ANSI escape codes can be combined with one another:
```python
core.info('\u001b[31;46mRed foreground with a cyan background and \u001b[1mbold text at the end')
```

> Note: Escape codes reset at the start of each line

```python
core.info('\u001b[35mThis foreground will be magenta')
core.info('This foreground will reset to the default')
```

#### Action state

You can use this library to save state and get state for sharing information between a given wrapper action:
In action's `main.py`:

```python
core.save_state("pidToKill", 12345)

pid = core.get_state("pidToKill")
```

#### Filesystem path helpers

You can use these methods to manipulate file paths across operating systems.

The `to_posix_path` function converts input paths to Posix-style (Linux) paths.
The `to_win32_path` function converts input paths to Windows-style paths. These
functions work independently of the underlying runner operating system.

```python
from pygithubactions import path

path.to_posix_path('\\foo\\bar') // => /foo/bar
path.to_win32_path('/foo/bar') // => \foo\bar
```

The `to_platform_path` function converts input paths to the expected value on the runner's operating system.

```python
// On a Windows runner.
path.to_platform_path('/foo/bar') // => \foo\bar

// On a Linux runner.
path.to_platform_path('\\foo\\bar') // => /foo/bar
```

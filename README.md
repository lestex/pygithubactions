# pygithubactions
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

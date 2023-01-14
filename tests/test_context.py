from pygithubactions.context.context import Context
from pygithubactions.context.context import get_context


def test_context_object(tmp_path, create_event_file_func):
    event_to_test = {
        'type': 'pull_request',
    }
    create_event_file_func('EVENT_PATH', event_to_test, tmp_path)
    ctx = get_context()

    assert type(ctx) is Context
    assert ctx.payload['type'] == 'pull_request'
    assert ctx.event_name == 'push'

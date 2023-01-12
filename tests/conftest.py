import os

import pytest

TEST_INPUT_ENV_VARS = {
    'INPUT_MY_INPUT': 'val',
    'INPUT_MISSING': '',
    'INPUT_SPECIAL_CHARS_\'\t"\\': '\'\t"\\ response ',
    'INPUT_MULTIPLE_SPACES_VARIABLE': 'I have multiple spaces',
    'INPUT_BOOLEAN_INPUT': 'true',
    'INPUT_BOOLEAN_INPUT_TRUE1': 'true',
    'INPUT_BOOLEAN_INPUT_TRUE2': 'True',
    'INPUT_BOOLEAN_INPUT_TRUE3': 'TRUE',
    'INPUT_BOOLEAN_INPUT_FALSE1': 'false',
    'INPUT_BOOLEAN_INPUT_FALSE2': 'False',
    'INPUT_BOOLEAN_INPUT_FALSE3': 'FALSE',
    'INPUT_WRONG_BOOLEAN_INPUT': 'wrong',
    'INPUT_WITH_TRAILING_WHITESPACE': '  some val  ',
    'INPUT_MY_INPUT_LIST': 'val1\nval2\nval3',
    'INPUT_LIST_WITH_TRAILING_WHITESPACE': '  val1  \n  val2  \n  ',
}


# The combination of scope="session" and autouse=True means
# this code runs only once for the whole test suit.
@pytest.fixture(scope='session', autouse=True)
def get_input_env():
    # Will be executed before the first test
    old_environ = dict(os.environ)
    os.environ.update(TEST_INPUT_ENV_VARS)

    yield

    # Will be executed after the last test
    os.environ.clear()
    os.environ.update(old_environ)


@pytest.fixture(scope='session', autouse=True)
def create_file_func():
    def create_file(command: str, tmp: str) -> str:
        path = os.path.join(tmp, f'{command}')
        os.environ[f'GITHUB_{command}'] = path

        with open(path, 'a', encoding='utf8') as f:
            f.write('')

        return path

    return create_file


@pytest.fixture(scope='session', autouse=True)
def read_file_func():
    def read_file(command: str, tmp: str) -> str:
        path = os.path.join(tmp, f'{command}')

        with open(path, 'r', encoding='utf8') as f:
            data = f.read()

        del os.environ[f'GITHUB_{command}']

        return data

    return read_file

import os

from pygithubactions.core.path_utils import to_platform_path
from pygithubactions.core.path_utils import to_posix_path
from pygithubactions.core.path_utils import to_win32_path
import pytest

TO_POSIX_PATH_TEST = [
    ('', ''),
    ('foo', 'foo'),
    ('foo/bar/baz', 'foo/bar/baz'),
    ('/foo/bar/baz', '/foo/bar/baz'),
    ('foo\\bar\\baz', 'foo/bar/baz'),
    ('\\foo\\bar\\baz', '/foo/bar/baz'),
    ('\\foo/bar/baz', '/foo/bar/baz'),
]


@pytest.mark.parametrize('test_input,expected', TO_POSIX_PATH_TEST)
def test_to_posix_path(test_input, expected):
    assert to_posix_path(test_input) == expected


TO_WIN32_PATH_TEST = [
    ('', ''),
    ('foo', 'foo'),
    ('foo/bar/baz', 'foo\\bar\\baz'),
    ('/foo/bar/baz', '\\foo\\bar\\baz'),
    ('foo\\bar\\baz', 'foo\\bar\\baz'),
    ('\\foo\\bar\\baz', '\\foo\\bar\\baz'),
    ('\\foo/bar\\baz', '\\foo\\bar\\baz'),
]


@pytest.mark.parametrize('test_input,expected', TO_WIN32_PATH_TEST)
def test_to_win32_path(test_input, expected):
    assert to_win32_path(test_input) == expected


TO_PLATFORM_PATH_TEST = [
    ('', ''),
    ('foo', 'foo'),
    ('foo/bar/baz', os.path.join('foo', 'bar', 'baz')),
    ('/foo/bar/baz', os.path.join(os.sep, 'foo', 'bar', 'baz')),
    ('foo\\bar\\baz', os.path.join('foo', 'bar', 'baz')),
    ('\\foo\\bar\\baz', os.path.join(os.sep, 'foo', 'bar', 'baz')),
    ('\\foo/bar\\baz', os.path.join(os.sep, 'foo', 'bar', 'baz')),
]


@pytest.mark.parametrize('test_input,expected', TO_PLATFORM_PATH_TEST)
def test_to_platform_path(test_input, expected):
    assert to_platform_path(test_input) == expected

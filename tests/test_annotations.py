from pygithubactions.core.utils import AnnotationProperties
from pygithubactions.core.utils import to_command_properties
import pytest

# AnnotationProperties(
#   title: str = '',
#   file: str = '',
#   startLine: int = 0,
#   endLine: int = 0,
#   startColumn: int = 0,
#   endColumn: int = 0
# )
TEST_ANNOTATION_PROPERTIES = [
    (
        AnnotationProperties(),
        {
            'col': 0,
            'endColumn': 0,
            'endLine': 0,
            'file': '',
            'line': 0,
            'title': '',
        },
    ),
    (
        AnnotationProperties(
            title='test',
            file='run.txt',
            startLine=1,
            endLine=2,
            startColumn=10,
            endColumn=20,
        ),
        {
            'col': 10,
            'endColumn': 20,
            'endLine': 2,
            'file': 'run.txt',
            'line': 1,
            'title': 'test',
        },
    ),
]


@pytest.mark.parametrize('test_input,expected', TEST_ANNOTATION_PROPERTIES)
def test_annotation_properties(test_input, expected):
    got = to_command_properties(test_input)

    assert got == expected

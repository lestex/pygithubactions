from pygithubactions.core.core import get_boolean_input
from pygithubactions.core.core import get_input
from pygithubactions.core.core import get_multiline_input
import pytest


class TestGetInput:
    def test_get_input_non_required_input(self):
        assert get_input('my input') == 'val'

    def test_get_input_gets_required_input(self):
        assert get_input('my input', required=True) == 'val'

    def test_get_input_raises_exception_missing_required_input(self):
        with pytest.raises(Exception):
            get_input('missing', required=True)

    def test_get_input_case_insensitive(self):
        assert get_input('My InPuT') == 'val'

    def test_get_input_does_not_raise_missing_non_required_input(self):
        assert get_input('missing', required=False) == ''

    def test_get_input_handles_special_characters(self):
        assert get_input('special chars_\'\t"\\') == '\'\t"\\ response'

    def test_get_input_handles_multiple_spaces(self):
        want = 'I have multiple spaces'
        got = get_input('multiple spaces variable')
        assert got == want

    def test_get_input_trims_whitespace_by_default(self):
        assert get_input('with trailing whitespace') == 'some val'

    def test_get_input_trims_whitespace_when_explicitly_set(self):
        want = 'some val'
        got = get_input('with trailing whitespace', trim_whitespace=True)
        assert got == want

    def test_get_input_does_not_trim_whitespace_when_option_false(self):
        want = '  some val  '
        got = get_input('with trailing whitespace', trim_whitespace=False)
        assert got == want


class TestGetBooleanInput:
    def test_get_boolean_input_gets_non_required_input(self):
        assert get_boolean_input('boolean input') is True

    def test_get_boolean_input_gets_required_input(self):
        assert get_boolean_input('boolean input', required=True) is True

    def test_get_boolean_input_handles_input(self):
        assert get_boolean_input('boolean input true1') is True
        assert get_boolean_input('boolean input true2') is True
        assert get_boolean_input('boolean input true3') is True

        assert get_boolean_input('boolean input false1') is False
        assert get_boolean_input('boolean input false2') is False
        assert get_boolean_input('boolean input false3') is False

    def test_get_boolean_input_handles_wrong_boolean_input(self):
        with pytest.raises(Exception):
            get_boolean_input('wrong boolean input')


class TestGetMultilineInput:
    def test_get_multiline_input_works(self):
        want = ['val1', 'val2', 'val3']
        assert get_multiline_input('my input list') == want

    def test_get_multiline_input_trims_whitespace_default(self):
        want = ['val1', 'val2']
        assert get_multiline_input('list with trailing whitespace') == want

    def test_get_multiline_input_trims_whitespace_when_option_true(self):
        want = ['val1', 'val2']
        got = get_multiline_input(
            'list with trailing whitespace', trim_whitespace=True
        )
        assert got == want

    def test_get_multiline_input_not_trim_whitespace_when_option_false(self):
        want = ['  val1  ', '  val2  ', '  ']
        got = get_multiline_input(
            'list with trailing whitespace', trim_whitespace=False
        )
        assert got == want

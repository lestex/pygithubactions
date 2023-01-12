import os
from unittest import mock

from pygithubactions.core.core import set_output
from pygithubactions.core.file_command import issue_file_command
import pytest

from . import requires_env

UUID = 'edb6883f-b400-440d-8d27-15b881d69e09'


class TestSetOutput:
    command = 'OUTPUT'

    @requires_env('local')
    def test_legacy_set_output_produces_correct_command(self, capsys):
        set_output('some output', 'some value')
        captured = capsys.readouterr()

        want = f'{os.linesep}::set-output name=some output::some value{os.linesep}'   # noqa
        assert captured.out == want

    @requires_env('local')
    def test_legacy_set_output_handles_bools(self, capsys):
        set_output('some output', False)
        captured = capsys.readouterr()

        want = f'{os.linesep}::set-output name=some output::false{os.linesep}'
        assert captured.out == want

    @requires_env('local')
    def test_legacy_set_output_handles_numbers(self, capsys):
        set_output('some output', 1.01)
        captured = capsys.readouterr()

        want = f'{os.linesep}::set-output name=some output::1.01{os.linesep}'
        assert captured.out == want

    def test_set_output_produces_correct_command_and_sets_output(
        self, tmp_path, create_file_func, read_file_func
    ):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            set_output('my out', 'out val')

        got = read_file_func(self.command, tmp_path)
        want = f'my out<<{DELIMITER}{os.linesep}out val{os.linesep}{DELIMITER}{os.linesep}'   # noqa
        assert got == want

    def test_set_output_handles_boolean_inputs(
        self, tmp_path, create_file_func, read_file_func
    ):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            set_output('my out', True)

        got = read_file_func(self.command, tmp_path)
        want = f'my out<<{DELIMITER}{os.linesep}true{os.linesep}{DELIMITER}{os.linesep}'   # noqa
        assert got == want

    def test_set_output_handles_number_inputs(
        self, tmp_path, create_file_func, read_file_func
    ):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            set_output('my out', 5)

        got = read_file_func(self.command, tmp_path)
        want = f'my out<<{DELIMITER}{os.linesep}5{os.linesep}{DELIMITER}{os.linesep}'   # noqa
        assert got == want

    def test_set_output_does_not_allow_delimiter_value(
        self, tmp_path, create_file_func
    ):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            with pytest.raises(Exception):
                set_output('my out', f'good stuff {DELIMITER} bad stuff')

    def test_set_output_does_not_allow_delimiter_name(
        self, tmp_path, create_file_func
    ):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            with pytest.raises(Exception):
                set_output(f'good stuff {DELIMITER} bad stuff', 'test')

    def test_issue_file_command_raises(self):
        command = 'unknown'
        with pytest.raises(Exception):
            issue_file_command(command, 'test')

    def test_issue_file_command_raises_missing_file(
        self, tmp_path, create_file_func
    ):
        path = create_file_func(self.command, tmp_path)
        os.remove(path)

        with pytest.raises(Exception):
            issue_file_command(self.command, 'test')

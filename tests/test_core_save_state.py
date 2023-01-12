import os
from unittest import mock

from pygithubactions.core.core import save_state
from pygithubactions.core.file_command import issue_file_command
import pytest

from . import requires_env

UUID = 'edb6883f-b400-440d-8d27-15b881d69e09'


class TestSaveState:
    command = 'STATE'

    @requires_env('local')
    def test_legacy_save_state_produces_correct_command(self, capsys):
        save_state('state_1', 'some value')
        got = capsys.readouterr().out
        assert got == f'::save-state name=state_1::some value{os.linesep}'

    @requires_env('local')
    def test_legacy_save_state_handles_numbers(self, capsys):
        save_state('state_1', 1)
        got = capsys.readouterr().out
        assert got == f'::save-state name=state_1::1{os.linesep}'

    @requires_env('local')
    def test_legacy_save_state_handles_bools(self, capsys):
        save_state('state_1', True)
        got = capsys.readouterr().out
        assert got == f'::save-state name=state_1::true{os.linesep}'

    def test_save_state_produces_correct_command_saves_state(
        self, tmp_path, create_file_func, read_file_func
    ):
        create_file_func(self.command, tmp_path)
        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            save_state('my state', 'out val')

        got = read_file_func(self.command, tmp_path)
        want = f'my state<<{DELIMITER}{os.linesep}out val{os.linesep}{DELIMITER}{os.linesep}'   # noqa
        assert got == want

    def test_save_state_handles_boolean_inputs(
        self, tmp_path, create_file_func, read_file_func
    ):
        create_file_func(self.command, tmp_path)
        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            save_state('my state', True)

        got = read_file_func(self.command, tmp_path)
        want = f'my state<<{DELIMITER}{os.linesep}true{os.linesep}{DELIMITER}{os.linesep}'   # noqa
        assert got == want

    def test_save_state_handles_numbers_inputs(
        self, tmp_path, create_file_func, read_file_func
    ):
        create_file_func(self.command, tmp_path)
        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            save_state('my state', 65)

        got = read_file_func(self.command, tmp_path)
        want = f'my state<<{DELIMITER}{os.linesep}65{os.linesep}{DELIMITER}{os.linesep}'   # noqa
        assert got == want

    def test_set_output_does_not_allow_delimiter_value(
        self, tmp_path, create_file_func
    ):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            with pytest.raises(Exception):
                save_state('my state', f'good stuff {DELIMITER} bad stuff')

    def test_set_output_does_not_allow_delimiter_name(
        self, tmp_path, create_file_func
    ):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            with pytest.raises(Exception):
                save_state(f'good stuff {DELIMITER} bad stuff', 'test')

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

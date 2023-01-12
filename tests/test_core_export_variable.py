import os
from unittest import mock

from pygithubactions.core.core import export_variable
import pytest

from . import requires_env

UUID = 'edb6883f-b400-440d-8d27-15b881d69e09'


class TestExportVariable:
    command = 'ENV'

    @requires_env('local')
    def test_legacy_export_variable(self, capsys):
        export_variable('my var', 'var val')
        got = capsys.readouterr().out
        want = f'::set-env name=my var::var val{os.linesep}'
        assert got == want

    @requires_env('local')
    def test_legacy_export_variable_escapes_variable_names(self, capsys):
        export_variable('special char var \r\n,:', 'special val')
        got = capsys.readouterr().out
        want = f'::set-env name=special char var %0D%0A%2C%3A::special val{os.linesep}'
        assert got == want

    @requires_env('local')
    def test_legacy_export_variable_handles_boolean_inputs(self, capsys):
        export_variable('my var', True)
        got = capsys.readouterr().out
        want = f'::set-env name=my var::true{os.linesep}'
        assert got == want

    @requires_env('local')
    def test_legacy_export_variable_handles_number_inputs(self, capsys):
        export_variable('my var', 5)
        got = capsys.readouterr().out
        want = f'::set-env name=my var::5{os.linesep}'
        assert got == want

    def test_export_variable(self, tmp_path, create_file_func, read_file_func):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            export_variable('my var', 'var val')

        got = read_file_func(self.command, tmp_path)
        want = f'my var<<{DELIMITER}{os.linesep}var val{os.linesep}{DELIMITER}{os.linesep}'
        assert got == want

    def test_export_variable_handles_boolean_inputs(
        self, tmp_path, create_file_func, read_file_func
    ):
        create_file_func(self.command, tmp_path)
        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            export_variable('my var', True)

        got = read_file_func(self.command, tmp_path)
        want = f'my var<<{DELIMITER}{os.linesep}true{os.linesep}{DELIMITER}{os.linesep}'
        assert got == want

    def test_export_variable_handles_number_inputs(
        self, tmp_path, create_file_func, read_file_func
    ):
        create_file_func(self.command, tmp_path)
        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            export_variable('my var', 5)

        got = read_file_func(self.command, tmp_path)
        want = f'my var<<{DELIMITER}{os.linesep}5{os.linesep}{DELIMITER}{os.linesep}'
        assert got == want

    def test_export_variable_does_not_allow_delimiter_value(
        self, tmp_path, create_file_func
    ):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            with pytest.raises(Exception):
                export_variable('my out', f'good stuff {DELIMITER} bad stuff')

    def test_export_variable_does_not_allow_delimiter_name(
        self, tmp_path, create_file_func
    ):
        create_file_func(self.command, tmp_path)

        with mock.patch('uuid.uuid4') as uuid4:
            uuid4.return_value = UUID
            DELIMITER = f'ghadelimiter_{UUID}'
            with pytest.raises(Exception):
                export_variable(f'good stuff {DELIMITER} bad stuff', 'test')

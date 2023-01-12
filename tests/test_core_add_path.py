import os

from pygithubactions.core.core import add_path

from . import requires_env

UUID = 'edb6883f-b400-440d-8d27-15b881d69e09'


class TestAddPath:
    command = 'PATH'
    path = 'myPath'

    @requires_env('local')
    def test_add_path(self, capsys):
        old_path = os.environ['PATH']
        add_path(self.path)

        got = capsys.readouterr().out
        want = f'::add-path::{self.path}{os.linesep}'
        assert os.environ['PATH'] == f'{self.path}{os.pathsep}{old_path}'
        assert got == want

    def test_add_path_produces_correct_commands_sets_env(
        self, tmp_path, create_file_func, read_file_func
    ):
        create_file_func(self.command, tmp_path)
        old_path = os.environ['PATH']
        add_path(self.path)

        assert os.environ['PATH'] == f'{self.path}{os.pathsep}{old_path}'
        got = read_file_func(self.command, tmp_path)
        assert got == f'myPath{os.linesep}'

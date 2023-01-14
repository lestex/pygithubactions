import os

from pygithubactions import core
import pytest


def test_set_secret_produces_correct_command(capsys):
    core.set_secret('secret val')
    captured = capsys.readouterr()
    assert captured.out == f'::add-mask::secret val{os.linesep}'


def test_is_debug():
    os.environ['RUNNER_DEBUG'] = '1'
    assert core.is_debug() is True
    del os.environ['RUNNER_DEBUG']

    assert core.is_debug() is False


def test_set_failed_sets_correct_exit_code_failure_message(capsys):
    failure_message = 'Failure message'
    with pytest.raises(SystemExit) as e:
        core.set_failed(failure_message)

    captured = capsys.readouterr()
    assert e.type == SystemExit
    assert e.value.code == 1
    assert captured.out == f'::error::{failure_message}{os.linesep}'


def test_set_failed_escapes_failure_message(capsys):
    failure_message = 'Failure \r\n\nmessage\r'
    with pytest.raises(SystemExit):
        core.set_failed(failure_message)

    captured = capsys.readouterr()
    assert captured.out == f'::error::Failure %0D%0A%0Amessage%0D{os.linesep}'


def test_debug_sets_correct_message(capsys):
    core.debug('Debug')
    captured = capsys.readouterr()
    assert captured.out == f'::debug::Debug{os.linesep}'


def test_debug_escapes_message(capsys):
    core.debug('\r\ndebug\n')
    captured = capsys.readouterr()
    assert captured.out == f'::debug::%0D%0Adebug%0A{os.linesep}'


def test_warning_sets_correct_message(capsys):
    core.warning('Warning')
    captured = capsys.readouterr()
    assert captured.out == f'::warning::Warning{os.linesep}'


def test_warning_escapes_message(capsys):
    core.warning('\r\nwarning\n')
    captured = capsys.readouterr()
    assert captured.out == f'::warning::%0D%0Awarning%0A{os.linesep}'


def test_info_sets_correct_message(capsys):
    core.info('Info message')
    captured = capsys.readouterr()
    assert captured.out == f'Info message{os.linesep}'


def test_info_escapes_message(capsys):
    core.info('\r\ninfo message\n')
    captured = capsys.readouterr()
    assert captured.out == f'\r\ninfo message\n{os.linesep}'


def test_notice_sets_correct_message(capsys):
    core.notice('Notice message')
    captured = capsys.readouterr()
    assert captured.out == f'::notice::Notice message{os.linesep}'


def test_notice_escapes_message(capsys):
    core.notice('\r\ninfo message\n')
    captured = capsys.readouterr()
    assert captured.out == f'::notice::%0D%0Ainfo message%0A{os.linesep}'


def test_set_command_echo_can_enable_echoing(capsys):
    core.set_command_echo(enabled=True)
    captured = capsys.readouterr()
    assert captured.out == f'::echo::on{os.linesep}'


def test_set_command_can_disable_echoing(capsys):
    core.set_command_echo(enabled=False)
    captured = capsys.readouterr()
    assert captured.out == f'::echo::off{os.linesep}'

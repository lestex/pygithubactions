import os

from pygithubactions.core.command import issue_command


def test_command_only(capsys):
    issue_command('some-command', {}, '')
    captured = capsys.readouterr()
    assert captured.out == f'::some-command::{os.linesep}'


def test_command_escape_message(capsys):
    issue_command(
        'some-command', {}, 'percent % percent % cr \r cr \r lf \n lf \n'
    )
    captured = capsys.readouterr()
    assert (
        captured.out
        == f'::some-command::percent %25 percent %25 cr %0D cr %0D lf %0A lf %0A{os.linesep}'  # noqa: E501
    )

    # verify literal escape sequences
    issue_command('some-command', {}, '%25 %25 %0D %0D %0A %0A')
    captured = capsys.readouterr()
    assert (
        captured.out
        == f'::some-command::%2525 %2525 %250D %250D %250A %250A{os.linesep}'
    )


def test_command_escape_property(capsys):
    issue_command(
        'some-command',
        {
            'name': 'percent % percent % cr \r cr \r lf \n lf \n colon : colon : comma , comma ,'  # noqa: E501
        },
        '',
    )
    captured = capsys.readouterr()
    assert (
        captured.out
        == f'::some-command name=percent %25 percent %25 cr %0D cr %0D lf %0A lf %0A colon %3A colon %3A comma %2C comma %2C::{os.linesep}'  # noqa: E501
    )

    # Verify literal escape sequences
    issue_command(
        'some-command',
        {},
        '%25 %25 %0D %0D %0A %0A %3A %3A %2C %2C',
    )
    captured = capsys.readouterr()
    assert (
        captured.out
        == f'::some-command::%2525 %2525 %250D %250D %250A %250A %253A %253A %252C %252C{os.linesep}'  # noqa: E501
    )


def test_command_with_message(capsys):
    issue_command('some-command', {}, 'some message')
    captured = capsys.readouterr()
    assert captured.out == f'::some-command::some message{os.linesep}'


def test_command_with_message_properties(capsys):
    issue_command(
        'some-command',
        {'prop1': 'value 1', 'prop2': 'value 2'},
        'some message',
    )
    captured = capsys.readouterr()
    assert (
        captured.out
        == f'::some-command prop1=value 1,prop2=value 2::some message{os.linesep}'  # noqa: E501
    )


def test_command_with_one_property(capsys):
    issue_command('some-command', {'prop1': 'value 1'}, '')
    captured = capsys.readouterr()
    assert captured.out == f'::some-command prop1=value 1::{os.linesep}'


def test_command_with_two_properties(capsys):
    issue_command(
        'some-command',
        {'prop1': 'value 1', 'prop2': 'value 2'},
        '',
    )
    captured = capsys.readouterr()
    assert (
        captured.out
        == f'::some-command prop1=value 1,prop2=value 2::{os.linesep}'
    )


def test_command_with_three_properties(capsys):
    issue_command(
        'some-command',
        {'prop1': 'value 1', 'prop2': 'value 2', 'prop3': 'value 3'},
        '',
    )
    captured = capsys.readouterr()
    assert (
        captured.out
        == f'::some-command prop1=value 1,prop2=value 2,prop3=value 3::{os.linesep}'  # noqa: E501
    )


def test_command_with_non_string_props(capsys):
    issue_command(
        'some-command',
        {
            'prop1': {'test': 'object'},
            'prop2': 123,
            'prop3': True,
        },
        {'test': 'object'},
    )

    captured = capsys.readouterr()
    part_out = '::some-command prop1={"test"%3A "object"},prop2=123,prop3=true::{"test": "object"}'  # noqa: E501
    assert captured.out == f'{part_out}{os.linesep}'

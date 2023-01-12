from dataclasses import dataclass
import json
from typing import Any


def to_command_value(inp: Any) -> str:
    """Sanitizes an input into a string so it can
    be passed into issue_command safely.

    Args:
        inp (Any): Input value

    Returns:
        str: Sanitized input
    """
    if inp == '':
        return ''
    if isinstance(inp, str):
        return inp

    return json.dumps(inp)


@dataclass
class AnnotationProperties:
    # A title for the annotation.
    title: str = ''

    # The path of the file for which the annotation should be created.
    file: str = ''

    # The start line for the annotation.
    startLine: int = 0

    # The end line for the annotation. Defaults to `startLine`
    # when `startLine` is provided.
    endLine: int = 0

    # The start column for the annotation. Cannot be sent when
    # `startLine` and `endLine` are different values.
    startColumn: int = 0

    # The end column for the annotation. Cannot be sent when
    # `startLine` and `endLine` are different values.
    # Defaults to `startColumn` when `startColumn` is provided.
    endColumn: int = 0


def to_command_properties(
    annotation_properties: AnnotationProperties | None = None,
) -> dict:
    """Returns CommandProperties object

    Args:
        annotationProperties (dict): _description_

    Returns:
        CommandProperties: CommandProperties object
    """
    if annotation_properties:
        return {
            'title': annotation_properties.title,
            'file': annotation_properties.file,
            'line': annotation_properties.startLine,
            'endLine': annotation_properties.endLine,
            'col': annotation_properties.startColumn,
            'endColumn': annotation_properties.endColumn,
        }

    return {}

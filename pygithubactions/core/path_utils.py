import os


def to_posix_path(path: str) -> str:
    """Converts the given path to the posix form. On Windows, \\ will be
    replaced with /.

    Args:
        path (str): Path to transform.

    Returns:
         (str): Posix path.
    """
    return path.replace('\\', '/')


def to_win32_path(path: str) -> str:
    """Converts the given path to the win32 form. On Linux, / will be
    replaced with \\.

    Args:
        path (str): Path to transform.

    Returns:
         (str): Win32 path.
    """
    return path.replace('/', '\\')


def to_platform_path(path: str) -> str:
    """Converts the given path to a platform-specific path.
    It does this by replacing instances of / and \\ with the platform-specific
    path separator.

    Args:
        path (str): Path to transform.

    Returns:
         (str): The platform-specific path.
    """
    path = path.replace('/', os.sep)
    path = path.replace('\\', os.sep)
    return path

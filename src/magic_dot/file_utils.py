"""
Windows file utils supporting MagicDot's concealment techniques
"""
import os
import win32file
import win32con


def nt_path(path: str) -> str:
    """
    Converts a DOS path into an NT path. If the provided path is an already an
    NT path referencing a DOS device, then the returned path is the same path.

    :param path: The path to convert
    :return: The resulted NT path
    """
    if path.startswith("\\??"):
        return path

    return f"\\??\\{path}"


def dos_path(path: str) -> str:
    """
    Converts an NT path referencing to a DOS device into a DOS path.

    :param path: The path to convert
    :return: The resulted DOS path
    """
    return path.replace("\\??\\", "")


def nt_makedirs(path: str):
    """
    Creates directories recursively. Same as os.makedirs(),
    but works with paths that have trailing dots and trailing spaces in path elements.

    :param path: The path of the directories to create
    """
    path_head, path_tail = os.path.split(dos_path(path))
    if "" == path_tail:
        return
    else:
        nt_makedirs(path_head)
        try:
            os.mkdir(nt_path(path))
        except FileExistsError:
            pass


def set_short_name(path: str, short_name: str):
    """
    Sets the short name of a file or a directory.

    :param path: The path of the file or directory
    :param short_name: The short name to set
    """
    flags = 0
    if os.path.isdir(path):
        flags = win32con.FILE_FLAG_BACKUP_SEMANTICS

    file_handle = win32file.CreateFile(
        path,
        win32con.GENERIC_ALL,
        win32con.FILE_SHARE_DELETE | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_READ,
        None,
        win32con.OPEN_EXISTING,
        flags,
        0,
    )
    win32file.SetFileShortName(file_handle, short_name)
    win32file.CloseHandle(file_handle)


def get_short_name(path: str) -> str:
    """
    Retrieves the short name of a file or a directory.

    :param path: The path of the file or the directory
    :raises NameError: Raised if the file does not have a short name
    :return: The short name of the file or the directory
    """
    parent_path = os.path.dirname(path)
    # index 9 in the tuple is the alternate file name
    # https://timgolden.me.uk/pywin32-docs/WIN32_FIND_DATA.html
    short_file_name = win32file.FindFilesW(path)[0][9]
    if short_file_name == "":
        raise NameError(f'"{parent_path}" does not have a short name')
    short_name_path = os.path.join(parent_path, short_file_name)
    return short_name_path

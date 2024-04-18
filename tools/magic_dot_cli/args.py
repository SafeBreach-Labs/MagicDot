import argparse
from enum import Enum

class ArgsCommands(Enum):
    """
    Possible arguments commands.
    """
    CREATE_INOPERABLE_FILE = 0,
    CREATE_INOPERABLE_DIR = 1,
    CREATE_IMPERSONATED_FILE = 2,
    CREATE_IMPERSONATED_DIR = 3,
    CREATE_IMPERSONATED_PROCESS = 4,
    ADD_INVISIBLE_FILE_INTO_ZIP = 5,
    DISABLE_PROCEXP = 6

def parse_args():
    parser = argparse.ArgumentParser(description="An unprivileged rootkit-like tool")
    commands_subparsers = parser.add_subparsers(title="command", dest="command", required=True)
    
    impersonate_proc_parser = commands_subparsers.add_parser(ArgsCommands.CREATE_IMPERSONATED_PROCESS.name, help="Create a process that impersonates a different process. Both Task Manager and Process Explorer will display information about the target process to impersonate to")
    impersonate_proc_parser.add_argument("-exe-path", type=str, required=True, help="Path to the executable to run")
    impersonate_proc_parser.add_argument("-impersonate-to", type=str, required=True, help="Path to the executable that the process should impersonate to")

    inoperable_file_parser = commands_subparsers.add_parser(ArgsCommands.CREATE_INOPERABLE_FILE.name, help="Create an inoperable file. This file also can't be deleted by Windows Defender")
    inoperable_file_parser.add_argument("-parent-dir-path", type=str, required=True, help="Path to the directory to create the inoperable file in")
    inoperable_file_parser.add_argument("-copy-from", type=str, help="Path to a file that contains content to write into the inoperable file")

    inoperable_dir_parser = commands_subparsers.add_parser(ArgsCommands.CREATE_INOPERABLE_DIR.name, help="Create an inoperable directory")
    inoperable_dir_parser.add_argument("-parent-dir-path", type=str, required=True, help="Path to the directory to create the inoperable directory in")
    inoperable_dir_parser.add_argument("-copy-from", type=str, help="Path to a directory that contains files to copy into the inoperable directory")

    impersonated_file_parser = commands_subparsers.add_parser(ArgsCommands.CREATE_IMPERSONATED_FILE.name, help="Create a file that impersonates a different file")
    impersonated_file_parser.add_argument("-target-file", type=str, required=True, help="Path to the file that the new file impersonates to")
    impersonated_file_parser.add_argument("-near", action="store_true", help="Create the file near the target file")
    short_name_group = impersonated_file_parser.add_mutually_exclusive_group(required=False)
    short_name_group.add_argument("-use-existing-short", action="store_true", help="Use the short name of the target file to impersonate")
    short_name_group.add_argument("-use-specific-short", type=str, help="Use the short name of the target file to impersonate")
    impersonated_file_parser.add_argument("-copy-from", type=str, help="Path to a file that contains content to write into the impersonated file")

    impersonated_dir_parser = commands_subparsers.add_parser(ArgsCommands.CREATE_IMPERSONATED_DIR.name, help="Create a directory that impersonates a different directory")
    impersonated_dir_parser.add_argument("-target-dir", type=str, required=True, help="Path to the file that the new directory impersonates to")
    impersonated_dir_parser.add_argument("-near", action="store_true", help="Create the directory near the target directory")
    short_name_group = impersonated_dir_parser.add_mutually_exclusive_group(required=True)
    short_name_group.add_argument("-use-existing-short", action="store_true", help="Use the short name of the target file to impersonate")
    short_name_group.add_argument("-use-specific-short", action="store_true", help="Use the short name of the target file to impersonate")
    impersonated_dir_parser.add_argument("-copy-from", type=str, help="Path to a directory that contains files to copy into the impersonated directory")

    invisible_zip_file_parser = commands_subparsers.add_parser(ArgsCommands.ADD_INVISIBLE_FILE_INTO_ZIP.name, help="Inserts a file into a zip. The file is inserted with a name that prevents Windows' ZIP archiver from being able to list it in the ZIP.")
    invisible_zip_file_parser.add_argument("-file", type=str, required=True, help="Path to file to insert into the ZIP")
    invisible_zip_file_parser.add_argument("-zip-file", type=str, required=True, help="Path to the ZIP file")

    disable_procexp_parser = commands_subparsers.add_parser(ArgsCommands.DISABLE_PROCEXP.name, help="Exploits a DOS vulnerability in ProcExp. Creates a process that runs forever and does nothing. The process has a certain name that crashes ProcExp whenever it runs. Valid against all ProcExp versions under version 17.04 (released in April 3rd 2023).")

    return parser.parse_args()
from magic_dot.concealments import create_impersonated_dir, create_impersonated_file, create_impersonated_process, create_inoperable_dir, create_inoperable_file, create_untraceable_startup_folder, add_invisible_file_to_zip, disable_procexp
from magic_dot.file_utils import nt_path

def create_inoperable_file_from_args(args):
    inoperable_file_path = create_inoperable_file(args.parent_dir_path, args.copy_from)
    print(f"Inoperable file was created. From now on you can access the file using the following path:\n\"{inoperable_file_path}\" or using Cygwin's tools that use NT paths by default")


def create_inoperable_dir_from_args(args):
    inoperable_dir_path = create_inoperable_dir(args.parent_dir_path, args.copy_from)
    print(f"Inoperable directory was created. From now on you can access the directory using the following path:\n\"{inoperable_dir_path}\" or using Cygwin's tools that use NT paths by default")


def create_impersonated_file_from_args(args):
    impersonated_file_path = create_impersonated_file(args.target_file, args.copy_from, args.near, args.use_existing_short, args.use_specific_short)
    print(f"Impersonated file was created. From now on you can access the file using the following path:\n\"{nt_path(impersonated_file_path)}\" or using Cygwin's tools that use NT paths by default")


def create_impersonated_dir_from_args(args):
    impersonated_dir_path = create_impersonated_dir(args.target_dir, args.copy_from, args.near, args.use_existing_short, args.use_specific_short)
    print(f"Impersonated directory was created. From now on you can access the directory using the following path:\n\"{nt_path(impersonated_dir_path)}\" or using Cygwin's tools that use NT paths by default")


def create_impersonated_process_from_args(args):
    return create_impersonated_process(args.impersonate_to, args.exe_path)


def add_invisible_file_to_zip_from_args(args):
    add_invisible_file_to_zip(args.zip_file, args.file)


def disable_procexp_from_args(args):
    disable_procexp()

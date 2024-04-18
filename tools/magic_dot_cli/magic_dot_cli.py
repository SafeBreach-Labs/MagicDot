from command_handlers import create_inoperable_file_from_args, create_inoperable_dir_from_args, create_impersonated_file_from_args, \
    create_impersonated_dir_from_args, create_impersonated_process_from_args, add_invisible_file_to_zip_from_args, disable_procexp_from_args, \
    create_dots_file_from_args, create_dots_dir_from_args
from args import parse_args, ArgsCommands

ARGS_COMMANDS_TO_HANDLERS = {
    ArgsCommands.CREATE_INOPERABLE_FILE: create_inoperable_file_from_args,
    ArgsCommands.CREATE_INOPERABLE_DIR: create_inoperable_dir_from_args,
    ArgsCommands.CREATE_DOTS_FILE: create_dots_file_from_args,
    ArgsCommands.CREATE_DOTS_DIR: create_dots_dir_from_args,
    ArgsCommands.CREATE_IMPERSONATED_FILE: create_impersonated_file_from_args,
    ArgsCommands.CREATE_IMPERSONATED_DIR: create_impersonated_dir_from_args,
    ArgsCommands.CREATE_IMPERSONATED_PROCESS: create_impersonated_process_from_args,
    ArgsCommands.DISABLE_PROCEXP: disable_procexp_from_args,
    ArgsCommands.ADD_INVISIBLE_FILE_INTO_ZIP: add_invisible_file_to_zip_from_args
}

def main():
    args = parse_args()

    command_int_value = ArgsCommands[args.command]
    ARGS_COMMANDS_TO_HANDLERS[command_int_value](args)


if "__main__" == __name__:
    main()
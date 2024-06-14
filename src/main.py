from cli.commands import commands
from cli.setup import setup_parser, get_command_function

def main():
    parser = setup_parser(commands)
    args = parser.parse_args()

    if args.command:
        command_spec = commands[args.command]
        action_function = get_command_function(command_spec['module'], command_spec['action'])
        action_function(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

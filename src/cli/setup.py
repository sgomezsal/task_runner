import argparse
import importlib

def setup_parser(commands):
    parser = argparse.ArgumentParser(description="CLI Task Manager")
    subparsers = parser.add_subparsers(dest="command", required=True, help='Commands')

    for command_name, command_spec in commands.items():
        sub_parser = subparsers.add_parser(command_name, help=command_spec['help'])
        for arg in command_spec['arguments']:
            kwargs = {'required': arg.get('required', False), 'help': arg['help']}
            if 'nargs' in arg:
                kwargs['nargs'] = arg['nargs']
            if 'type' in arg:
                kwargs['type'] = arg['type']
            sub_parser.add_argument(*arg['flags'], **kwargs)

    return parser


def get_command_function(module_name, action_name):
    module = importlib.import_module(module_name)
    action_function = getattr(module, action_name)
    return action_function
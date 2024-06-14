commands = {
    'add-tasks': {
        'module': 'services.task_services',
        'action': 'add_task',
        'help': 'Add a new task',
        'arguments': [
            {'flags': ['-t', '--title'], 'required': True, 'help': 'Title of the task', 'nargs': '+'},
            {'flags': ['-c', '--category'], 'required': False, 'help': 'Abbreviation of the category to add the task'}
        ]
    },
    'add-category': {
        'module': 'services.category_services',
        'action': 'add_category',
        'help': 'Add a new category',
        'arguments': [
            {'flags': ['-n', '--category-name'], 'required': True, 'help': 'Full name of the category'},
            {'flags': ['-a', '--abbreviation'], 'required': True, 'help': 'Abbreviation for the category'}
        ]
    },
    'delete-item': {
        'module': 'services.item_services',
        'action': 'delete_item',
        'help': 'Delete an item by category and index',
        'arguments': [
            {'flags': ['-c', '--category'], 'required': True, 'help': 'Abbreviation of the category'},
            {'flags': ['-i', '--index'], 'required': True, 'type': int, 'help': 'Index of the item to delete'}
        ]
    }
}
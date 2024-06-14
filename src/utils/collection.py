
def find_item_index(data, category, title):
    """Find the index of a task by title in a specified category."""
    category_info = data.get(category, {})
    items = category_info.get('items', [])
    return next((i for i, item in enumerate(items) if item['title'].lower() == title.lower()), None)
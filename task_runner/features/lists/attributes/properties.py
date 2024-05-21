def parse_properties(properties_list):
    """Parse the input properties from command line."""
    properties = []
    for prop in properties_list:
        if '=' in prop:
            name, value = prop.strip('@').split('=', 1)
            properties.append((name, value.strip('"\'')))
        else:
            properties.append((prop.strip('@'), None))
    return properties
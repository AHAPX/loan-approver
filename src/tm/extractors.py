def extract(data, name):
    names = name.split('.', 1)
    value = data.get(names[0])
    if not value:
        return value
    if len(names) > 1 and isinstance(value, dict):
        value = extract(value, names[1])
    return value

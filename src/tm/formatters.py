TYPES = {
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
}


class BaseFormatter():
    formatter = {}

    def format(self, key, value):
        data = self.formatter.get(key)
        return data and data(value)


class TypeFormatter(BaseFormatter):
    formatter = TYPES

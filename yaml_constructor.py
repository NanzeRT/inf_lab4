class YamlConstructor:
    def __init__(self, data: dict|list|str):
        self.data = data
    
    def _construct(self, data: dict|list|str, depth: int = 0, parent_type: type = None) -> str:
        if isinstance(data, dict):
            return self._construct_dict(data, depth, parent_type)
        elif isinstance(data, list):
            return self._construct_list(data, depth, parent_type)
        else:
            return self._construct_str(data, depth, parent_type)
    
    def _construct_dict(self, data: dict, depth: int, parent_type: type) -> str:
        result = ''
        items = list(data.items())
        if parent_type == list:
            val = self._construct(items[0][1], depth + 1, dict)
            result += f'{self._reserved_word_safe(items[0][0])}: {val}'
            items = items[1:]
        else:
            result += '\n'
        for key, value in items:
            val = self._construct(value, depth + 1, dict)
            result += f'{self._get_indent(depth)}{self._reserved_word_safe(key)}: {val}'
        return result
    
    def _construct_list(self, data: list, depth: int, parent_type: type) -> str:
        if parent_type == dict:
            depth -= 1

        result = ''
        if parent_type == list:
            val = self._construct(data[0], depth + 1, list)
            result += f'- {val}'
            data = data[1:]
        else:
            result += '\n'

        for item in data:
            val = self._construct(item, depth + 1, list)
            result += f'{self._get_indent(depth)}- {val}'
        return result

    def _construct_str(self, data: str, depth: int, parent_type: type) -> str:
        if '\n' in data:
            result = '|-\n'
            for line in data.splitlines():
                result += f'{self._get_indent(depth)}{line}\n'
            return result
        else:
            return self._reserved_word_safe(data) + '\n'
    
    _SPECIAL_CHARS = '[]{}:,#&*!|>\'"%@`'
    _RESERVED_WORDS = ['true', 'false', 'null', 'y', 'n', 'yes', 'no', 'on', 'off']

    def _reserved_word_safe(self, word: str) -> str:
        if word in self._RESERVED_WORDS or any(char in word for char in self._SPECIAL_CHARS):
            return f'"{word}"'
        return word

    def _get_indent(self, depth: int) -> str:
        return '  ' * depth

    def construct(self) -> str:
        return self._construct(self.data)


if __name__ == '__main__':
    data = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': {
            'key4': 'value4',
            'key5': 'value5\nwdhkjwahdkjaw\nhdawhdawhd',
        },
        'key6': [
            'value6',
            'value7',
            'value8',
        ],
        'key7': [
            {
                'key8': 'value9',
                'key9': 'value10',
            },
            {
                'key10': 'value11',
                'key11': 'value12',
            },
        ],
        'key12': 'value13',
        'key13': 'value14',
    }

    constructor = YamlConstructor(data)
    print(constructor.construct())
class NestedDict:
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, NestedDict(value))
            else:
                setattr(self, key, value)

# Example usage:
data = {
    'level1': {
        'level2_a': 1,
        'level2_b': {
            'level3_c': 2
        }
    },
    'level1_d': 3
}

nested_obj = NestedDict(data)
print(nested_obj.get('level1'))
print(nested_obj.level1.level2_a)
print(nested_obj.level1.level2_b.level3_c)
print(nested_obj.level1_d)

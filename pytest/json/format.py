

import json

with open(r'test_data\android\trace\systrace.txt', 'r') as fi:
    data = json.load(fi)
    with open('test_output', 'w') as fo:
        json.dump(data, fo, ensure_ascii=False, indent=4, separators=(',', ':'))



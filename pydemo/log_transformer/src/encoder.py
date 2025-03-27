import os
from pylib.basic.file import json_read, json_write

_tag_map = {}
_file_name = None

ID_IGORNED = -100


# ID_TID_OFFSET = 0
ID_EVENT_OFFSET = 10000
# ID_TAG_OFFSET = 30000
# ID_START = 31000

def init(file_name):
    global _tag_map
    global _file_name
    _file_name = file_name
    if os.path.exists(file_name):
        _tag_map = json_read(file_name)
    

def close():
    json_write( _file_name, _tag_map)


def ID_TID(tid):
    return int(tid)


def ID_TAG(tag):
    if tag not in _tag_map:
        _tag_map[tag] = len(_tag_map)
    return _tag_map[tag]


def ID_EVENT(event):
    return event + ID_EVENT_OFFSET






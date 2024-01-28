from dataclasses import dataclass, field
from typing import List
from datetime import datetime
import dateutil

@dataclass(order=True)
class Article(object):
    _id: int
    author_id: int
    title: str = field(compare=False)
    text: str = field(repr=False, compare=False)
    tags: List[str] = field(default=list(), repr=False, compare=False)
    created: datetime = field(default=datetime.now(), repr=False, compare=False)
    edited: datetime = field(default=datetime.now(), repr=False, compare=False)

    def __post_init__(self):
       if type(self.created) is str:
           self.created = dateutil.parser.parse(self.created)

       if type(self.edited) is str:
           self.edited = dateutil.parser.parse(self.edited)
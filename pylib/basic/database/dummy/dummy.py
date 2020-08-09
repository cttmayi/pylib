#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

class DbDummy():
    def __init__(self):
        self.cur_id = None
        super().__init__()

    def create(self, table_name):
        self.__contents__ = {}
        self.__contents__[table_name] = {}
        return True


    def query_id(self, table_name, id):
        contents = self.__contents__[table_name]
        if id in contents:
            return contents[id]
        return None


    def query(self, table_name, cond=None):
        contents = self.__contents__[table_name]
        ret = []
        for k in contents.keys():
            content = contents[k]
            ret.append(content)
        return ret


    def update(self, table_name, id, db_body):

        contents = self.__contents__[table_name]
        if id in contents:
            content = contents[id]
            for u in db_body:
                content[u] = db_body[u]
            return True
        return False


    def insert(self, table_name, db_body, id=None):
        contents = self.__contents__[table_name]

        if id == None:
            id = str(self.__get_id())

        contents[id] = db_body
        contents[id]['_id'] = id
        return id


    def delete(self, table_name, id):
        contents = self.__contents__[table_name]
        if id in contents:
            del contents[id]
            return True
        return False
    
    def __get_id(self):
        while(True):
            cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            if self.cur_id != cur_time:
               self.cur_id = cur_time
               break
        return self.cur_id
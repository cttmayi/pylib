#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import time


from elasticsearch import Elasticsearch


DB_DOC_TYPE = "news"
HITS = "hits"
SOURCE = "_source"
ID = "_id"

es = Elasticsearch(maxsize=25)

class DbElasticsearch():

    def __init__(self):
        self.es = es
        super().__init__()


    def create(self, table_name):
        if not self.es.indices.exists(index=table_name):
            self.es.indices.create(index=table_name)
            return True
        return False


    def query_id(self, table_name, id):
        res = self.query(table_name, {ID : id})
        if len(res) > 0:
            return res[0]
        return None


    def query(self, table_name, conds=None, from_=0, size=10000):
        self.es.indices.refresh(index=table_name)

        if conds is not None:
            query_body = {
                "query" : {
                    "bool": {
                        "must":[]
                    }
                }
            }

            for key in conds.keys():
                cond = conds[key]
                query_body['query']['bool']['must'].append({'match': {key: cond}})
        else:
            query_body = {
                'query' : {"match_all" : {}},
            }

        res_list = self.es.search(index=table_name, body=query_body, from_=from_, size=size)[HITS][HITS]
        return self._to_list(res_list)

    
    @staticmethod
    def _to_list(res_list):
        content_list = []
        for res in res_list:
            content = res[SOURCE]
            content[ID] = (res[ID])
            content_list.append(content)
        return content_list


    def update(self, table_name, id, db_body):
        update_body = {
            'doc': db_body
        }
        self.es.update(index=table_name, id=id, body=update_body)


    def insert(self, table_name, db_body, id=None):
        if id is None:
            id = self.es.index(index=table_name,  body=db_body)[ID]
        else:
            self.es.index(index=table_name,  id=id, body=db_body)
        self.es.indices.refresh(index=table_name)
        return id


    def delete(self, table_name, id):
        try:
            return self.es.delete(index=table_name, id=id)
        except:
            return None


    def refresh(self, table_name):
        self.es.indices.refresh(index=table_name)






from llama_index.readers.web import TrafilaturaWebReader





url="https://baike.baidu.com/item/恐龙/139019"
url="https://news.mbalib.com/story/256926 "
docs = TrafilaturaWebReader().load_data([url])

from pprint import pprint 
pprint(docs[0].text)






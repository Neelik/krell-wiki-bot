import requests
from .index import Index


index_base = "https://arcadaliam.fandom.com/wiki/Page_Index"


def update_index():
    page_index = requests.get(index_base)
    index = Index(page_index.text)
    return index
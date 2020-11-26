from bs4 import BeautifulSoup
import re
import string


MAX_DEPTH = 3

attribute_lookup = {
    "The Silver Ruin": "silver_ruin",
    "Friends of the Silver Ruin": "allies",
    "Other NPCs": "npcs",
    "Locations": "locations",
    "Gods": "deities"
}


class Index(object):

    def __init__(self, response):
        self.raw = response
        self.top_levels = set()
        self.indexed_pages = self.__index_pages()


    def __toc(self):
        return self.soup_raw.find("div", {"class": "toc"})


    def __clean_text(self, text):
        text_nonum = re.sub(r'\d+', '', text.strip())
        text_nopunct = "".join([char.lower() for char in text_nonum if char not in string.punctuation])
        cleaned = text_nopunct.strip().title()
        return cleaned


    def __index_pages(self):
        indexed = []
        content = self.soup_raw.find("div", {"class": "mw-parser-output"})
        ul_lists = content.find_all("ul")
        for ul_item in ul_lists:
            li_tags = ul_item.find_all("li")
            indexed.extend([self.__clean_text(li.get_text()) for li in li_tags if not li.has_attr("class")])
        return indexed


    @property
    def soup_raw(self):
        return BeautifulSoup(self.raw, "html.parser")

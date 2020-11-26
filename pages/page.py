from bs4 import BeautifulSoup


class Page(object):
    """
        Object that represents a particular page from the Arca Daliam Wiki
    """

    def __init__(self, response):
        self.raw = response

    @property
    def soup_raw(self):
        return BeautifulSoup(self.raw, "html.parser")

    @property
    def soup_pretty(self):
        return self.soup_raw.prettify()

    def __overview_text(self):
        content = self.soup_raw.find("div", {"class": "mw-parser-output"})
        overview = content.find_all("p")
        if len(overview) > 0:
            return overview[0].get_text()
        return ""

    @property
    def character_overview(self):
        """
            Parses the soup for the Overview text of a character
        """

        return self.__overview_text()

    @property
    def npc_overview(self):
        """
            Parses the soup for the Overview text of a character
        """

        return self.__overview_text()

    @property
    def location_overview(self):
        """
            Parses the soup for the Overview text of a character
        """

        return self.__overview_text()

    @property
    def site_index(self):
        return ""

    def save_soup(self):
        with open("page-response.html", "w") as output:
            output.write(str(self.soup_pretty))

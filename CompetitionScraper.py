from selenium import webdriver
from bs4 import BeautifulSoup

from ClubScraper import ClubScraper

class CompetitionScraper:
    def __init__(self, competition_url):
        self._url = competition_url
        self._table = None
        self.teams = []

    def _scrape_table(self, row_type):
        for player in self._table.findAll("tr", {"class": row_type}):
            club_tag = player.find_next("a", {"class":"vereinprofil_tooltip tooltipstered"})
            club_link = header + club_tag["href"] + "/plus/1"
            club_link = club_link.replace("startseite", "kader")
            self.teams.append(club_link)

    def scrape_competition(self):
        driver = webdriver.Firefox()
        driver.get(self._url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        self._table = soup.find("table", {"class": "items"})
        self._scrape_table("odd")
        self._scrape_table("even")

    def scrape_club(self, competition_index):
        clubScraper = ClubScraper(self.teams[0])
        clubScraper.scrape_club()

    def __str__(self):
        return '\n'.join(map(str,self.teams))

    def __getitem__(self, item):
        return self.teams[item]

    def __setitem__(self, key, value):
        pass


if __name__ == "__main__":
    header = "https://www.transfermarkt.us"
    url = "https://www.transfermarkt.us/serie-a/startseite/wettbewerb/IT1"
    scraper = CompetitionScraper(url)
    scraper.scrape_competition()
    scraper.scrape_club(0)


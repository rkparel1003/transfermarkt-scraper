from selenium import webdriver
from bs4 import BeautifulSoup

from ClubScraper import ClubScraper
import ScraperConstants


class CompetitionScraper:
    def __init__(self, competition_url):
        self._url = competition_url
        self._table = None
        self.teams = dict()
        self.driver = webdriver.Firefox()

    def _scrape_table(self, row_type):
        for player in self._table.findAll("tr", {"class": row_type}):
            club_tag = player.find_next("a", {"class":"vereinprofil_tooltip tooltipstered"})
            club_name = club_tag.contents[0]["alt"]
            club_link = ScraperConstants.HEADER + club_tag["href"] + "/plus/1"
            club_link = club_link.replace("startseite", "kader")
            self.teams[club_name] = club_link

    def scrape_competition(self):
        self.driver.get(self._url)
        content = self.driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        self._table = soup.find("table", {"class": "items"})
        self._scrape_table("odd")
        self._scrape_table("even")

    def scrape_club(self, competition_index):
        clubScraper = ClubScraper(self.teams[0])
        clubScraper.scrape_club()

    def print_clubs(self):
        for key in self.teams:
            print(key, self.teams[key])

    def __getitem__(self, item):
        return self.teams[item]

    def __setitem__(self, key, value):
        pass

    def __del__(self):
        self.driver.quit()

if __name__ == "__main__":
    header = "https://www.transfermarkt.us"
    url = "https://www.transfermarkt.us/serie-a/startseite/wettbewerb/IT1"
    scraper = CompetitionScraper(url)
    scraper.scrape_competition()
    scraper.print_clubs()


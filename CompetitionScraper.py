from selenium import webdriver
from bs4 import BeautifulSoup


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

    def scrape_club(self):
        driver = webdriver.Firefox()
        driver.get(self._url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        self._table = soup.find("table", {"class": "items"})
        self._scrape_table("odd")
        self._scrape_table("even")

    def __str__(self):
        return '\n'.join(map(str,self.teams))

if __name__ == "__main__":
    header = "https://www.transfermarkt.us"
    url = "https://www.transfermarkt.us/serie-a/startseite/wettbewerb/IT1"
    scraper = CompetitionScraper(url)
    scraper.scrape_club()
    print(str(scraper))

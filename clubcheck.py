from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

class ClubScraper:
    def __init__(self, url):
        self._url = url
        self._table = None
        self._player_dict = dict()

    def _find_position(self, player):
        self._player_dict["position"] = player.find("td")["title"]


    def _find_nationality(self, player):
        for tag in player.findAll("img"):
            if len(tag["class"]) > 0 and tag["class"][0] == "flaggenrahmen":
                self._player_dict["nationality"] = tag["alt"]


    def _find_player_name(self, player):
        player_name = player.find("img")["title"]
        if "Joined" in player_name or "Returned" in player_name:
            player_name = player.find("a", {"class": "spielprofil_tooltip tooltipstered"}).getText()
        self._player_dict["name"] = player_name

    def _find_player_number(self, tag):
        number_tag = tag.find_next("td", {"class":"zentriert"})
        self._player_dict["number"] = number_tag.getText()
        return number_tag

    def _find_player_birthday(self, tag):
        birthday_tag = tag.find_next("td", {"class":"zentriert"})
        self._player_dict["birthday"] = birthday_tag.getText()
        return birthday_tag

    def _find_player_height(self, tag):
        height_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict["height"] = height_tag.getText()
        return height_tag

    def _find_player_foot(self, tag):
        foot_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict["foot"] = foot_tag.getText()
        return foot_tag

    def _find_player_join_date(self, tag):
        join_date_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict["join_date"] = join_date_tag.getText()
        return join_date_tag

    def _find_player_contract(self, tag):
        contract_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict["contract"] = contract_tag.getText()
        return contract_tag

    def _find_player_value(self, tag):
        value_tag = tag.find_next("td", {"class": "rechts hauptlink"})
        self._player_dict["value"] = value_tag.getText()
        return value_tag

    def _scrape_row(self, player):
        self._find_player_name(player)
        self._find_nationality(player)
        self._find_position(player)
        number_tag = self._find_player_number(player)
        birthday_tag = self._find_player_birthday(number_tag)
        # blank
        blank_tag = birthday_tag.find_next("td", {"class": "zentriert"})
        height_tag = self._find_player_height(blank_tag)
        foot_tag = self._find_player_foot(height_tag)
        join_date_tag = self._find_player_join_date(foot_tag)
        # blank
        blank_tag = join_date_tag.find_next("td", {"class": "zentriert"})
        contract_tag = self._find_player_contract(blank_tag)
        value_tag = self._find_player_value(contract_tag)
    def _scrape_table(self, row_type):
        for player in self._table.findAll("tr", {"class":row_type}):
            self._scrape_row(player)
        print(self._player_dict.values())

    def scrape_club(self):
        driver = webdriver.Firefox()
        driver.get(self._url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        self._table = soup.find("table", {"class":"items"})
        self._scrape_table("odd")
        self._scrape_table("even")


if __name__ == "__main__":
    url = "https://www.transfermarkt.us/ac-milan/kader/verein/5/saison_id/2019/plus/1"
    scraper = ClubScraper(url)
    scraper.scrape_club()
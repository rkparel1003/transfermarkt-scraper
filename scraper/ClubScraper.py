from bs4 import BeautifulSoup
from typing import MutableMapping
import requests

class ClubScraper:
    def __init__(self, name: str, url: str):
        self._url = url
        self._table = None
        self._club_name = name
        self._player_dict = dict()
        self._current_player_number = int()

    '''
        Extracts the player's number from the provided tag.
    '''
    def _find_player_number(self, tag: BeautifulSoup) -> BeautifulSoup:
        number_tag = tag.find_next("td", {"class": "zentriert"})
        self._current_player_number = number_tag.getText()
        self._player_dict[self._current_player_number] = dict()
        self._player_dict[self._current_player_number]["number"] = number_tag.getText()
        return number_tag

    '''
        Extracts the player's position from the provided tag.
    '''
    def _find_position(self, player: BeautifulSoup) -> None:
        self._player_dict[self._current_player_number]["position"] = player.find("td")["title"]

    '''
        Extracts the player's nationality from the provided tag.
    '''
    def _find_nationality(self, player: BeautifulSoup) -> None:
        for tag in player.findAll("img"):
            if len(tag["class"]) > 0 and tag["class"][0] == "flaggenrahmen":
                self._player_dict[self._current_player_number]["nationality"] = tag["alt"]

    '''
        Extracts the player's name from the provided tag.
    '''
    def _find_player_name(self, player: BeautifulSoup) -> None:
        player_name = player.find("img")["title"]
        player_name = player.find("a", {"class": "spielprofil_tooltip tooltipstered"}).getText()
        self._player_dict[self._current_player_number]["name"] = player_name

    '''
        Extracts the player's birthday from the provided tag.
    '''
    def _find_player_birthday(self, tag: BeautifulSoup) -> BeautifulSoup:
        birthday_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["birthday"] = birthday_tag.getText()
        return birthday_tag

    '''
        Extracts the player's height from the provided tag.
    '''
    def _find_player_height(self, tag: BeautifulSoup) -> BeautifulSoup:
        height_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["height"] = height_tag.getText()
        return height_tag

    '''
        Extracts the player's foot preference from the provided tag.
    '''
    def _find_player_foot(self, tag: BeautifulSoup) -> BeautifulSoup:
        foot_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["foot"] = foot_tag.getText()
        return foot_tag

    '''
        Extracts the player's join_date from the provided tag.
    '''
    def _find_player_join_date(self, tag: BeautifulSoup) -> BeautifulSoup:
        join_date_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["join_date"] = join_date_tag.getText()
        return join_date_tag

    '''
        Extracts the player's contract expiration date from the provided tag.
    '''
    def _find_player_contract(self, tag: BeautifulSoup) -> BeautifulSoup:
        contract_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["contract"] = contract_tag.getText()
        return contract_tag

    '''
        Extracts the player's value from the provided tag.
    '''
    def _find_player_value(self, tag: BeautifulSoup) -> BeautifulSoup:
        value_tag = tag.find_next("td", {"class": "rechts hauptlink"})
        self._player_dict[self._current_player_number]["value"] = value_tag.getText(strip=True)
        return value_tag

    '''
        Each player is one row in the table.
        Sequentially extracts each piece of data from this tag.
    '''
    def _scrape_row(self, player: BeautifulSoup) -> None:
        number_tag = self._find_player_number(player)
        self._find_player_name(player)
        self._find_nationality(player)
        self._find_position(player)
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

    '''
        Scrapes every row in the table that matches the odd or even row type provided.
    '''
    def _scrape_table(self, row_type: str) -> None:
        for player in self._table.findAll("tr", {"class": row_type}):
            self._scrape_row(player)

    '''
        Extracts the table of player data from the url provided in the constructor.
        Scrapes over each row of the table and returns a dictionary of all players in this club.
    '''
    def scrape_club(self) -> MutableMapping[str, MutableMapping[str, str]]:
        content = requests.get(self._url)
        soup = BeautifulSoup(content, features="html.parser")
        self._table = soup.find("table", {"class": "items"})
        self._scrape_table("odd")
        self._scrape_table("even")
        return self._player_dict
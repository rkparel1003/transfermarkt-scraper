from bs4 import BeautifulSoup
from typing import MutableMapping
import requests

import scraper.ScraperConstants as ScraperConstants
from scraper.Player import Player

class ClubScraper:
    def __init__(self, name: str, url: str):
        self._url = url
        self._table = None
        self._club_name = name
        self._players = dict()

    '''
        Extracts the player's number from the number column
    '''
    def _find_number(self, number_column: BeautifulSoup) -> str:
        number_tag = number_column.find_next("div", {"class": "rn_nummer"})
        return number_tag.getText() 

    '''
        Extracts player's name from the name column
    '''
    def _find_name(self, name_column: BeautifulSoup) -> str:
        # posrela_tag = player_row.find_next('td', {'class': 'posrela'})
        name_tag = name_column.find_next('a', {'class': 'spielprofil_tooltip'})
        return name_tag.getText()

    '''
        Extracts the player's position from the name column
    '''
    def _find_position(self, name_column: BeautifulSoup) -> str:
        return name_column.findAll('td')[-1].getText()

    '''
        Extracts the player's nationality (possibly multiple) from the nationality column
    '''
    def _find_nationality(self, nat_column: BeautifulSoup) -> list:
        nationalities = nat_column.findAll('img')
        return [nat['title'] for nat in nationalities]

    '''
        Extracts the player's date of birth from the dob column
    '''
    def _find_dob(self, dob_column: BeautifulSoup) -> str:
        return dob_column.getText()

    '''
        Extracts the player's value from the value column
    '''
    def _find_value(self, value_column: BeautifulSoup) -> str:
        return value_column.getText()

    '''
        Each player is one row in the table.
        Sequentially extracts each piece of data from this row.
        Return a new Player object that encapsulates all this data.
    '''
    def _scrape_row(self, player_row: BeautifulSoup) -> Player:
        player_data = player_row.findChildren('td')
        number = self._find_number(player_data[0])
        name = self._find_name(player_data[1])
        pos = self._find_position(player_data[1])
        dob = self._find_dob(player_data[6])
        nationalities = self._find_nationality(player_data[7])
        value = self._find_value(player_data[8])
        return Player(number, name, pos, dob, nationalities, value)


    '''
        Scrapes every row in the table that matches the odd or even row type provided.
    '''
    def _scrape_table(self, row_type: str) -> None:
        for player in self._table.findAll("tr", {"class": row_type}):
            print(self._scrape_row(player))

    '''
        Extracts the table of player data from the url provided in the constructor.
        Scrapes over each row of the table and returns a dictionary of all players in this club.
    '''
    def scrape_club(self) -> MutableMapping[str, MutableMapping[str, str]]:
        content = requests.get(self._url, headers=ScraperConstants.HEADS).content
        soup = BeautifulSoup(content, features="html.parser")
        self._table = soup.find("table", {"class": "items"})
        print(f"********** {self._club_name} **********")
        self._scrape_table("odd")
        self._scrape_table("even")
        return self._players
from bs4 import BeautifulSoup
from typing import MutableMapping, Optional, Dict
import requests
from urllib.parse import urljoin

import scraper.ScraperConstants as ScraperConstants
from scraper.ClubScraper import ClubScraper


class CompetitionScraper:
    def __init__(self, competition_url: str):
        self._url = competition_url
        self._table = None
        self.teams = dict()

    '''
        Pulls data from the rows of the table.
        Reads from all odd rows and then all even rows in the order provided.
    '''
    def _scrape_table(self, row_type: str) -> None:
        for club_row in self._table.findAll("tr", {"class": row_type}):
            first_tag = club_row.find('td', {'class': 'hauptlink no-border-links hide-for-small hide-for-pad'})
            for club in first_tag.findAll('a', {'class':'vereinprofil_tooltip'}):
                club_name = club.get_text()
                club_link = urljoin(ScraperConstants.HEADER, club['href'])
                self.teams[club_name] = club_link

    '''
        Scrape all the teams off the provided competition_url
        Looks over all of the rows of players on this page.
    '''
    def scrape_competition(self) -> None:
        content = requests.get(self._url, headers=ScraperConstants.HEADS).content
        soup = BeautifulSoup(content, features="html.parser")
        self._table = soup.find("table", {"class": "items"})
        self._scrape_table("odd")
        self._scrape_table("even")

    def scrape_players(self) -> None:
        for name in self.teams:
            self._scrape_club(name)

    '''
        Creates a club scraper and scrapes the url that the club_name parameter
        maps to in self.teams.
    '''
    def _scrape_club(self, club_name: str) -> None:
        club_scraper = ClubScraper(club_name, self.teams[club_name])
        players = club_scraper.scrape_club()

    '''
        Prints out all key value pairs of (name, club_info dictionary).
    '''
    def print_clubs(self) -> None:
        for key in self.teams:
            print(key, self.teams[key])

    def __getitem__(self, item: str) -> str:
        return self.teams[item]

    def __setitem__(self, key: str, value: str) -> None:
        self.teams[key] = value
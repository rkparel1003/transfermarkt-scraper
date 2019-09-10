from selenium import webdriver
from bs4 import BeautifulSoup
from typing import MutableMapping, Optional, Dict

from ClubScraper import ClubScraper
import ScraperConstants
import transfermarktdatabase


class CompetitionScraper:
    def __init__(self, competition_url: str):
        self._url = competition_url
        self._table = None
        self.teams = Dict[str, str]
        self.driver = webdriver.Firefox()
        self.dbms = transfermarktdatabase.MyDatabase(transfermarktdatabase.SQLITE, dbname="transfermarktdb.sqlite")
        self.dbms.create_db_tables()

    '''
        Pulls data from the rows of the table.
        Reads from all odd rows and then all even rows in the order provided.
    '''
    def _scrape_table(self, row_type: str) -> None:
        for player in self._table.findAll("tr", {"class": row_type}):
            club_tag = player.find_next("a", {"class":"vereinprofil_tooltip tooltipstered"})
            club_name = club_tag.contents[0]["alt"]
            club_link = ScraperConstants.HEADER + club_tag["href"] + "/plus/1"
            club_link = club_link.replace("startseite", "kader")
            self.teams[club_name] = club_link

    '''
        Uses the selenium webdriver to scrape the competition url provided in 
        CompetitionScraper's constructor.
        Looks over all of the rows of players on this page.
    '''
    def scrape_competition(self) -> None:
        self.driver.get(self._url)
        content = self.driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        self._table = soup.find("table", {"class": "items"})
        self._scrape_table("odd")
        self._scrape_table("even")

    '''
        Scrapes all of the club urls in the teams dictionary.
    '''
    def insert_all_clubs_data(self) -> None:
        for team_name in self.teams:
            self._scrape_club(team_name)

    '''
        Creates a club scraper and scrapes the url that the club_name parameter
        maps to in self.teams.
    '''
    def _scrape_club(self, club_name: str) -> None:
        club_scraper = ClubScraper(club_name, self.teams[club_name])
        players = club_scraper.scrape_club()
        self._insert_club_data(club_name, players)

    '''
        Prints out all key value pairs of (name, club_info dictionary).
    '''
    def print_clubs(self) -> None:
        for key in self.teams:
            print(key, self.teams[key])

    '''
        Loops over every player in the current club.
        Calls for an insert query to be created with this players' data
        Tells the dbms to execute the query.
    '''
    def _insert_club_data(self, club_name: str, players: MutableMapping[str, MutableMapping[str, str]]):
        for key in players:
            player = players[key]
            insert_query_values = self._create_insert_query(club_name, player)
            self.dbms.execute_query(insert_query_values, ScraperConstants.PLAYER_INSERT)

    '''
        Creates the insert query for players.
        Pulls out every variable from the player dictionary and puts it into a string 
        formatted as a SQL Insert statement.
    '''
    def _create_insert_query(self, club_name, player: MutableMapping[str, str]) -> tuple:
        player_id = self._get_player_id()
        number = player['number']
        name = player['name']
        nationality = player['nationality']
        position = player['position']
        birthday = player['birthday']
        height = player['height']
        join_date = player['join_date']
        contract = player['contract']
        price = player['value']
        return player_id, club_name, number, name, nationality, position, birthday, height, join_date, contract, price

    '''
        Gets the unique ID for the player id.
    '''
    def _get_player_id() -> int:
        player_id = ScraperConstants.max_id
        ScraperConstants.max_id += 1
        return player_id

    '''
        Performs a single insert query onto the player database.
        values may or may not be provided.
    '''
    def single_insert(self, query, values: Optional[tuple] = None):
        self.dbms.execute_query(values, query)

    '''
        Calls the function in transfermarktdatabase to print out all player rows.
    '''
    def print_database(self) -> None:
        self.dbms.print_all_data(transfermarktdatabase.PLAYERS)

    def __getitem__(self, item: str) -> str:
        return self.teams[item]

    def __setitem__(self, key: str, value: str) -> None:
        self.teams[key] = value

    '''
        When this class leaves scope it closes the selenium webdriver.
    '''
    def __del__(self) -> None:
        self.driver.quit()

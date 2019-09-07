from selenium import webdriver
from bs4 import BeautifulSoup

from ClubScraper import ClubScraper
import ScraperConstants
import transfermarktdatabase


class CompetitionScraper:
    def __init__(self, competition_url):
        self._url = competition_url
        self._table = None
        self.teams = dict()
        self.driver = webdriver.Firefox()
        self.dbms = transfermarktdatabase.MyDatabase(transfermarktdatabase.SQLITE, dbname="transfermarktdb.sqlite")
        self.dbms.create_db_tables()

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

    def insert_all_clubs_data(self):
        for team_name in self.teams:
            self._scrape_club(team_name)

    def _scrape_club(self, club_name):
        club_scraper = ClubScraper(club_name, self.teams[club_name])
        players = club_scraper.scrape_club()
        self._insert_club_data(club_name, players)

    def print_clubs(self):
        for key in self.teams:
            print(key, self.teams[key])

    '''
        Loops over every player in the current club.
        Calls for an insert query to be created with this players' data
        Tells the dbms to execute the query.
    '''
    def _insert_club_data(self, club_name, players):
        for key in players:
            player = players[key]
            insert_query = self._create_insert_query(club_name, player)
            self.dbms.execute_query(insert_query)

    '''
        Creates the insert query for players.
        Pulls out every variable from the player dictionary and puts it into a string 
        formatted as a SQL Insert statement.
    '''
    def _create_insert_query(self, club_name, player: dict):
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
        sql_query_header = "INSERT INTO 'players'(id, team_name, number, name, nationality, position, birthday, height, join_date, contract, price) "
        sql_query_values = f"VALUES('{player_id}', '{club_name}', '{number}', '{name}', '{nationality}', '{position}', '{birthday}', '{height}', '{join_date}', '{contract}', '{price}');"
        return sql_query_header + sql_query_values

    def _get_player_id(self):
        player_id = ScraperConstants.max_id
        ScraperConstants.max_id += 1
        return player_id

    def print_database(self):
        self.dbms.print_all_data(transfermarktdatabase.PLAYERS)

    def __getitem__(self, item):
        return self.teams[item]

    def __setitem__(self, key, value):
        pass

    def __del__(self):
        self.driver.quit()

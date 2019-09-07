from selenium import webdriver
from bs4 import BeautifulSoup
import ScraperConstants
import mydatabase

class ClubScraper:
    def __init__(self, name, url):
        self._url = url
        self._table = None
        self._club_name = name
        self._player_dict = dict()
        self._current_player_number = int()
        self.driver = webdriver.Firefox()
        self.dbms = mydatabase.MyDatabase(mydatabase.SQLITE, dbname="transfermarktdb.sqlite")
        self.dbms.create_db_tables()

    def _find_player_number(self, tag):
        number_tag = tag.find_next("td", {"class": "zentriert"})
        self._current_player_number = number_tag.getText()
        self._player_dict[self._current_player_number] = dict()
        self._player_dict[self._current_player_number]["number"] = number_tag.getText()
        return number_tag

    def _find_position(self, player):
        self._player_dict[self._current_player_number]["position"] = player.find("td")["title"]

    def _find_nationality(self, player):
        for tag in player.findAll("img"):
            if len(tag["class"]) > 0 and tag["class"][0] == "flaggenrahmen":
                self._player_dict[self._current_player_number]["nationality"] = tag["alt"]

    def _find_player_name(self, player):
        player_name = player.find("img")["title"]
        if "Joined" in player_name or "Returned" in player_name:
            player_name = player.find("a", {"class": "spielprofil_tooltip tooltipstered"}).getText()
        self._player_dict[self._current_player_number]["name"] = player_name

    def _find_player_birthday(self, tag):
        birthday_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["birthday"] = birthday_tag.getText()
        return birthday_tag

    def _find_player_height(self, tag):
        height_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["height"] = height_tag.getText()
        return height_tag

    def _find_player_foot(self, tag):
        foot_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["foot"] = foot_tag.getText()
        return foot_tag

    def _find_player_join_date(self, tag):
        join_date_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["join_date"] = join_date_tag.getText()
        return join_date_tag

    def _find_player_contract(self, tag):
        contract_tag = tag.find_next("td", {"class": "zentriert"})
        self._player_dict[self._current_player_number]["contract"] = contract_tag.getText()
        return contract_tag

    def _find_player_value(self, tag):
        value_tag = tag.find_next("td", {"class": "rechts hauptlink"})
        self._player_dict[self._current_player_number]["value"] = value_tag.getText(strip=True)
        return value_tag

    def _scrape_row(self, player):
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

    def _scrape_table(self, row_type):
        for player in self._table.findAll("tr", {"class": row_type}):
            self._scrape_row(player)

    def scrape_club(self):
        self.driver.get(self._url)
        content = self.driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        self._table = soup.find("table", {"class": "items"})
        self._scrape_table("odd")
        self._scrape_table("even")

    def _get_player_id(self):
        player_id = ScraperConstants.max_id
        ScraperConstants.max_id += 1
        return player_id

    def _create_insert_query(self, player: dict):
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
        return "INSERT INTO 'players'(id, team_name, number, name, nationality, position, birthday, height, join_date, contract, price) " \
                       f"VALUES('{player_id}', '{self._club_name}', '{number}', '{name}', '{nationality}', '{position}', '{birthday}', '{height}', '{join_date}', '{contract}', '{price}');"

    def insert_club_data(self):
        for key in self._player_dict:
            player = self._player_dict[key]
            insert_query = self._create_insert_query(player)
            self.dbms.execute_query(insert_query)

    def print_database(self):
        self.dbms.print_all_data(mydatabase.PLAYERS)

    def __del__(self):
        self.driver.quit()


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def _find_position(player):
    return player.find("td")["title"]


def _find_nationality(player):
    for tag in player.findAll("img"):
        if len(tag["class"]) > 0 and tag["class"][0] == "flaggenrahmen":
            return tag["alt"]


def _find_player_name(player, player_dict):
    player_name = player.find("img")["title"]
    if "Joined" in player_name or "Returned" in player_name:
        player_name = player.find("a", {"class": "spielprofil_tooltip tooltipstered"}).getText()
    return player_name


def _scrape_table(table, row_type):
    player_dict = dict()
    for player in table.findAll("tr", {"class":row_type}):
        player_name = _find_player_name(player, player_dict)
        player_nationality = _find_nationality(player, player_dict)
        player_position = _find_position(player, player_dict)
        #number, birthday, BLANK, height, footed, join date, BLANK, end contract
        next = player.find_next("td",{"class":"zentriert"})
        player_number = next.getText()
        next = next.find_next("td", {"class": "zentriert"})
        player_birthday = next.getText()
        # this one is a blank
        next = next.find_next("td", {"class": "zentriert"})
        next = next.find_next("td", {"class": "zentriert"})
        player_height = next.getText()
        next = next.find_next("td", {"class": "zentriert"})
        player_foot = next.getText()
        next = next.find_next("td", {"class":"zentriert"})
        player_join_date = next.getText()
        # blank
        next = next.find_next("td", {"class":"zentriert"})
        next = next.find_next("td", {"class": "zentriert"})
        player_contract_until = next.getText()
        next = next.find_next("td", {"class": "rechts hauptlink"})
        player_current_value = next.getText()
        print(player_name, player_nationality, player_position,player_number, player_birthday, player_height, player_foot, player_join_date, player_contract_until, player_current_value)

def scrape_club(url:str):
    driver = webdriver.Firefox()
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    table = soup.find("table", {"class":"items"})
    _scrape_table(table, "odd")
    _scrape_table(table, "even")


if __name__ == "__main__":
    url = "https://www.transfermarkt.us/ac-milan/kader/verein/5/saison_id/2019/plus/1"
    scrape_club(url)

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def _find_nationality(player):
    for tag in player.findAll("img"):
        if len(tag["class"]) > 0 and tag["class"][0] == "flaggenrahmen":
            return tag["alt"]


def scrape_club(url:str):
    driver = webdriver.Firefox()
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    table = soup.find("table", {"class":"items"})
    for player in table.findAll("tr", {"class":"odd"}):
        player_name = player.find("img")["title"]
        if "Joined" in player_name or "Returned" in player_name:
            player_name = player.find("a",{"class":"spielprofil_tooltip tooltipstered"}).getText()
        player_nationality = _find_nationality(player)
        print(player_name, player_nationality)
    for player in table.findAll("tr", {"class":"even"}):
        player_name = player.find("img")["title"]
        if "Joined" in player_name or "Returned" in player_name:
            player_name = player.find("a", {"class": "spielprofil_tooltip tooltipstered"}).getText()
        player_nationality = _find_nationality(player)
        print(player_name, player_nationality)


if __name__ == "__main__":
    url = "https://www.transfermarkt.us/ac-milan/kader/verein/5/saison_id/2019/plus/1"
    scrape_club(url)
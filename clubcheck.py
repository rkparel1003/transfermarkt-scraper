from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

def scrape_club(url:str):
    driver = webdriver.Firefox()
    driver.get(url)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    #scrapes odd and even rows in the table
    table = soup.find("table", {"class":"items"})
    for player in table.findAll("tr", {"class":"odd"}):
        player_name = player.find("img")["title"]
        print(player_name)
        for tag in player.findAll("td", {"class":"zentriert"}):
            print(tag.getText())
    for player in table.findAll("tr", {"class":"even"}):
        player_name = player.find("img")["title"]
        print(player_name)
        for tag in player.findAll("td", {"class":"zentriert"}):
            print(tag.getText())

if __name__ == "__main__":
    url = "https://www.transfermarkt.us/ac-milan/kader/verein/5/saison_id/2019/plus/1"
    scrape_club(url)
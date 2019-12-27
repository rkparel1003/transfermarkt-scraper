from typing import Final

"""
CONSTANTS
"""

USER_AGENT :Final[str] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
HEADS = {'User-Agent': USER_AGENT}

HEADER: Final[str] = "https://www.transfermarkt.us"
GB1_URL: Final[str] = "https://www.transfermarkt.us/premier-league/startseite/wettbewerb/GB1"
ES1_URL: Final[str] = "https://www.transfermarkt.us/la-liga/startseite/wettbewerb/ES1"
IT1_URL: Final[str] = "https://www.transfermarkt.us/serie-a/startseite/wettbewerb/IT1"
L1_URL: Final[str] = "https://www.transfermarkt.us/1-bundesliga/startseite/wettbewerb/L1"
FR1_URL: Final[str] = "https://www.transfermarkt.us/ligue-1/startseite/wettbewerb/FR1"

ALL_LEAGE_URLS: Final[list] = [GB1_URL, ES1_URL, IT1_URL, FR1_URL]

CREATE_TABLE_QUERY: Final[str] = """
    CREATE TABLE players(
        id integer PRIMARY KEY,
        club_name text,
        number text,
        name text,
        position text,
        dob text,
        nationalities text,
        value text)
    """

INSERT_PLAYER_QUERY: Final[str] = """
        INSERT INTO players
        (club_name, number, name, position, dob, nationalities, value)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """       
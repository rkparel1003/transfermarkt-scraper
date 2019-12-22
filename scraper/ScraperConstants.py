from typing import Final

"""
CONSTANTS
"""

HEADER: Final[str] = "https://www.transfermarkt.us"
GB1_URL: Final[str] = "https://www.transfermarkt.us/premier-league/startseite/wettbewerb/GB1"
ES1_URL: Final[str] = "https://www.transfermarkt.us/la-liga/startseite/wettbewerb/ES1"
IT1_URL: Final[str] = "https://www.transfermarkt.us/serie-a/startseite/wettbewerb/IT1"
L1_URL: Final[str] = "https://www.transfermarkt.us/1-bundesliga/startseite/wettbewerb/L1"
FR1_URL: Final[str] = "https://www.transfermarkt.us/ligue-1/startseite/wettbewerb/FR1"

PLAYER_INSERT: Final[str] = "INSERT INTO 'players'(id, team_name, number, name, nationality, position, birthday, height, join_date," \
            " contract, price) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"

max_id = 0

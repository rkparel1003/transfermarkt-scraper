from CompetitionScraper import CompetitionScraper
from ClubScraper import ClubScraper
import ScraperConstants
import transfermarktdatabase as db


def scrape_competition_and_insert(dbms: db.TransfermarktDatabase, competition_url: str) -> None:
    competition_scraper = CompetitionScraper(competition_url, dbms)
    competition_scraper.scrape_competition()
    competition_scraper.insert_all_clubs_data()


def insert_all_competitions_data(dbms: db.TransfermarktDatabase, *all_urls: str):
    for url in all_urls:
        scrape_competition_and_insert(dbms, url)


def create_db(db_name: str):
    return db.TransfermarktDatabase(db.SQLITE, dbname=db_name)


def main():
    dbms = create_db("transfermarktdb.sqlite")
    dbms.create_db_tables()
    insert_all_competitions_data(dbms,
                                 ScraperConstants.IT1_URL,
                                 ScraperConstants.L1_URL,
                                 ScraperConstants.GB1_URL,
                                 ScraperConstants.FR1_URL,
                                 ScraperConstants.ES1_URL
                                 )


if __name__ == "__main__":
    main()

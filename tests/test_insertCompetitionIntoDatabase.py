import unittest

from CompetitionScraper import CompetitionScraper
from ClubScraper import ClubScraper
import ScraperConstants

def generic_test_scrape_and_insert(competition_url):
    scraper = CompetitionScraper(competition_url)
    scraper.scrape_competition()
    scraper.insert_all_clubs_data()
    scraper.print_database()


class TestInsertCompetitionIntoDatabase(unittest.TestCase):
    def test_IT1(self):
        generic_test_scrape_and_insert(ScraperConstants.IT1_URL)


if __name__ == '__main__':
    unittest.main()

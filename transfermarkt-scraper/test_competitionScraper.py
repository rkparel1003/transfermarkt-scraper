from unittest import TestCase

from CompetitionScraper import CompetitionScraper
from ClubScraper import ClubScraper
import ScraperConstants


def generic_test_scrape(competition_url):
    scraper = CompetitionScraper(competition_url)
    scraper.scrape_competition()
    club_name = next(iter(scraper.teams))
    club_url = scraper.teams[club_name]
    club_scraper = ClubScraper(club_name, club_url)
    club_scraper.scrape_club()


class TestCompetitionScraper(TestCase):
    def test_scrapeIT1(self):
        generic_test_scrape(ScraperConstants.IT1_URL)

    def test_scrapeGB1(self):
        generic_test_scrape(ScraperConstants.GB1_URL)

    def test_scrapeES1(self):
        generic_test_scrape(ScraperConstants.ES1_URL)

    def test_scrapeL1(self):
        generic_test_scrape(ScraperConstants.L1_URL)

    def test_scrapeFR1(self):
        generic_test_scrape(ScraperConstants.FR1_URL)

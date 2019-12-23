
from scraper.CompetitionScraper import CompetitionScraper
from scraper import ScraperConstants

def generic_test_scrape(competition_url):
    scraper = CompetitionScraper(competition_url)
    scraper.scrape_competition()
    scraper.scrape_players()
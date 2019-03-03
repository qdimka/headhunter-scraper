from unittest import TestCase

from src.scraper.scraper import HeadHunterScraper


class TestHeadHunterScraper(TestCase):
    def test_parse(self):
        vacancies = HeadHunterScraper()\
            .parse('kazan', text='it', search_field='name')
        self.assertTrue(len(vacancies) != 0)

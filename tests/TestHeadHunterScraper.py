#! /usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from scraper.scraper import HeadHunterScraper
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class TestHeadHunterScraper(TestCase):
    def test_parse(self):
        vacancies = HeadHunterScraper()\
            .parse('kazan', text='программист', search_field='name')
        self.assertTrue(len(vacancies) != 0)

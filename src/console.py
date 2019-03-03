import argparse

from scraper.scraper import HeadHunterScraper

parser = argparse.ArgumentParser(description='Collection of vacancies from the site hh.ru.')
parser.add_argument('-t', '--text', dest='text')
parser.add_argument('-c', '--city', dest='city')
parser.add_argument('-s', '--search_field', dest='search_field')
parser.add_argument('-e', '--experience', dest='experience')
parser.add_argument('-f', '--filename', dest='filename')

parser.print_help()
args = parser.parse_args()
scraper = HeadHunterScraper()
data = scraper.parse(args.city)
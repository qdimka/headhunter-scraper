import argparse
from scraper.scraper import HeadHunterScraper
from exporter.csvexporter import CsvExporter
import sys

reload(sys)
sys.setdefaultencoding('utf8')

parser = argparse.ArgumentParser(description='Collection of vacancies from the site hh.ru.')
parser.add_argument('-t', dest='text', default='it')
parser.add_argument('-c', dest='city', default='kazan')
parser.add_argument('-s', dest='search_field', default='name')
parser.add_argument('-e', dest='experience', default='doesNotMatter')
parser.add_argument('-f', dest='filename', default='output')
parser.add_argument('--exporter', default='csv')

exporters = {
    'csv': CsvExporter
}

if __name__ == "__main__":
    args = parser.parse_args()
    scraper = HeadHunterScraper()
    data = scraper\
        .parse(args.city,
               text=args.text,
               search_field=args.search_field,
               experience=args.experience)
    if data:
        filename = '{0}.{1}'.format(args.filename, args.exporter)
        exporters[args.exporter]()\
            .export(filename, data)

import csv
from exporter import Exporter


class CsvExporter(Exporter):
    def export(self, filename, data):
        with open(filename, 'wb') as csv_file:
            csv.writer(csv_file)\
                .writerows(data)


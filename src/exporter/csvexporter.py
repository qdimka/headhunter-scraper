import csv
from exporter import Exporter


class CsvExporter(Exporter):
    def export(self, filename, data):
        with open(filename, "wb") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)


import os
from unittest import TestCase
from exporter.csvexporter import CsvExporter


class TestCsvExporter(TestCase):
    def test_export(self):
        data = [[1,2,3],[1,2,3]]
        file_path = 'test.csv'
        CsvExporter().export(file_path, data)
        self.assertTrue(os.path.exists(file_path))
        os.remove(file_path)

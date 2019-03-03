from abc import abstractmethod


class Exporter(object):

    @abstractmethod
    def export(self, filename, data):
        pass
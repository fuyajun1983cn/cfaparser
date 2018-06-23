import abc
from cfaparser.utils import info
from collections import defaultdict


class Handler(abc.ABC):

    @abc.abstractmethod
    def process(self, data):
        pass

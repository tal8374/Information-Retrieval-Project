# Imports
from abc import ABCMeta, abstractmethod


class IStemmer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def stem_expression_list(self, expr_list):
        raise NotImplementedError()

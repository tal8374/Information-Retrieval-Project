import linecache
import traceback
from collections import Counter

from Configuration.config import IR_CONFIG
from Indexing.IO.ADictionary import ADictionary
import pickle

CACHE_DATA_FORMAT = "term : {} - value : {} \n"


class Cache(ADictionary):
    """
    Represents the Cache data structure
    """

    def __init__(self, input_dictionary, posting_file_path, create_default=False):
        super(Cache, self).__init__()
        self.posting_file_path = posting_file_path

        if create_default:
            return

        self.initialize_cache(input_dictionary)

    def initialize_cache(self, input_dictionary):
        """
       Creates the cache

       :rtype: void
       """

        most_frequent_terms = Cache.get_most_frequent_terms(input_dictionary)
        self.create_cache(most_frequent_terms, input_dictionary)

    def create_cache(self, most_frequent_terms, input_dictionary):
        """
        Creates the the cache

       :rtype: void
       """
        for term, frequency in most_frequent_terms:
            line_number = input_dictionary[term][1]
            dir_path = self.posting_file_path
            line_info = linecache.getline(dir_path, line_number)
            self.add_term(term, line_info[line_info.find(";") + 1:])

    def get_term(self, term_name):
        """
        Returns Data of the term if exist, None otherwise

       :rtype: Data of the term if exist, None otherwise
       """

        return self.data_dict.get(term_name)

    def add_term(self, term_name, line_info=None):
        self.data_dict[term_name] = line_info

    def add_terms(self, term_list):
        pass

    @staticmethod
    def get_most_frequent_terms(input_dictionary):
        """
       Returns the most frequent terms

       :rtype: void
       """

        counter = Counter()
        for term in input_dictionary:
            frequency = input_dictionary[term][2]
            counter[term] = frequency
        return counter.most_common(10000)

    def write_dictionary_to_file(self):
        with open('cache_data.txt', 'w') as the_file:
            for term in sorted(self.data_dict):
                the_file.write(CACHE_DATA_FORMAT.format(term, self.data_dict[term]))

    def load_data(self, file_path):
        """
        Loads the cache
        """

        self.data_dict = {}

        with open(file_path, 'rb') as handle:
            self.data_dict = pickle.load(handle)

    def save_data(self, cache_file_path):
        """
        Saves the cache
        """

        with open(cache_file_path, 'wb') as handle:
            pickle.dump(self.data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

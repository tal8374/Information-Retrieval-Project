import traceback

from Configuration.config import IR_CONFIG
from Indexing.IO.ADictionary import ADictionary
from Indexing.IO.Cache import Cache
from Indexing.IO.LineHandler import LineHandler
import linecache
import pickle

DICTIONARY_DATA_FORMAT = "term : {} - df : {} - tf : {} - pointer : {} \n"


class MainDictionary(ADictionary):
    """
    This class represent the data structure which holds the terms
    """

    def __init__(self, term_posting_file_target):
        super(MainDictionary, self).__init__()
        self.posting_file_path = term_posting_file_target

        self.line_handler = LineHandler(self.posting_file_path)

        self.cache = None
        self.documents_dictionary = {}

    def get_term(self, term_name):
        """
        Check if the cache has the record, otherwise search in the posting file

        :param term_name: The term we search for.
        :return: Term representation
        """
        data = self.cache.get_term(term_name)
        if data is not None:
            return data
        else:
            pointer = self.data_dict[term_name][1]
            line_info = linecache.getline(self.posting_file_path, pointer)
            return line_info[line_info.find(";") + 1:]

    def add_terms(self, term_obj_list):
        """
        Logic for how to add to the main term dictionary

        :param term_obj_list: The term list to add to the dictionary
        """
        for term_obj in term_obj_list:
            if term_obj.term_str not in self.data_dict:
                self.data_dict[term_obj.term_str] = [term_obj.__len__()[0], None]
            else:
                self.data_dict[term_obj.term_str][0] += term_obj.__len__()[0]

    def add_term(self, term_name, info=None):
        pass

    def initialize_terms_pointer(self, ):
        self.line_handler.calculate_lines()
        for term in self.data_dict:
            self.update_term_pointer(term)

    def update_term_pointer(self, term):
        """
        Sets the pointer to the line in posting file
        :param term:
        :return:
        """
        line_number = self.line_handler.get_line(term)
        self.data_dict[term][1] = line_number

    def filter_low_frequency_term(self):
        """
        Filter low frequency term from dictionary
        """
        filtered_dict = []
        filtered_dict_append = filtered_dict.append
        for term in self.data_dict:
            tf = int(self.data_dict[term][2])
            if tf <= 3:
                filtered_dict_append(term)
        for term in filtered_dict:
            del self.data_dict[term]

    def init_cache(self):
        self.cache = Cache(self.data_dict, self.posting_file_path)

    def write_cache_to_file(self):
        self.cache.write_cache_to_file()

    def update_term_tf(self):
        linecache_get_line = linecache.getline
        """
        Store the total TF of the term in the dictionary
        :return: 
        """
        for term in self.data_dict:
            if term == "":
                continue
            line_number = self.line_handler.get_line(term)
            content = linecache_get_line(self.posting_file_path, line_number)
            start_index_tf = content.find("[")
            end_index_tf = content.find("]")
            term = content[:content.find(";")]
            tf = content[start_index_tf + 1:end_index_tf]
            try:
                self.data_dict[term].append(tf)
            except Exception:
                print traceback.print_exc(Exception.message)

    def load_data(self, file_path):
        """
        Load the dictionary from a file
        :param file_path: A path to load the data from
        """

        self.initialize_document_dictionary(self.posting_file_path)

        self.data_dict = {}

        with open(file_path, 'rb') as handle:
            self.data_dict = pickle.load(handle)

    def save_data(self, directory_file_path):
        """
        Save the dictionary to a file
        :param file_path: Destination file path
        """
        with open(directory_file_path, 'wb') as handle:
            pickle.dump(self.data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def write_dictionary_to_file(self, dictionary_cache_directory):
        with open(dictionary_cache_directory + "\dictionary_data", 'w') as the_file:
            for term in sorted(self.data_dict):
                df = self.data_dict[term][0]
                pointer = self.data_dict[term][1]
                tf = self.data_dict[term][2]
                the_file.write(DICTIONARY_DATA_FORMAT.format(term, str(df), str(tf), str(pointer)))

    def save_cache(self, cache_file_path):
        """
        Save the dictionary

        :param void
        """

        self.cache.save_data(cache_file_path)

    def load_cache(self, dictionary_cache_directory):
        """
        Loads the dictionary

        :param void
        """

        if self.cache is None:
            self.cache = Cache({}, self.posting_file_path, True)

        self.cache.load_data(dictionary_cache_directory)

    def initialize_document_dictionary(self, posting_doc_file):
        line_counter = 1
        with open(posting_doc_file, "r") as ins:
            for line in ins:
                doc = line[:line.find(",")]
                self.documents_dictionary[doc] = line_counter
                line_counter += 1

    def update_term_data(self):
        pointer = 1
        with open(self.posting_file_path, 'r') as f:
            for line in f:
                if '' != line:
                    term = line[:line.find(";")]
                    term_tf = int(line[line.find("[") + 1: line.find("]")])
                    self.data_dict[term][1] = pointer
                    self.data_dict[term].append(term_tf)
                    pointer += 1

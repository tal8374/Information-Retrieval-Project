from abc import ABCMeta, abstractmethod
import pickle


class ADictionary(object):
    __metaclass__ = ABCMeta

    def __init__(self, input_dictionary=None):
        """
        
        :param input_dictionary: The data structure for holding the terms 
        """
        self.data_dict = {}

    def __len__(self):
        """
        
        :return: 
        """
        return len(self.data_dict)

    @abstractmethod
    def get_term(self, term_name):
        """
        Gets the term
        
        :param term_name: The term to search for
        :return: A term represented as a line from data 
        """
        raise NotImplementedError()

    @abstractmethod
    def add_term(self, term_name, line_info = None):
        """
        A function to add a term to the data structure
        
        :param term_name: 
        :param line_info: 
        :param terms_list: list of terms
        """
        raise NotImplementedError()

    @abstractmethod
    def add_terms(self, term_list):
        """
        A function to add terms to the data structure

        :param term_list: 
        :return: 
        """
        raise NotImplementedError()

    def load_data(self, file_path=None):  # TODO: Add the path from the IR_CONFIG
        """
        Load the dictionary from a file
        :param file_path: A path to load the data from
        """
        with open(file_path, 'rb') as handle:
            self.data_dict = pickle.load(handle)

    def save_data(self, file_path=None):  # TODO: Add the path from the IR_CONFIG
        """
        Save the dictionary to a file
        :param file_path: Destination file path
        """
        with open(file_path, 'wb') as handle:
            pickle.dump(self.data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

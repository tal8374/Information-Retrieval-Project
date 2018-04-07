import threading
from Observable import Observable
from Indexing.Indexer import Indexer
import sys

from QueryHandler.Searcher import Searcher


class Model(Observable):
    def __init__(self):
        super(Model, self).__init__()
        self.indexer = None
        self.to_stem = False
        self.path_for_posting_and_dictionary = ""
        self.corpus_folder_path = ""
        self.corpus_folder_path = ""
        self.path_for_posting_and_dictionary = ""

    def build_index(self, corpus_directory_path, stop_words_directory_path, to_stem, path_for_posting_and_dictionary):
        """
        Building the index

        :rtype: void
        """

        self.to_stem = to_stem
        self.path_for_posting_and_dictionary = path_for_posting_and_dictionary

        build_index_thread = threading.Thread(name="build_index_thread",
                                              target=self.run_build_index(corpus_directory_path,
                                                                          stop_words_directory_path))
        build_index_thread.start()

    def run_build_index(self, corpus_directory_path, stop_words_directory_path):
        """
        Running the thread who runs the build index method

        :rtype: void
        """
        self.indexer = Indexer(corpus_directory_path, stop_words_directory_path, self.to_stem,
                               self.path_for_posting_and_dictionary)
        self.indexer.build_index()
        super(Model, self).update_observers('Done building index', message='Done building index')

    def save_dictionary_and_cache(self, dictionary_cache_directory):
        """
        Saving the dictionary and the cache

        :rtype: void
        """

        thread_save_dictionary_and_cache = threading.Thread(name="thread_save_dictionary_and_cache",
                                                            target=self.run_save_dictionary_and_cache(
                                                                dictionary_cache_directory))
        thread_save_dictionary_and_cache.start()

    def run_save_dictionary_and_cache(self, dictionary_cache_directory):
        """
        Runs the save dictionary and cache thread

       :rtype: void
       """

        self.indexer.save_dict_and_cache(dictionary_cache_directory)
        super(Model, self).update_observers('Done saving dictionary and cache',
                                            message='Done saving dictionary and cache')

    def load_dictionary_and_cache(self, corpus_folder_path, stop_words_file_path, to_stem,
                                  path_for_posting_and_dictionary):
        """
        running the dictionary and the cache thread

       :rtype: void
       """

        self.path_for_posting_and_dictionary = corpus_folder_path
        self.stop_words_file_path = stop_words_file_path
        self.to_stem = to_stem
        self.path_for_posting_and_dictionary = path_for_posting_and_dictionary

        self.indexer = Indexer(self.corpus_folder_path, self.stop_words_file_path, self.to_stem,
                               self.path_for_posting_and_dictionary)

        load_dictionary_and_cache_thread = threading.Thread(name="load_dictionary_and_cache_thread",
                                                            target=self.run_load_dictionary_and_cache())
        load_dictionary_and_cache_thread.start()

    def run_load_dictionary_and_cache(self):
        """
        Loading the dictionary and cache method

       :rtype: void
       """

        self.indexer.load_dict_and_cache()
        super(Model, self).update_observers('Done loading dictionary and cache',
                                            message='Done loading dictionary and cache')

    def get_cache(self):
        return self.indexer.dictionary.cache

    def get_dictionary(self):
        return self.indexer.dictionary

    def get_cache_size(self):
        try:
            return sys.getsizeof(self.indexer.dictionary.cache.data_dict)
        except Exception:
            return 0

    def get_dictionary_size(self):
        return sys.getsizeof(self.indexer.dictionary.data_dict)

    def get_doc_counter(self):
        return self.indexer.number_of_docs_processed

    def get_relevant_documents(self, stop_words_path, queries, to_stem, main_dictionary, doc_posting_file_target):
        searcher = Searcher(stop_words_path, queries, to_stem, main_dictionary, doc_posting_file_target)
        searcher.detect_relevant_documents()


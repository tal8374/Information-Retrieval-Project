from Observable import Observable
from Observer import Observer


class ViewModel(Observable, Observer):
    def __init__(self, model):
        Observable.__init__(self)
        self.model = model

    def build_index(self, corpus_directory_path, stop_words_directory_path, to_stem, path_for_posting_and_dictionary):
        """
        Building the index

       :rtype: void
       """

        self.model.build_index(corpus_directory_path, stop_words_directory_path, to_stem,
                               path_for_posting_and_dictionary)

    def save_dictionary_and_cache(self, dictionary_cache_directory):
        """
         Saving the dictionary and cache

        :rtype: void
        """

        self.model.save_dictionary_and_cache(dictionary_cache_directory)

    def load_dictionary_and_cache(self, corpus_folder_path, stop_words_file_path, to_stem,
                                  path_for_posting_and_dictionary):
        """
         Loading the dictionary and cache

        :rtype: void
        """

        self.model.load_dictionary_and_cache(corpus_folder_path, "", to_stem,
                                             path_for_posting_and_dictionary)

    def update(self, *args, **kwargs):
        """
        Updating that there was change

        :rtype: void
        """
        Observable.update_observers(self)

    def get_cache(self):
        return self.model.get_cache()

    def get_dictionary(self):
        return self.model.get_dictionary()

    def get_cache_size(self):
        return self.model.get_cache_size()

    def get_dictionary_size(self):
        return self.model.get_dictionary_size()

    def get_doc_counter(self):
        return self.model.get_doc_counter()

    def get_relevant_documents(self, stop_words_path, queries, to_stem, main_dictionary, doc_posting_file_target):
        self.model.get_relevant_documents(stop_words_path,queries, to_stem, main_dictionary, doc_posting_file_target)

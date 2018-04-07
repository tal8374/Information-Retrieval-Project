from __future__ import division

import os
import traceback
from threading import Thread

import math
from sortedcollections import OrderedDict
from Indexing.IO.MainDictionary import MainDictionary
from Indexing.StopWordsContainer import StopWordsContainer
from Stemming.Stemmer import Stemmer
from Storage.CorpusHandler.FBCorpusHandler import FBCorpusHandler
from Storage.CorpusHandler.FTCorpusHandler import FTCorpusHandler
from Storage.CorpusHandler.LACorpusHandler import LACorpusHandler
from Storage.Posting.MergeFiles import MergeFiles
from Storage.Posting.TermsMergerStrategy import TermsMergerStrategy
from TextOperations.TextHelper import TextHelper
from Configuration.config import IR_CONFIG
from Storage.ReadFile import ReadFile
from Parse import Parse
from Storage import Document


class Indexer(object):
    """ 
    Inverted index data structure
    """

    def __init__(self, corpus_folder_path, stop_words_file_path, to_stem, path_for_posting_and_dictionary):
        self.stop_words_container = StopWordsContainer(stop_words_file_path)
        self.stemmer = Stemmer() if to_stem else None
        self.parser = Parse()
        self.doc_posting_fd = None
        self.doc_counter = 0  # Will be used to count the number of iterations
        self.doc_repr_list = []
        self.term_posting_fd = None
        self.global_term_dict = {}
        self.number_of_docs_processed = 0
        self.corpus_folder = corpus_folder_path
        self.stop_words_file_path = stop_words_file_path
        self.path_for_posting_and_dictionary = path_for_posting_and_dictionary

        self.stem_doc_posting_folder = os.path.join(path_for_posting_and_dictionary,
                                                    IR_CONFIG["storage"]["stem_doc_posting_folder"])
        self.doc_posting_folder = os.path.join(path_for_posting_and_dictionary,
                                               IR_CONFIG["storage"]["doc_posting_folder"])
        self.stem_term_posting_folder = os.path.join(path_for_posting_and_dictionary,
                                                     IR_CONFIG["storage"]["stem_term_posting_folder"])
        self.term_posting_folder = os.path.join(path_for_posting_and_dictionary,
                                                IR_CONFIG["storage"]["term_posting_folder"])

        if self.stemmer is not None:
            self.doc_posting_file_path = self.stem_doc_posting_folder
            self.term_posting_file_target = os.path.join(self.stem_term_posting_folder,
                                                         IR_CONFIG["storage"]["stem_term_posting_file_name"])
            self.doc_posting_file_target = os.path.join(self.stem_doc_posting_folder,
                                                        IR_CONFIG["storage"]["stem_doc_posting_file_name"])
            self.cache_file_path = os.path.join(path_for_posting_and_dictionary,
                                                IR_CONFIG["storage"]["cache_file_name_stem"])
            self.dictionary_file_path = os.path.join(path_for_posting_and_dictionary,
                                                     IR_CONFIG["storage"]["dictionary_file_name_stem"])

        else:
            self.doc_posting_file_path = self.doc_posting_folder
            self.term_posting_file_target = os.path.join(self.term_posting_folder,
                                                         IR_CONFIG["storage"]["term_posting_file_name"])
            self.doc_posting_file_target = os.path.join(self.doc_posting_folder,
                                                        IR_CONFIG["storage"]["doc_posting_file_name"])
            self.cache_file_path = os.path.join(path_for_posting_and_dictionary,
                                                IR_CONFIG["storage"]["cache_file_name"])
            self.dictionary_file_path = os.path.join(path_for_posting_and_dictionary,
                                                     IR_CONFIG["storage"]["dictionary_file_name"])

        self.dictionary = MainDictionary(self.term_posting_file_target)

    def build_index(self):
        """
        The main function for the index building.
        """
        read_file_obj = ReadFile(self.corpus_folder)

        for data in read_file_obj.extract_from_tags():
            # Get handler
            corpus_handler = self.get_handler(data)

            # Get doc object to work on
            doc_obj = self.get_doc_obj(corpus_handler)

            # Append the doc obj to the list
            self.doc_repr_list.append(doc_obj.__repr__())

            # Update counter
            self.doc_counter += 1

            # In case we got to counter limit
            if IR_CONFIG["indexer"]["doc_to_process"] == self.doc_counter:
                self.start_posting_procedure()

        # Still having data to process
        if 0 < len(self.global_term_dict.values()):
            self.start_posting_procedure()

        # Merge the results to one single file
        self.merge_terms_posting()

        if self.doc_posting_fd is not None:
            self.doc_posting_fd.close()

        self.dictionary.update_term_data()
        # self.dictionary.initialize_terms_pointer()
        # self.dictionary.update_term_tf()
        self.dictionary.filter_low_frequency_term()
        self.dictionary.init_cache()
        self.dictionary.initialize_document_dictionary(self.doc_posting_file_target)

        self.add_document_data()
        try:
            self.save_dict_and_cache(self.path_for_posting_and_dictionary)
        except:
            pass

    def update_term_data(self):
        self.dictionary.update_term_data()

    def add_document_data(self):
        if self.stemmer is not None:
            path = os.path.join(
                (os.path.join(self.path_for_posting_and_dictionary, IR_CONFIG["storage"]["stem_doc_posting_folder"])),
                IR_CONFIG["storage"]["stem_doc_posting_file_name"])
        else:
            path = os.path.join(
                (os.path.join(self.path_for_posting_and_dictionary, IR_CONFIG["storage"]["doc_posting_folder"])),
                IR_CONFIG["storage"]["doc_posting_file_name"])
        with open(path + "2", 'w') as out_file:
            with open(path, 'r') as in_file:
                for line in in_file:
                    out_file.write(self.calc_document_wight(line.rstrip('\n')) + '\n')

        # os.remove(path)
        # os.rename(path + "2", path.replace("2", ""))

    def calc_document_wight(self, line):
        splitted_line = line.split(",")
        #                       doc id, doc file name, header, date, document length, term with max tf, *term#tf*....
        document_weight = 0
        max_tf_freq = int(splitted_line[5])
        for data in splitted_line[6].split("*"):
            try:
                splitted_data = data.split("#")
                term_tf = int(splitted_data[1])
                term = splitted_data[1]
                term_df = self.dictionary.data_dict[term][0]
                num_of_docs = len(self.dictionary.documents_dictionary)
                term_idf = math.log(num_of_docs / term_df, 2)
                document_weight += ((term_tf / max_tf_freq) * term_idf) ** 2
            except Exception:
                pass  # couldn't find the term in the dictionary

        return ",".join([splitted_line[0], splitted_line[1], splitted_line[2], splitted_line[3], splitted_line[4],
                         splitted_line[5], str(document_weight ** 0.5)])

    def merge_terms_posting(self):

        if self.stemmer is None:
            merge_sorter = MergeFiles(TermsMergerStrategy(),
                                      (os.path.join(self.path_for_posting_and_dictionary,
                                                    IR_CONFIG["storage"]["term_posting_folder"])),
                                      IR_CONFIG["storage"]["term_posting_file_name"])
        else:
            merge_sorter = MergeFiles(TermsMergerStrategy(),
                                      (os.path.join(self.path_for_posting_and_dictionary,
                                                    IR_CONFIG["storage"]["stem_term_posting_folder"])),
                                      IR_CONFIG["storage"]["stem_term_posting_file_name"])

        merge_sorter.merge_sort()

    def start_posting_procedure(self):
        # Get new file descriptors for writing the buffer
        if self.term_posting_fd is None:
            self.get_new_term_posting_file()
        if self.doc_posting_fd is None:
            self.get_new_doc_posting_file()

        if self.stemmer is not None:
            self.stemmer.reset_dictionary()

        docs_thread = Thread(name='post_docs', target=self.post_docs())
        docs_thread.start()

        main_dictionary_thread = Thread(name='store_terms', target=self.dictionary.add_terms(
            self.global_term_dict.values()))
        main_dictionary_thread.start()

        # Sort the term buffer before writing to storage
        self.global_term_dict = OrderedDict(sorted(self.global_term_dict.items()))

        # Post the data to storage
        self.post_terms_and_reset_posting(docs_thread, main_dictionary_thread)

    def reset_posting(self):
        """
        Resets the data for new group of documents to process
        :return: 
        """

        if self.term_posting_fd is not None:
            self.term_posting_fd.close()
        # self.doc_posting_fd = None
        self.doc_counter = 0  # Will be used to count the number of iterations
        self.doc_repr_list = []
        self.term_posting_fd = None
        self.global_term_dict = {}

    def post_terms_and_reset_posting(self, docs_thread_in, main_dictionary_thread_in):
        """

        :return: 
        """
        term_thread = Thread(name='post_term', target=self.post_terms())

        term_thread.start()

        main_dictionary_thread_in.join()
        term_thread.join()
        docs_thread_in.join()

        self.reset_posting()

    def post_terms(self):

        for term_str, term_obj in self.global_term_dict.iteritems():
            self.term_posting_fd.write(term_obj.__repr__() + "\n")

    def post_docs(self):
        index = 0
        for doc_repr in self.doc_repr_list:
            self.number_of_docs_processed += 1
            self.doc_posting_fd.write(doc_repr + "\n")
            index += 1

    def get_doc_obj(self, corpus_handler):
        """
        Creates a new Document object from given handler.

        :param corpus_handler: An handler of the current document
        :return: A new Document to process
        """
        return Document.Document(self.global_term_dict, self.stop_words_container, self.stemmer,
                                 corpus_handler)

    def get_handler(self, data):
        """
        Gets the proper handler for the given document

        :param data: a document
        :return: An handler for specific type of documents
        """

        try:
            prefix = " ".join(data[1].split())[: 2]
            if "FB" == prefix:
                corpus_handler = FBCorpusHandler(data, self.parser)
            elif "FT" == prefix:
                corpus_handler = FTCorpusHandler(data, self.parser)
            elif "LA" == prefix:
                corpus_handler = LACorpusHandler(data, self.parser)
            else:
                raise ValueError("Prefix '%s' is not supported" % (prefix,))
            return corpus_handler
        except Exception, e:
            print traceback.print_exc(e.message)

    def get_new_term_posting_file(self):
        """ 
        """
        if self.stemmer is not None:
            self.term_posting_fd = open(os.path.join(
                (os.path.join(self.path_for_posting_and_dictionary, IR_CONFIG["storage"]["stem_term_posting_folder"])),
                TextHelper.generate_file_name()), 'a')
        else:
            self.term_posting_fd = open(os.path.join(os.path.join(self.path_for_posting_and_dictionary,
                                                                  IR_CONFIG["storage"]["term_posting_folder"]),
                                                     TextHelper.generate_file_name()), 'a')

    def get_new_doc_posting_file(self):
        """ 
        """
        if self.stemmer is not None:
            self.doc_posting_fd = open(os.path.join(
                (os.path.join(self.path_for_posting_and_dictionary, IR_CONFIG["storage"]["stem_doc_posting_folder"])),
                IR_CONFIG["storage"]["stem_doc_posting_file_name"]), 'a')
        else:
            self.doc_posting_fd = open(os.path.join(
                (os.path.join(self.path_for_posting_and_dictionary, IR_CONFIG["storage"]["doc_posting_folder"])),
                IR_CONFIG["storage"]["doc_posting_file_name"]), 'a')

    def save_dict_and_cache(self, dir_name):

        if self.stemmer is None:
            directory_file_path = os.path.join(dir_name, IR_CONFIG["storage"]["dictionary_file_name"])
            cache_file_path = os.path.join(dir_name, IR_CONFIG["storage"]["cache_file_name"])
        else:
            directory_file_path = os.path.join(dir_name, IR_CONFIG["storage"]["dictionary_file_name_stem"])
            cache_file_path = os.path.join(dir_name, IR_CONFIG["storage"]["cache_file_name_stem"])

        self.dictionary.save_data(directory_file_path)
        self.dictionary.save_cache(cache_file_path)

    def load_dict_and_cache(self):

        self.dictionary.load_data(self.dictionary_file_path)
        self.dictionary.load_cache(self.cache_file_path)


if __name__ == "__main__":
    import time

    start_time = time.time()

    i = Indexer()
    i.build_index()

    print("--- %s seconds ---" % (time.time() - start_time))

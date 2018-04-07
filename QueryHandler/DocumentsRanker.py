from __future__ import division

import linecache
import math

from collections import defaultdict

import os

from Indexing.Parse import Parse
from QueryHandler import QueryHelper
from Stemming.Stemmer import Stemmer
from Storage.CorpusDataExtractor import CorpusDataExtractor


class DocumentsRanker(object):

    def __init__(self, main_dictionary, doc_posting_file_target):
        self.doc_posting_file_target = doc_posting_file_target
        self.main_dictionary = main_dictionary
        self.documents_rank = defaultdict(int)  # doc -> rank

    def rank(self, query):
        self.documents_rank = defaultdict(int)  # For new query emptying the dictionary is needed

        doc_info = {}  # doc -> term's tf
        query_weight = len(query) ** 0.5

        for query_term in query:
            try:
                term_doc_data = self.main_dictionary.get_term(query_term)
                term_doc_data = term_doc_data[term_doc_data.find("|") + 1:]
                term_doc_data = term_doc_data.replace("{", "")
                term_doc_data = term_doc_data.replace("}", "")
                term_doc_data_splitted = term_doc_data.split(",")  # doc#tf
            except Exception:
                continue  # query term is not exists in the main dictionary
            for data in term_doc_data_splitted:
                try:
                    doc = data[: data.find("#")]
                    terms_tf = int(data[data.find("#") + 1:])
                    doc_info[doc] = terms_tf
                except Exception:
                    pass  # last one is empty string...
            self.rank_documents(doc_info, query_term, query_weight)

    def rank_documents(self, doc_info, query_term, query_weight):
        for doc in doc_info:
            doc_line = self.main_dictionary.documents_dictionary[doc]
            doc_data = linecache.getline(self.doc_posting_file_target, doc_line).rstrip('\n')
            doc_data_splitted = doc_data.split(",")
            doc_size = int(doc_data_splitted[4])
            doc_weight = float(doc_data_splitted[6])
            df = self.main_dictionary.data_dict[query_term][0]
            idf = math.log(len(self.main_dictionary.documents_dictionary) / df, 2)
            tf = doc_info[doc]
            self.documents_rank[doc] = QueryHelper.cosine_similarity(idf, tf, doc_size, query_weight, doc_weight)
            # self.documents_rank[doc] = (idf * (doc_info[doc] / doc_size)) / (query_weight * doc_weight)

    @staticmethod
    def cosine_similarity(idf, tf, size, query_weight, total_weight):
        return (idf * (tf / size)) / (query_weight * total_weight)



if __name__ == "__main__":
    dr = DocumentsRanker({}, "D:\Data_Test")
    dr.get_most_relevant_sentences(5, "FBIS3-532", "FB396004", True)

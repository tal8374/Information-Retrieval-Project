from Indexing.Parse import Parse
from Query import Query
from QueryHandler.Ranker import Ranker
from Stemming.Stemmer import Stemmer
from Storage.CorpusDataExtractor import CorpusDataExtractor


class Searcher(object):

    def __init__(self, stop_words_path, queries_list, to_stem, main_dictionary, doc_posting_file_target):
        self.doc_posting_file_target = doc_posting_file_target
        self.main_dictionary = main_dictionary
        self.to_stem = to_stem
        self._queries_list = queries_list
        self.stop_words_path = stop_words_path
        self._relevant_documents = {}  # query -> [relevant documents]
        self.ranker = Ranker(queries_list, main_dictionary, doc_posting_file_target)

        self.analyse_queries()

    def analyse_queries(self):
        analyzed_queries = []
        for query in self._queries_list:
            query_handler = Query(query, self.to_stem, self.stop_words_path)
            analyzed_queries.append(query_handler.query)
        self._queries_list = analyzed_queries

    def detect_relevant_documents(self):
        """
        Detects most relevant documents for the query

        :rtype: void
        """

        self.ranker.rank_documents()

    @property
    def relevant_documents(self):
        return self._relevant_documents

    @property
    def queries_list(self):
        return self._queries_list

    @queries_list.setter
    def query(self, value):
        self._queries_list = value


if __name__ == "__main__":
    pass

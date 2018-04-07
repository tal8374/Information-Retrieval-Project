import math
import operator

from collections import defaultdict

from QueryHandler.DocumentsRanker import DocumentsRanker


class Ranker(object):

    def __init__(self, query_list, dictionary, doc_posting_file_target):
        self.doc_posting_file_target = doc_posting_file_target
        self._query_list = query_list
        self._dictionary = dictionary
        # self._ranked_documents = defaultdict(dict)  # query -> ( document -> rank )
        self._ranked_documents = defaultdict(list)  # query -> [most ranked documents]
        self.document_ranker = DocumentsRanker(dictionary, doc_posting_file_target)

    def rank_documents(self):
        """
        Ranks the document

        :rtype: void
        """

        for query in self._query_list:
            self.document_ranker.rank(query.split())
            self.update_ranked_documents(self.document_ranker.documents_rank, query)
            self._ranked_documents[query] = self.document_ranker.documents_rank

    def update_ranked_documents(self, ranked_documents, query):
        """
         Updates for the query  the most 50 ranked document

        :rtype: void
        """

        sorted_ranked_documents = sorted(ranked_documents.items(), key=operator.itemgetter(1), reverse=True)
        index = 0
        while index < min(50, len(ranked_documents)):
            doc, rank = sorted_ranked_documents[index]
            self._ranked_documents[query].append(doc)
            index += 1

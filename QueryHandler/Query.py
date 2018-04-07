import os

from Indexing.Parse import Parse
from Indexing.StopWordsContainer import StopWordsContainer
from Stemming.Stemmer import Stemmer


class Query(object):

    def __init__(self, query, to_stem, stop_words_file_path):
        self.stemmer = Stemmer()
        self._query = query
        self.to_stem = to_stem
        self.stop_words_file_path = os.path.join(stop_words_file_path, "stop_words.txt")

        self.analyze_query()

    def analyze_query(self):
        """
         analyses the query bythe following order:
         1. Deletes the stop words
         2. Parses the query
         3. if stemmed query is required, stems the query.

         :rtype: void
         """

        self.delete_stop_words()
        self.parse_query()
        if self.to_stem:
            self.stem_query()
        self._query = " ".join(self._query)

    def stem_query(self):
        """
         Stems the query

         :rtype: void
         """

        self._query = self.stemmer.stem_expression_list(self._query)

    def delete_stop_words(self):
        """
         Deleted stop words from query

         :rtype: void
         """

        stop_words_container = StopWordsContainer(self.stop_words_file_path)
        self._query = " ".join([word for word in self._query.split() if word.lower() not in stop_words_container])

    def parse_query(self):
        """
         Parses the query

         :rtype: void
         """

        parser = Parse()
        parser.parse_text(self._query)
        self._query = parser.parsed_text

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = value


if __name__ == "__main__":
    query = Query("Falkland petroleum exploration", False)
    print query.query

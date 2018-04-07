import traceback
from collections import Counter
from Indexing.Parse import Parse
from Storage.CorpusHandler.FBCorpusHandler import FBCorpusHandler
from Storage.Term import Term

KEY_DELIMITER = ";"
FILE_OPEN_SYMBOL = "["
FILE_CLOSE_SYMBOL = "]"
DOC_LENGTH = "|"
# DOCUMENT_REPR_FORMAT = "%s%s %s%s%s {%s,%s} |%s| #%s @%s@"
#                       doc id, doc file name, header, date, document length, term with max tf, *term#tf*....
DOCUMENT_REPR_FORMAT = "%s,%s,%s,%s,%s,%s,%s"


class Document(object):
    """
    doc_str        -- The string representation of the document
    doc_id         -- The string representation of the document identification
    max_tf         -- The freq of the most frequent term in the Document 
    document_size  -- Document size determined after removing stop words.
    """

    def __init__(self, global_term_dict, stop_words_handler, stemmer, corpus_handler):
        if corpus_handler is None:
            return
        self.doc_file_name = corpus_handler.get_file_name()
        self.doc_id = corpus_handler.get_doc_id()
        self.max_tf = None
        self.max_tf_freq = 0
        self.document_size = 0
        self.text, self.header, self.date = corpus_handler.text, corpus_handler.header, corpus_handler.date
        self.terms_instances = Counter
        self.terms_list = []

        self.global_term_dict = global_term_dict
        self.stemmer = stemmer
        self.stop_words_handler = stop_words_handler

        self.initialize_document()

    def initialize_document(self):
        """
         Initilized the document object data

          :rtype: void
          """

        self.generate_terms()
        self.delete_stop_words()
        self.stem_words()
        self.update_collection_size()
        self.generate_instances()
        try:
            self.set_max_tf()
        except  Exception, e:
            self.max_tf = Term("")
        self.update_terms_list()

    def stem_words(self):
        """
         Stem the terms in the document object

          :rtype: void
          """

        if self.stemmer is not None:
            self.terms_list = self.stemmer.stem_expression_list(self.terms_list)
            self.header = self.stemmer.stem_expression_list(self.header)

    def generate_instances(self):
        """
         generates the instances of the terms

          :rtype: void
          """

        self.terms_instances = Counter(term for term in self.terms_list)

    def generate_terms(self):
        """
         Generates the terms in the header and the text

          :rtype: void
          """

        self.generate_text()
        self.generate_header()

    def generate_text(self):
        """
         Generates the terms from the text

          :rtype: void
          """
        append = self.terms_list.append
        for word in self.text:
            append(word)

    def generate_header(self):
        """
         Generates the terms from the header

          :rtype: void
          """
        append = self.terms_list.append
        for word in self.header:
            append(word)

    def update_collection_size(self):
        """
         Updates the collection size

          :rtype: void
          """

        self.document_size = len(self.terms_list)

    def set_max_tf(self):
        """
         Sets the max tf

          :rtype: void
          """

        term = self.terms_instances.most_common(1)[0]
        self.update_max_tf(term[0])
        self.update_max_tf_frequency(term[1])

    def update_max_tf(self, term):
        """
         Updating the max tf term

          :rtype: void
          """

        self.max_tf = Term(term)

    def update_max_tf_frequency(self, frequency):
        """
         Updating the max tf term's frequency

          :rtype: void
          """

        self.max_tf_freq = frequency

    def get_most_common_terms(self):
        """
         Calculates the most common terms

          :rtype: void
          """

        counter = Counter(self.doc_file_name)
        return counter(self.terms_list).most_common(1)[0]

    def update_terms_list(self):
        """
         Updates the term'slist

          :rtype: void
          """

        for term in self.terms_list:
            if term in self.global_term_dict:
                add_to_term = self.global_term_dict[term]
                add_to_term[self.doc_id] = self.terms_instances[term]
            else:
                new_term = Term(term)
                new_term[self.doc_id] = self.terms_instances[term]

                # Adding a new entry to the dict
                self.global_term_dict[new_term.__str__()] = new_term

    def delete_stop_words(self):
        self.terms_list = filter(lambda term: term not in self.stop_words_handler, self.terms_list)

    def __len__(self):
        """
         return the size of the term list

          :rtype: Number, size of the term list
          """

        return self.document_size

    def __str__(self):
        """
         Returns the doc id

          :rtype: String
          """

        return self.doc_id

    def __repr__(self):
        """
         Representation of the document object data

          :rtype: void
        """

        # return DOCUMENT_REPR_FORMAT % (self.doc_id, KEY_DELIMITER, FILE_OPEN_SYMBOL, self.doc_file_name,
        #                                FILE_CLOSE_SYMBOL, " ".join(self.header), " ".join(self.date), self.__len__(),
        #                                self.max_tf.term_str)


        term_data = []
        for term in self.terms_instances:
            term_data.append(term + "#" + str(self.terms_instances[term]))

        return DOCUMENT_REPR_FORMAT % (self.doc_id, self.doc_file_name, " ".join(self.header), " ".join(self.date),
                                       self.__len__(), self.max_tf_freq, "*".join(term_data))


if __name__ == "__main__":
    parser = Parse()
    data = ["File_Name", "Doc_id", "The World today today", "The World today today", "2 May 1993", "2 may 1993",
            "The World today today"]
    ch = FBCorpusHandler(data, parser)
    doc = Document(ch)
    doc = Document(ch)

import os

from Indexing.Parse import Parse
from Stemming.Stemmer import Stemmer
from Storage.CorpusDataExtractor import CorpusDataExtractor

EMPTY_TEXT = ""
SPACE = " "


class SentenceRanker(object):

    def __init__(self, doc_id, file_name, to_stem, doc_posting_file_target, query):
        self.query = query
        self.doc_id = doc_id
        self.to_stem = to_stem
        self.file_name = file_name
        self.doc_posting_file_target = doc_posting_file_target
        self.ranked_sentences = {}  # sentence -> rank
        self.words_idf = {}  # word -> idf

    def rank(self, query):
        query_weight = len(self.query.split()) ** 0.5

    def get_sentences_weight(self):
        sentences = self.get_document_sentences()
        self.initilize_words_idf(sentences)
        for sentence in sentences:
            sentence_weight = self.get_sentence_weight(sentence)

    def get_document_sentences(self):
        doc_text = self.get_document_text(self.doc_id, self.file_name)
        sentences = doc_text.split(".")
        for i, sentence in enumerate(sentences):
            sentences[i] = self.parse_sentence(sentences[i])
            sentences[i] = self.stem_sentence(sentences[i]) if self.to_stem else sentences[i]

    def get_document_text(self, doc_id, file_name):
        file_path = os.path.join(self.doc_posting_file_target, "corpus", file_name, file_name)
        with open(file_path, 'r') as fd:
            file_contents = fd.read()
        file_data = CorpusDataExtractor(file_contents, "DOC")
        for data in file_data:
            if data[0].strip() == doc_id:
                return data[1]
        return EMPTY_TEXT

    @staticmethod
    def parse_sentence(sentence):
        parser = Parse()
        parser.parse_text(sentence)
        return SPACE.join(parser.parsed_text)

    @staticmethod
    def stem_sentence(sentence):
        stemmer = Stemmer()
        return SPACE.join([SPACE.join(stemmer.stem_expression_list([word])) for word in sentence.split()])

    def initilize_words_idf(self, sentences):
        pass

    def get_sentence_weight(self, sentence):
        pass


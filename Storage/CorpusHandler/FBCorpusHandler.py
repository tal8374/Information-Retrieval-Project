from Storage.CorpusHandler.AFileCorpusHandler import AFileCorpusHandler

TEXT_TAGS = frozenset([
    "[Text]",
    "[Excerpt]",
    "[Excerpts]",
    "[Summary From Poor Reception]",
    "[Summary]",
    "[Summary From Poor Reception]",
    "[Text)",
    "[TEXT]",
    "[text]",
    "[Editorial Report]",
    "[Editorial report]"
])


class FBCorpusHandler(AFileCorpusHandler):
    def __init__(self, data, parser):
        super(FBCorpusHandler, self).__init__(data)
        self.header = "" if data[6] is None else data[6].lower()
        self.date = "" if data[5] is None else data[5]
        self.parser = parser
        self.extract_data()

    def extract_text(self):
        """
        Extracting text from the doc

        :rtype: void
        """

        self.extract_language()
        for tag in TEXT_TAGS:
            if tag not in self.text:
                continue
            index_of_text = self.text.find(tag)
            self.text = self.text[index_of_text + len(tag):]

        super(FBCorpusHandler, self).extract_text()

    def extract_header(self):
        """
        Extracting header from the doc

        :rtype: void
        """

        if self.header.find("<ti") != -1:
            header_open_tag_index = self.header.find("<ti")
            header_close_tag_index = self.header.find("</ti")
            self.parser.parse_text(self.header[header_open_tag_index + len("<ti>"): header_close_tag_index])

        elif self.header.find("document") != -1:
            header_open_tag_index = self.header.find("document type:")
            header_close_tag_index = self.header.find("<", header_open_tag_index)
            self.parser.parse_text(
                self.header[header_open_tag_index + len("document type:"): header_close_tag_index])
        else:
            self.parser.parse_text(self.header)

        self.header = self.parser.parsed_text

    def extract_date(self):
        """
        Extracting date from the doc

        :rtype: void
        """

        self.parser.parse_text(self.date)
        self.date = self.parser.parsed_text

    def extract_language(self):
        if self.text.find("Language: <F P=") == -1:
            return
        start_language_index = self.text.find(">") + 2
        end_language_index = self.text.find("</") - 1
        language = self.text[start_language_index: end_language_index]
        self.language = language.lower()

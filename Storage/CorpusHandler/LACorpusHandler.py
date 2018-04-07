from Storage.CorpusHandler.AFileCorpusHandler import AFileCorpusHandler


class LACorpusHandler(AFileCorpusHandler):
    def __init__(self, data, parser):
        super(LACorpusHandler, self).__init__(data)
        self.header = "" if data[3] is None else data[3].lower()
        self.date = "" if data[4] is None else data[4]
        self.parser = parser
        self.extract_data()

    def extract_text(self):
        """
        Extracting text from the doc
    
        :rtype: void
        """

        self.text = self.text.replace("<P>", "").replace("</P>", "")
        super(LACorpusHandler, self).extract_text()

    def extract_header(self):
        """
        Extracting header from the doc

        :rtype: void
        """

        self.header = self.header.replace("<p>", "").replace("</p>", "")
        self.parser.parse_text(self.header)
        self.header = self.parser.parsed_text

    def extract_date(self):
        """
        Extracting date from the doc

        :rtype: void
        """

        self.date = " ".join(self.date.split()[1:4])
        self.parser.parse_text(self.date)
        self.date = self.parser.parsed_text

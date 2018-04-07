from Storage.CorpusHandler.AFileCorpusHandler import AFileCorpusHandler


class FTCorpusHandler(AFileCorpusHandler):
    def __init__(self, data, parser):
        super(FTCorpusHandler, self).__init__(data)
        self.header = "" if data[3] is None else data[3].lower()
        self.date = "" if data[4] is None else data[4]
        self.parser = parser
        self.extract_data()

    def extract_text(self):
        """
        Extracting text from the doc

        :rtype: void
        """

        super(FTCorpusHandler, self).extract_text()

    def extract_header(self):
        """
        Extracting header from the doc

        :rtype: void
        """

        self.header = self.header[3:]
        self.parser.parse_text(self.header)
        self.header = self.parser.parsed_text

    def extract_date(self):
        """
        Extracting date from the doc

        :rtype: void
        """

        self.date = [self.date[4:6] + "/" + self.date[2:4] + "/" + self.date[0:2]]

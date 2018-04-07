from abc import ABCMeta, abstractmethod


class AFileCorpusHandler(object):
    __metaclass__ = ABCMeta

    def __init__(self, data):
        self.file_name = data[0]
        self.doc_id = " ".join(data[1].split())
        self.text = "" if data[2] is None else data[2]
        self.language = "unknown"
        self.time = None
        self.header = None

    def extract_data(self):
        """
        Extracting data (header, date, text)  from the doc

        :rtype: void
        """

        self.extract_header()
        self.extract_date()
        self.extract_text()

    @abstractmethod
    def extract_header(self):
        raise NotImplementedError

    @abstractmethod
    def extract_date(self):
        raise NotImplementedError

    def extract_text(self):
        self.parser.parse_text(self.text)
        self.text = self.parser.parsed_text

    def get_text(self):
        """
        Returns the text value

        :rtype: String[]
        """

        return self.text

    def get_header(self):
        """
        Returns the header value

        :rtype: String[]
        """

        return self.header

    def get_time(self):
        """
        Returns the date value

        :rtype: String[]
        """

        return self.time

    def get_file_name(self):
        """
        Returns the file name value

        :rtype: String[]
        """

        return self.file_name

    def get_doc_id(self):
        """
        Returns the text value

        :rtype: String[]
        """

        return self.doc_id

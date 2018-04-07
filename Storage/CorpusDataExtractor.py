from Configuration.config import IR_CONFIG


class CorpusDataExtractor(object):
    """
    This file gives an iterator over the documents as a collection in the file stream given
    """

    def __init__(self, file_contents_as_stream, open_tag):
        self.__current_list_index = 0
        self.open_tag, self.close_tag = CorpusDataExtractor.wrap_tag(open_tag)
        self.splitted_list = file_contents_as_stream.split(self.close_tag)
        self.__initialize_finder_var()

    def __initialize_finder_var(self):
        """
        Set all indexes to 0
        """
        self.cut_from = 0
        self.end_cut_from = 0
        self.seek_from = 0

    @staticmethod
    def wrap_tag(tag):
        """
        Gets a tag 
            example: "DOC" -> ("<DOC>", "</DOC>")
        
        :param tag: tag to be wrapped as a string 
        :return: A tuple (open and close) which has the wrapped tag
        """
        return "<%s>" % tag, "</%s>" % tag

    def __get_data_from_tag(self, current_text, tag):
        """
        
        :param current_text: The text which we need to extract the info from
        :param tag: The tag in the text to extract the data from
        :return:  None if not found, A string representing the inner tag value otherwise
        """
        self.__initialize_finder_var()
        op_tag, close_tag = CorpusDataExtractor.wrap_tag(tag)

        try:
            self.cut_from = current_text.index(op_tag, self.seek_from) + len(op_tag)
            self.end_cut_from = current_text.index(close_tag, self.seek_from)
            self.seek_from = current_text.index(close_tag, self.seek_from) + len(close_tag)

        # We didn't find the tag so we will not extract data
        except ValueError:
            return None

        # We found a string between the tags so we return the string using slicing and the indexes we calculated
        return current_text[self.cut_from: self.end_cut_from]

    def next(self):
        """
        An iterator which iterates over the documents of the text stream
        
        :return: The next list containing the desired data
        """

        # Extract Data
        if self.__current_list_index <= (len(self.splitted_list) - 2):
            document_as_str = " ".join(self.splitted_list[self.__current_list_index].split())[len(self.open_tag):]
            self.__current_list_index += 1

            # Check for text
            text = self.__get_data_from_tag(document_as_str, IR_CONFIG["read_file"]["conditional_tag"])
            if text is None:
                return self.next()

            doc_no = self.__get_data_from_tag(document_as_str, IR_CONFIG["read_file"]["id_tag"])
            headline = self.__get_data_from_tag(document_as_str, IR_CONFIG["read_file"]["headline_tag"])
            date = self.__get_data_from_tag(document_as_str, IR_CONFIG["read_file"]["date_tag"])
            date1 = self.__get_data_from_tag(document_as_str, IR_CONFIG["read_file"]["date1_tag"])
            header = self.__get_data_from_tag(document_as_str, IR_CONFIG["read_file"]["header_tag"])

            return [doc_no, text, headline, date, date1, header]
        else:
            # In case we don't have any more documents in the text stream
            raise StopIteration

    def __iter__(self):
        """
        Makes the class iterable
        :return: 
        """
        return self


if __name__ == "__main__":
    with open(r"D:\Data_Test\corpus\FB396004\FB396004", 'r') as fd:
        file_contents = fd.read()

    for i in CorpusDataExtractor(file_contents, "DOC"):
        print i

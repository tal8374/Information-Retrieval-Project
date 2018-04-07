DICT_FORMAT = "{%s#%s},"
TERM_FORMAT = "%s; %s%s%s "
KEY_DELIMITER = ";"
TOTAL_TF_OPEN = "["
TOTAL_TF_CLOSE = "]"
DICT_START_DELIMITER = "|"


class Term(object):
    """
    Represents a term after parsing and eliminating stop words.
     
    Used for writing in and out from posting files
    """

    def __init__(self, term_str):
        """
        
        :param term_str: A string which represent a term's name  
        """
        self.term_str = term_str
        self.term_freq_dict = {}  # {doc : number of times in a doc}

    def __setitem__(self, doc_id, freq_in_doc):
        """
        Adds a new pair of doc identification and the frequency of a term in a document.
        
        :param doc_id: The document identification - unique value 
        :param freq_in_doc: The number of times the term  appeared in the document
        """
        self.term_freq_dict.update({doc_id: freq_in_doc})

    def __str__(self):
        """
        
        :return: String representation of the Term 
        """

        return self.term_str

    def __len__(self):
        """
        Get the total number of keys and the some of the TF
        
        :return: 
        """
        return len(self.term_freq_dict), sum(self.term_freq_dict.itervalues())

    def __repr__(self):
        total_num_of_terms = self.__len__()[1]
        return TERM_FORMAT % (self.term_str, TOTAL_TF_OPEN, total_num_of_terms, TOTAL_TF_CLOSE) + "%s%s" % (
            DICT_START_DELIMITER, self.docs_tfi_dict_as_str())

    def __lt__(self, other):
        return self.term_str < other.term_str

    def __eq__(self, other):
        return self.term_str == other.term_str

    def docs_tfi_dict_as_str(self):
        """"
        Represents the tfi dictionary as a string 
        """
        dict_to_str = ""
        for doc_id, tfi in self.term_freq_dict.iteritems():
            dict_to_str = "%s%s" %(dict_to_str, DICT_FORMAT % (doc_id, tfi,))
        return dict_to_str


if __name__ == "__main__":
    a = Term("tog")
    a["doc1"] = 5
    a["doc2"] = 2
    a["doc3"] = 9
    b = Term("cat")
    b["doc1"] = 55
    b["doc2"] = 3
    b["doc3"] = 1
    c = Term("lemo")
    c["doc1"] = 55
    c["doc2"] = 55
    c["doc3"] = 23

    term_obj_list = [c, a, b]

    term_obj_list.sort()

    for i in term_obj_list:
        print str(i) + " ******** " + repr(i)
        print "\n\n" + i.docs_tfi_dict_as_str()

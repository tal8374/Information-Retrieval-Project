from Configuration.config import IR_CONFIG


class StopWordsContainer(object):
    """ 
    Will be holding the set of stop words
    """

    def __init__(self, file_path):
        if file_path == "":
            return

        with open(file_path, 'r') as fd:
            self.__stop_words_set = frozenset([line.strip() for line in fd])

    def __contains__(self, word):
        """
        Returns if a given word is in the set -> Means if a word is a stop word or not

        :param word: A word to check if in the set
        :return: True if the word is in the set, False otherwise
        """
        return word in self.__stop_words_set


if __name__ == "__main__":
    stop_words_extractor = StopWordsContainer()
    print "a" in stop_words_extractor

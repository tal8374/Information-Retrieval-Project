SAFE_SYMBOL_LIST = frozenset([45, 37, 92, 47, 36, 58, 46])  # ["-","%","\\","/","$", ":","."]
TO_DELETE = frozenset(
    ['~', '`', '!', '@', '#', '^', '&', '*', '(', ')', '+', '=', '"', '*', '+', ";", "[", "]", "|", ",", "'", "?"])


class TextFilter(object):
    """
    Filter unnecessary symbols and problematic terms 
    """

    def __init__(self, text):
        self.text = text

    def delete_garbage(self):
        """
          Deletes unnecessary chars in text
          text# -> text,
          text   text-> text text,

          :rtype: string[]
          """
        self.text = self.text.replace("-", " ").replace(" / ", " ")
        self.text = TextFilter.delete_unwanted_chars(self.text)
        splitted_text = self.text.split()
        splitted_text = [expr for expr in splitted_text if TextFilter.is_ascii(expr)]
        return TextFilter.remove_word_suffixes(splitted_text)

    @staticmethod
    def is_ascii(word):
        try:
            word.decode('ascii')
        except UnicodeDecodeError:
            return False
        return True

    @staticmethod
    def delete_unwanted_chars(text):

        for sign in TO_DELETE:
            text = text.replace(sign, "")

        return text

    @staticmethod
    def remove_word_suffixes(words):
        """
          Removes suffix from word
          [cat.] -> [cat]

          :rtype: string[]
          """

        return [TextFilter.remove_special_suffix(word) for word in words]

    @staticmethod
    def has_special_suffix(word):
        """
          Checks if there is special suffix at the end of word
          cat. -> True
          cat -> False

          :rtype: boolean, True if has special suffix, False otherwise
          """

        return word[-1:] == '.' and word != "p.m." and word != 'a.m.'

    @staticmethod
    def remove_special_suffix(word):

        """
          Removes suffix from word
          cat. -> cat

          :rtype: string
          """

        if TextFilter.has_special_suffix(word):
            return word[: -1]
        return word


if __name__ == "__main__":
    d = TextFilter("abc Tel Aviv 3131")
    d.delete_garbage()
    print d.text

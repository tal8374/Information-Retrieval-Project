from datetime import datetime
import traceback
from Indexing.TextFilter import TextFilter

DATE_FORMATS = frozenset([
    ('%d %B %Y', '%d/%m/%Y'),
    ('%d %B %y', '%d/%m/%Y'),
    ('%B %d %Y', '%d/%m/%Y'),
    ('%d %B', '%d/%m'),
    ('%B %d', '%d/%m'),
    ('%B %Y', '%m/%Y'),
])

PERCENT_FORMAT = frozenset([
    ("%", " percent"),
    ("percentage", "percent")
])

DAYS_SUFFIX_FORMATS_DICT = {
    "1st": "1",
    "2nd": "2",
    "3rd": "3",
    "4th": "4"
}

MONTHS_FORMATS = frozenset([
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
    "jan",
    "feb",
    "mar",
    "apr",
    "jun",
    "jul",
    "aug",
    "sept",
    "sep",
    "oct",
    "nov",
    "dec"])

MONTHS_CONVERTER = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "Jul": "Jul",
    "Jun": "June",
    "Aug": "July",
    "Sept": "September",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December",
    "January": "January",
    "February": "February",
    "Feb": "February",
    "March": "March",
    "April": "April",
    "May": "May",
    "June": "June",
    "July": "July",
    "August": "August",
    "September": "September",
    "October": "October",
    "November": "November",
    "December": "December",
}

SPACE = " "
AM_PM_SET = frozenset(["p.m.", "a.m"])


class Parse(object):
    def __init__(self, text=[]):
        self._parsed_text = text
        self.__initialize_methods_list()

    def __initialize_methods_list(self):
        """
        Initilizes the list of parsing methods.

        :rtype: void
        """

        self.METHODS = [
            self.extract_date,
            self.extract_words,
            self.extract_percentage,
            self.extract_dollars,
            self.extract_number,
            self.extract_time,
        ]

    def parse_text(self, text):
        """
        Parses the text with the rules of each method in METHODS

        :rtype: void
        """
        filtered_text = TextFilter(text)
        text = filtered_text.delete_garbage()
        self._parsed_text = list(text)

        # Parse the text using the defined functions
        for index, value in enumerate(self.METHODS):
            value()

    def extract_time(self):
        """
         Parsed the text with time rules
         5:00 a.m -> 5:00
         5:00 p.m -> 17:00

         :rtype: void
         """

        parsed_text_list = []
        for index, word in enumerate(self._parsed_text):

            if word in AM_PM_SET:
                continue
            elif index + 1 < len(self._parsed_text) and "p.m." == self._parsed_text[index + 1]:
                parsed_time = self.parse_time(word)
                self.add_data_collection(parsed_text_list, [parsed_time])
            else:
                self.add_data_collection(parsed_text_list, [word])

        self._parsed_text = parsed_text_list

    def extract_dollars(self):
        """
        Parsed the text with dollar rules
        $50 -> 50 dollars

        :rtype: void
        """

        parsed_text_list = []
        for word in self._parsed_text:
            if "$" in word:
                self.add_data_collection(parsed_text_list, [word[1:] + " dollars"])
            else:
                self.add_data_collection(parsed_text_list, [word])

        self._parsed_text = parsed_text_list

    @staticmethod
    def parse_time(time_to_parse):
        """
        Parsed the time
        2 May 1993 -> 2/5/1993

        :rtype: parsed date, else None
        """
        if ":" not in time_to_parse:
            time_to_parse += ":00"
        try:
            time_data = int(time_to_parse[0: time_to_parse.find(":")])
            time_data += 12
            first_half = str(time_data)
            second_half = time_to_parse[time_to_parse.find(":") + 1:]
            return "%s:%s" % (first_half, second_half)
        except ValueError:
            pass

    def extract_number(self):
        """
        Parsed the text with number rules
        1.2323 -> 1.23

        :rtype: void
        """
        parsed_number_list = []
        for index, value in enumerate(self._parsed_text):
            if "." not in value and "/" not in value:
                self.add_data_collection(parsed_number_list, [value])
                continue
            try:
                self.add_data_collection(parsed_number_list,
                                         [str(self.__remove_floated_zeroes(round(float(value), 2)))])
            except (ValueError, ZeroDivisionError):
                self.add_data_collection(parsed_number_list, [value])
        self._parsed_text = parsed_number_list

    @staticmethod
    def __remove_floated_zeroes(number):
        """
        removes unnecessary zeroes from float number
        1.23400000 ->  1.234

        :type number: string
        :rtype: string
        """

        return '{0:g}'.format(number)

    def extract_percentage(self):
        """
        Each number which has the "%" or percentage in the end will be replaced with "percent"
        3% -> 3 percent, 3 percentage -> 3 percent

        :rtype: string
        """
        parsed_text_list = []
        str_isdigit = str.isdigit
        for word in self._parsed_text:
            if str_isdigit(word):
                self.add_data_collection(parsed_text_list, [word])
                continue
            for before_format, after_format in PERCENT_FORMAT:
                word = word.replace(before_format, after_format)
            self.add_data_collection(parsed_text_list, [word])
        self._parsed_text = parsed_text_list

    def extract_date(self):
        """
        Each date will be formatted with the following format : Day/Month/Year or Day/Month or Month/Year
        12th MAY 1991 -> 12/05/1991, May 12, 1990 -> 12/05/1991,
        14 MAY -> 14/05, June 4 -> 04/06, May 1994 -> 05/1994

        :rtype: string
        """

        parsed_text_list = []
        index = 0
        while index < len(self._parsed_text):
            if self._parsed_text[index].lower() not in MONTHS_FORMATS:
                self.add_data_collection(parsed_text_list, [self._parsed_text[index]])
                index += 1
                continue
            index = max(0, index - 1)
            parsed_text_list = parsed_text_list[: index]
            try:
                word1, word2, word3 = self._parsed_text[index], self.__get_next_word(self._parsed_text,
                                                                                     index), self.__get_next_word(
                    self._parsed_text,
                    index + 1)

                word1 = self.remove_day_suffix(word1)
                word2 = self.remove_day_suffix(word2)
                if not word1.isdigit() and not word2.isdigit():
                    self.add_data_collection(parsed_text_list, [word1, word2, word3])
                    index += 3
                    continue
                if word1.lower() in MONTHS_FORMATS:
                    word1 = MONTHS_CONVERTER[word1.title()]
                if word2.lower() in MONTHS_FORMATS:
                    word2 = MONTHS_CONVERTER[word2.title()]
                if Parse.__is_date([word1, word2, word3]):
                    parsed_date = Parse.__parse_date(SPACE.join([word1, word2, word3]))
                    self.add_data_collection(parsed_text_list, [parsed_date])
                elif Parse.__is_date([word1, word2]):
                    parsed_date = Parse.__parse_date(SPACE.join([word1, word2.title()]))
                    self.add_data_collection(parsed_text_list, [word3, parsed_date])
                elif Parse.__is_date([word2, word3]):
                    parsed_date = Parse.__parse_date(SPACE.join([word2.title(), word3]))
                    self.add_data_collection(parsed_text_list, [word1, parsed_date])
                else:
                    self.add_data_collection(parsed_text_list, [word1, word2, word3])
                index += 3
            except ValueError, e:
                print traceback.print_exc(e.message)
        self._parsed_text = parsed_text_list

    @staticmethod
    def add_data_collection(collection, words):
        """
        Inserting the words into collection.
        If one of the word is empty it will not be inserted

        :type collection: collection
        :type words: String[]
        :rtype: void
        """

        coll_app = collection.append
        for word in words:
            if word is not None and word != "":
                coll_app(word)

    @staticmethod
    def __parse_date(date):
        """
        Parses the date by formats
        1 May 1993 -> 01/05/1993

        :type date: string
        :rtype: parsed date, else empty string
        """
        datetime_strptime = datetime.strptime
        for date_format, return_date_format in DATE_FORMATS:
            try:
                d = datetime_strptime(date, date_format)
                return d.strftime(return_date_format)
            except ValueError:
                pass
        return ""

    @staticmethod
    def remove_day_suffix(day):
        """
        Removes day suffix
        1st -> 1

        :rtype: day without suffix
        """

        if day in DAYS_SUFFIX_FORMATS_DICT.keys():
            day = DAYS_SUFFIX_FORMATS_DICT[day]
        return day

    @staticmethod
    def __is_date(splitted_date):
        """
        Checks if a date string is a date
        abc May 1993 -> False,
        12 May -> True,
        May 1993 -> True
        12 May 1993 -> True

        :type splitted_date: string
        :rtype: Boolean
        """

        if "" in splitted_date:
            return False
        str_lower = str.lower
        str_isdigit = str.isdigit
        for part_of_date in splitted_date:
            is_a_month = str_lower(part_of_date) not in MONTHS_FORMATS
            is_number = str_isdigit(part_of_date)
            if not part_of_date or is_a_month and not is_number:
                return False
        return True

    def extract_words(self):
        """
        Extracts the words from the sentence with the following rules:
        If there is capital letter in word check:
            If the following word has capital letter letter
                parse words in the following way: Ax By -> ax, by, bx by
            Else
                parse word in the following way: Ax -> ax
        Else
            word -> word
        :rtype: string
        """

        parsed_text_list = []
        list_append = parsed_text_list.append
        words_with_capital_char = []
        for index, word in enumerate(self._parsed_text):
            contains_capitals = Parse.__is_contains_capital(word)
            if len(words_with_capital_char) > 1 and not contains_capitals:
                for capital_word in words_with_capital_char:
                    list_append(capital_word)
                if len(words_with_capital_char) > 1:
                    list_append(" ".join(words_with_capital_char))
                words_with_capital_char = []
            if '/' in word or '.' in word or ':' in word or word.isdigit():
                list_append(word)
            elif not contains_capitals:
                list_append(word)
            elif contains_capitals:
                words_with_capital_char.append(word.lower())
        if len(words_with_capital_char) > 0:
            for capital_word in words_with_capital_char:
                list_append(capital_word)
            if len(words_with_capital_char) > 1:
                list_append(" ".join(words_with_capital_char))
        self._parsed_text = parsed_text_list

    @staticmethod
    def extract_capital_words(text_list, index, last_capital_word_index):
        """
        Extracts the words from the first index til the index of the last capital word

        :rtype: String[]
        """

        return [text_list[i].lower() for i in xrange(index, last_capital_word_index + 1)] + \
               [" ".join(text_list[index: last_capital_word_index + 1]).lower()]

    @staticmethod
    def get_last_capital_word(text_list, index):
        while index < len(text_list) and Parse.__is_contains_capital(text_list[index]):
            index += 1
        return index - 1

    @staticmethod
    def __get_next_word(words, index):
        """
        Returns the next word in list of words. If next word doesn't exist returns ""

        :type words: string[]
        :type index: int
        :rtype: string
        """

        if index < len(words) - 1:
            return words[index + 1]
        return ""

    @staticmethod
    def __is_contains_capital(word):
        """
         Checks if a string contains capital letter. If does returns True, False otherwise.
         Happy -> true, hAppy -> True, happy -> False

         :type word: string
         :rtype: string
         """
        if word.isdigit():
            return False
        return word.lower() != word

    @property
    def parsed_text(self):
        """
          Return the parsed text

          :rtype: string
          """

        return self._parsed_text

    @parsed_text.setter
    def parsed_text(self, value):
        self._parsed_text = value


if __name__ == "__main__":
    parse = Parse()
    parse.parse_text("23 Feb 1991 Happy Day! 8 p.m.")
    print parse.parsed_text

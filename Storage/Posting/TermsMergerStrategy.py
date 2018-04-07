from Storage.Posting.IMergeStrategy import IMergeStrategy
from Storage.Term import DICT_START_DELIMITER, KEY_DELIMITER, TERM_FORMAT, TOTAL_TF_CLOSE, TOTAL_TF_OPEN


class TermsMergerStrategy(IMergeStrategy):
    """
    Merge strategy for terms string
    """

    @staticmethod
    def compare_inputs(input1, input2):
        """
         Checks for the name of the terms in each input.
         
         Assumes that the input values aren't None
        """

        input1_key = TermsMergerStrategy.get_key(input1)
        input2_key = TermsMergerStrategy.get_key(input2)

        if input1_key < input2_key:
            return -1
        if input1_key == input2_key:
            return 0
        if input1_key > input2_key:
            return 1

    @staticmethod
    def merge_lines(input1, input2):
        """
        The terms are identical so we merge the lines
        
        :param input1: A line which represents the first term 
        :param input2: A line which represents the second term
        :return: A line which represents the terms combined
        """

        # Get term name
        term_name = TermsMergerStrategy.get_key(input1)

        # Calculate the total term frequency
        total_tf = TermsMergerStrategy.get_sum(input1) + TermsMergerStrategy.get_sum(input2)

        # We build a new term string which represent the term line and not a Term object because it is faster
        return TERM_FORMAT % (term_name, TOTAL_TF_OPEN, total_tf, TOTAL_TF_CLOSE) + DICT_START_DELIMITER + \
               TermsMergerStrategy.get_dict(input1) + TermsMergerStrategy.get_dict(input2)

    @staticmethod
    def get_key(line):
        return line[0:line.index(KEY_DELIMITER)]

    @staticmethod
    def get_sum(line):
        return int(line[line.index(TOTAL_TF_OPEN) + 1: line.index(TOTAL_TF_CLOSE)])

    @staticmethod
    def get_dict(line):
        return line[line.index(DICT_START_DELIMITER) + 1:]


if __name__ == "__main__":
    terms_strategy = TermsMergerStrategy()

    first_line = "lemo; [133] |{doc2#55},{doc3#23},{doc1#55},"
    second_line = "lemo; [16] |{doc8#2},{doc12#9},{doc60#5},"

    if 0 == terms_strategy.compare_inputs(first_line, second_line):
        print terms_strategy.merge_lines(first_line, second_line)

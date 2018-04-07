import traceback

EMPTY_STRING = ''


class LineHandler(object):
    """
    Mapper between terms in line to the line numbers in the posting file
    """

    def __init__(self, file_path):
        self.path = file_path
        self.data = {}  # name -> number of line
        self.counter = 1

    def calculate_lines(self, ):
        """
        Calculates the line number for each term / doc

        :rtype: void
        """

        with open(self.path, 'r') as f:
            for line in f:
                if EMPTY_STRING != line:
                    self.update_data(line)

    def update_data(self, line):
        """
        Updating the dictionary with the new row

        :rtype: void
        """

        self.data[LineHandler.get_name(line)] = self.counter
        self.counter += 1

    @staticmethod
    def get_name(line):
        """
        Gets the name of the line

        :rtype: void
        """

        return line[:line.index(";")]

    def get_line(self, term):
        """
        Returns the number of line of the term

        :rtype: Number
        """

        try:
            return self.data[term]
        except Exception:
            print traceback.print_exc(Exception.message)
            return ""


if __name__ == "__main__":
    line_counter = LineHandler(r"C:\Users\Tal\PycharmProjects\informationretrieval\tests\Test_Files\file1.txt")
    line_counter.calculate_lines()
    print line_counter.data

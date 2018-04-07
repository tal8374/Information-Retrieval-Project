import unittest
from Indexing.Parse import Parse


class TestParse(unittest.TestCase):

    def test_extract_date(self):
        tests = [
                ("23 Feb 1991", "23/02/1991"),
                ("1st May 1991", "01/05/1991"),
                ("2nd May 1991", "02/05/1991"),
                ("3rd May 1991", "03/05/1991"),
                ("4th May 1991", "04/05/1991"),
                ("12 May 1991", "12/05/1991"),
                ("12 MAY 1991", "12/05/1991"),
                ("12 MAY 91", "12/05/1991"),
                ("12 May 91", "12/05/1991"),
                ("May 12 1991", "12/05/1991"),
                ("MAY 12 1991", "12/05/1991"),
                ("14 MAY", "14/05"),
                ("14 May", "14/05"),
                ("June 4", "04/06"),
                ("JUNE 4", "04/06"),
                ("May 1994", "05/1994"),
                ("MAY 1994", "05/1994"),
                ("Not a date", "Not a date")
                ]

        for test, result in tests:
            parser = Parse(test.split())
            parser.extract_date()
            self.assertEqual(result, " ".join(parser.parsed_text))

    def test_extract_number(self):
        tests = [
                ("1.232313", "1.23"),
                ("Not a number", "Not a number"),
                ]

        for test, result in tests:
            parser = Parse(test.split())
            parser.extract_number()
            self.assertEqual(result, " ".join(parser.parsed_text))

    def test_extract_percent(self):
        tests = [
                ("6%", "6 percent"),
                ("6.6%", "6.6 percent"),
                ("6 percent", "6 percent"),
                ("6.6 percent", "6.6 percent"),
                ("6 percentage", "6 percent"),
                ("6.6 percentage", "6.6 percent"),
                ("Not a percent", "Not a percent"),
                 ]

        for test, result in tests:
            parser = Parse(test.split())
            parser.extract_percentage()
            self.assertEqual(result, " ".join(parser.parsed_text))

    def test_extract_words(self):
        tests = [
                 ("Avigail", "avigail"),
                 ("NBA", "nba"),
                 ("Avigail Paradaise", "avigail paradaise avigail paradaise"),
                 ("Tal Ivanov Tel Aviv", "tal ivanov tel aviv tal ivanov tel aviv"),
                 ]

        for test, result in tests:
            parser = Parse(test.split())
            parser.extract_words()
            self.assertEqual(result, " ".join(parser.parsed_text))

    def test_extract_time(self):
        tests = [
                ("11:30 a.m.", "11:30"),
                ("11:30 p.m.", "23:30"),
                ("at 11:30 a.m.", "at 11:30"),
                ("at 11:30 p.m.", "at 23:30"),
                 ]

        for test, result in tests:
            parser = Parse(test.split())
            parser.extract_time()
            self.assertEqual(result, " ".join(parser.parsed_text))

    def test_extract_dollars(self):
        tests = [
                ("$20", "20 dollars"),
                ("20", "20"),
                 ]

        for test, result in tests:
            parser = Parse(test.split())
            parser.extract_dollars()
            self.assertEqual(result, " ".join(parser.parsed_text))

if __name__ == '__main__':
    unittest.main()

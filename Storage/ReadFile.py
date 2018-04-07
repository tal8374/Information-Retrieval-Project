from Configuration.config import IR_CONFIG
from Storage.CorpusDataExtractor import CorpusDataExtractor
import os.path


class ReadFile(object):
    """
    Reads a file from the corpus and yields the next list of needed info
    """

    def __init__(self, storage_folder):
        self.__storage_folder = storage_folder
        self.__base_tag = IR_CONFIG["read_file"]["base_tag"]

    def extract_from_tags(self):
        """
        Extracts the data from the tags
        :return: 
        """
        os_path_basename = os.path.basename
        for file_path in ReadFile.get_next_file(self.__storage_folder):
            with open(file_path, 'r') as fd:
                file_contents = fd.read()
            try:
                cde = CorpusDataExtractor(file_contents, self.__base_tag)
                while True:
                    yield [os_path_basename(file_path)] + next(cde)
            except StopIteration:
                continue

    @staticmethod
    def get_next_file(base_folder):
        """
        Recursively yields the next file in the folder
        :param base_folder: 
        :return: Next file in the folder
        """
        os_path_join = os.path.join
        for root, dirs, files in os.walk(base_folder):
            for name in files:
                yield os_path_join(root, name)


if __name__ == "__main__":
    print ReadFile.get_next_file(r"../../tests/Test_Files/")

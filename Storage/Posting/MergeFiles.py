import os
import traceback
from threading import Thread

from Storage.Posting.AMergeFile import AMergeFile
from Storage.Posting.TermsMergerStrategy import TermsMergerStrategy
from Storage.Posting.TextFileMerger import TextFileMerger
from Storage.ReadFile import ReadFile
from TextOperations.TextHelper import *

NEW_LINE = "\n"
EMPTY_STRING = ''


class MergeFiles(AMergeFile):
    """
    An utility class for merging the contents of files
    """

    def __init__(self, strategy, folder_path, out_file_name):
        super(MergeFiles, self).__init__(strategy, folder_path, out_file_name)

    def merge_sort(self):
        """
        Used to merge sort the files
        """

        num_of_files = self.get_number_of_files_in_folder()
        folder_gen = ReadFile.get_next_file(self.folder_path)

        if 0 == num_of_files:
            raise IOError

        if 1 == num_of_files:
            single_file = next(folder_gen)
            os.rename(single_file, os.path.join(self.folder_path, self.out_file_name))
            return

        if 2 < num_of_files:
            fd1 = next(folder_gen)
            fd2 = next(folder_gen)
            folder_gen = None

            # Give an unique name for the output file
            self.merge(fd1, fd2, os.path.join(self.folder_path, TextHelper.generate_file_name()))

            # Delete the files and finish
            Thread(name='merge_delete_files_greater', target=TextFileMerger.delete_files([fd1, fd2])).start()

            self.merge_sort()

        if 2 == num_of_files:
            fd1 = next(folder_gen)
            fd2 = next(folder_gen)
            self.merge(fd1, fd2, os.path.join(self.folder_path, self.out_file_name))

            # Delete the files and finish
            Thread(name='merge_delete_files', target=TextFileMerger.delete_files([fd1, fd2])).start()

            return

    def merge(self, in_file1_path, in_file2_path, out_file_path):
        """
        Merge two files into a new one.

        We are using only 3 lines each time - memory efficient!
        """
        fd1, fd2, fd_out = None, None, None

        try:
            # Get the file descriptors
            fd_out, fd1, fd2 = self.open_files(out_file_path, in_file1_path, in_file2_path)

            # Get the first two lines from the input files
            fd1_line = fd1.readline()[:-1]
            fd2_line = fd2.readline()[:-1]

            while EMPTY_STRING != fd1_line and EMPTY_STRING != fd2_line:
                compare_res = self.strategy.compare_inputs(fd1_line, fd2_line)

                if 0 == compare_res:
                    fd_out.write(self.merge_line(fd1_line, fd2_line) + NEW_LINE)
                    fd1_line = fd1.readline()[:-1]
                    fd2_line = fd2.readline()[:-1]
                elif -1 == compare_res:
                    fd_out.write(fd1_line + NEW_LINE)
                    fd1_line = fd1.readline()[:-1]
                elif 1 == compare_res:
                    fd_out.write(fd2_line + NEW_LINE)
                    fd2_line = fd2.readline()[:-1]

            # We got EOF for one of the files so we can write the rest of the second one
            if EMPTY_STRING == fd1_line and EMPTY_STRING == fd2_line:
                pass
            while EMPTY_STRING == fd1_line and EMPTY_STRING != fd2_line:
                fd_out.write(fd2_line + NEW_LINE)
                fd2_line = fd2.readline()[:-1]
            while EMPTY_STRING == fd2_line and EMPTY_STRING != fd1_line:
                fd_out.write(fd1_line + NEW_LINE)
                fd1_line = fd1.readline()[:-1]

        except Exception, e:
            print traceback.print_exc(e.message)
        finally:
            # Close the handles
            MergeFiles.close_files(fd1, fd2, fd_out)

    def merge_line(self, line1, line2):
        return self.strategy.merge_lines(line1, line2)


if __name__ == "__main__":
    a = MergeFiles(TermsMergerStrategy(), r"../../tests/Test_Files/", "term_posting_file")
    a.merge_sort()

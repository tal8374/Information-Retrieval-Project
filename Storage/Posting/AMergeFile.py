from abc import ABCMeta, abstractmethod
import os


class AMergeFile(object):
    __metaclass__ = ABCMeta

    def __init__(self, strategy, folder_path, out_file_name):
        self.strategy = strategy
        self.folder_path = folder_path
        self.out_file_name = out_file_name

    @abstractmethod
    def merge(self, *args):
        raise NotImplementedError()

    @abstractmethod
    def merge_line(self, line1, line2):
        raise NotImplementedError()

    @abstractmethod
    def merge_sort(self):
        raise NotImplementedError()

    def open_files(self, out_file, fd_1, fd_2):
        """
        
        :param out_file: 
        :param fd_1: 
        :param fd_2: 
        
        :return: List of open file descriptors 
        """
        return [open(out_file, 'w'), open(fd_1, 'r'), open(fd_2, 'r')]

    @staticmethod
    def close_files(*args):
        for fd in args:
            if fd:
                fd.close()

    def get_number_of_files_in_folder(self):
        return len(
            [name for name in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, name))])

import os
import traceback
from threading import Thread


class TextFileMerger(object):
    """
    Used to merge text files
    """

    @staticmethod
    def merge_text_files(folder_path, out_file_path):
        """
        Get the list of files in the folder and merge them to one file
        Deletes all the files except the output file
        
        
        :param folder_path: The base folder
        :param out_file_path: The path for the output file
        """
        file_paths = TextFileMerger.get_files_in_folder(folder_path)
        with open(out_file_path, 'w') as outfile:
            outfile_write = outfile.write
            for file_name in file_paths:
                with open(file_name, 'r') as infile:
                    for line in infile:
                        if "\n" != line:
                            outfile_write(line)
        Thread(name='delete_files', target=TextFileMerger.delete_files(file_paths)).start()

    @staticmethod
    def get_files_in_folder(base_folder):
        """
        Get list of files in folder
        
        :param base_folder: 
        :return: List of file paths
        """
        return [os.path.join(root, name) for root, dirs, files in os.walk(base_folder) for name in files]

    @staticmethod
    def delete_files(file_paths):
        """
        
        :return: 
        """
        for file_path in file_paths:
            try:
                os.remove(file_path)
            except Exception, e:
                print traceback.print_exc(e.message)


if __name__ == "__main__":
    print TextFileMerger.get_files_in_folder(r"D:\corpus_test")

# from __future__ import division

import Tkinter
import os
import shutil
import timeit
import tkFileDialog
import traceback
from tkFileDialog import askopenfilename

from Configuration.config import IR_CONFIG
from Model import Model
from Observer import Observer
from ViewModel import ViewModel


class GUI(Tkinter.Frame, Observer):
    def __init__(self, view_model_in, parent=None):
        Tkinter.Frame.__init__(self, parent)
        self.view_model = view_model_in
        self.parent = parent
        self.pack()
        self.stemmer_checkbox_val = Tkinter.IntVar()
        self.expanded_queries_checkbox_val = Tkinter.IntVar()
        self.summarizing_documents_checkbox_val = Tkinter.IntVar()
        self.to_stem = False
        self.path_for_corpus_and_stop_words = ""
        self.path_for_posting_and_dictionary = ""
        self.path_for_posting = ""

        self.start_time = 0
        self.document_number = 0
        self.cache_size = 0
        self.dictionary_size = 0

        self.chk = None
        self.cb_expanded_queries = None
        self.is_cache_shown = False
        self.is_dictionary_shown = False
        self.button_show_dictionary_and_cache = None
        self.button_save_dictionary_and_cache = None
        self.button_path_for_corpus_and_stop_words = None
        self.button_load_dictionary_and_cache = None
        self.button_path_for_posting = None
        self.button_show_cache = None
        self.reset_button = None
        self.button_browse_query_file = None
        self.init_check_box()
        self.init_buttons()
        # parent.bind('<Return>', (lambda event, v = vars_t: self.start(v)))

        self.index_info_label_var = Tkinter.StringVar()
        self.index_info_label = Tkinter.Label(root, textvariable=self.index_info_label_var, relief=Tkinter.RAISED)
        self.index_info_label.pack()
        self.data_format = "Building index info \n Run time - {} seconds \n Cache size - {}  \n Index size " \
                           "- {}  \n Number of documents - {}"
        self.index_info_label_var.set(self.data_format.format("no info", "no info", "no info", "no info"))

    def update(self, *args, **kwargs):
        """
        Updating that there was change

        :rtype: void
        """
        self.enable_buttons()

        self.show_building_index_info()

    def show_building_index_info(self):

        stop = timeit.default_timer()

        self.run_time = int(stop - self.start_time)
        self.path_for_posting_and_dictionary
        os.path.join(self.path_for_posting_and_dictionary, )
        self.cache_size = self.view_model.get_cache_size()
        self.dictionary_size = self.view_model.get_dictionary_size()
        self.document_number = self.view_model.get_doc_counter()
        self.index_info_label_var.set(
            self.data_format.format(str(self.run_time), str(self.cache_size) + " bytes",
                                    str(self.dictionary_size) + " bytes", str(self.document_number)))

    def init_check_box(self):
        """
        Initilizes the check box

        :rtype: void
        """

        self.chk = Tkinter.Checkbutton(self.parent, text="Do Stemming",
                                       variable=self.stemmer_checkbox_val, onvalue=1, offvalue=0)
        self.chk.pack()

        self.cb_expanded_queries = Tkinter.Checkbutton(self.parent, text="Do expanded query",
                                                       variable=self.expanded_queries_checkbox_val, onvalue=1,
                                                       offvalue=0)
        self.cb_expanded_queries.pack()

        self.cb_summarizing_documents = Tkinter.Checkbutton(self.parent, text="Do summarizing documents",
                                                            variable=self.summarizing_documents_checkbox_val, onvalue=1,
                                                            offvalue=0)
        self.cb_summarizing_documents.pack()

    def init_buttons(self):
        """
        Initilizes the buttons

        :rtype: void
        """

        self.init_path_for_posting_button()
        self.init_path_for_corpus_and_stop_words_button()
        self.init_load_dictionary_and_cache_button()
        self.init_start_button()
        self.init_reset_button()
        self.init_show_cache_button()
        self.init_show_dictionary_and_cache_button()
        self.init_save_dictionary_and_cache_button()
        self.init_browse_query_file_button()

    def disable_buttons(self):
        """
        Disables the buttons

        :rtype: void
        """
        self.reset_button.config(state=Tkinter.DISABLED)
        self.button_show_cache.config(state=Tkinter.DISABLED)
        self.button_path_for_posting.config(state=Tkinter.DISABLED)
        self.button_load_dictionary_and_cache.config(state=Tkinter.DISABLED)
        self.button_path_for_corpus_and_stop_words.config(state=Tkinter.DISABLED)
        self.button_save_dictionary_and_cache.config(state=Tkinter.DISABLED)
        self.button_show_dictionary_and_cache.config(state=Tkinter.DISABLED)
        self.button_start.config(state=Tkinter.DISABLED)
        self.chk.config(state=Tkinter.DISABLED)

    def enable_buttons(self):
        """
        Enables the buttons

        :rtype: void
        """

        self.reset_button.config(state=Tkinter.NORMAL)
        self.button_show_cache.config(state=Tkinter.NORMAL)
        self.button_path_for_posting.config(state=Tkinter.NORMAL)
        self.button_load_dictionary_and_cache.config(state=Tkinter.NORMAL)
        self.button_path_for_corpus_and_stop_words.config(state=Tkinter.NORMAL)
        self.button_save_dictionary_and_cache.config(state=Tkinter.NORMAL)
        self.button_show_dictionary_and_cache.config(state=Tkinter.NORMAL)
        self.button_start.config(state=Tkinter.NORMAL)
        self.chk.config(state=Tkinter.NORMAL)

    def get_path_corpus_and_stop_words(self):
        """
        Recives the path of corpus and stop words from the user

        :rtype: void
        """

        self.path_for_corpus_and_stop_words = tkFileDialog.askdirectory(parent=self.parent,
                                                                        initialdir="/",
                                                                        title='Pick a directory')

        IR_CONFIG["storage"]["corpus_folder"] = os.path.join(self.path_for_corpus_and_stop_words, "corpus").replace(
            "\\", "/")
        IR_CONFIG["storage"]["stop_wards_path"] = os.path.join(self.path_for_corpus_and_stop_words,
                                                               "stop_words.txt").replace("\\", "/")

    def init_path_for_corpus_and_stop_words_button(self):
        """
       Create the button for browse corpus and stop word

       :rtype: void
       """

        self.button_path_for_corpus_and_stop_words = Tkinter.Button(root, text="Browse path posting directory",
                                                                    command=(
                                                                        lambda v=vars_t:
                                                                        self.get_path_posting()))
        self.button_path_for_corpus_and_stop_words.pack()

    def get_path_posting(self):
        """
       Recieves the path for corpus and stop words

       :rtype: void
       """
        self.path_for_posting = tkFileDialog.askdirectory(parent=self.parent,
                                                          initialdir="/",
                                                          title='Pick a directory')

    def init_path_for_posting_button(self):
        """
       Create the button for cache and dictionary browser

       :rtype: void
       """

        self.button_path_for_posting = Tkinter.Button(root,
                                                      text="Browse path for corpus and stop words directory",
                                                      command=(
                                                          lambda
                                                              v=vars_t: self.get_path_corpus_and_stop_words()))
        self.button_path_for_posting.pack()

    def init_browse_query_file_button(self):
        self.button_browse_query_file = Tkinter.Button(root,
                                                       text="Browse path for file with queries",
                                                       command=(
                                                           lambda
                                                               v=vars_t: self.choose_file()))
        self.button_browse_query_file.pack()

    def choose_file(self):
        filename = askopenfilename()
        print(filename)

    def init_start_button(self):
        """
       Create the button for start button

       :rtype: void
       """

        try:
            self.button_start = Tkinter.Button(root, fg="dark green", text='Start',
                                               command=(lambda v=vars_t: self.start(v)))
            self.button_start.pack()
        except Exception:
            print traceback.print_exc(Exception.message)

    def init_reset_button(self):
        """
       Create the button for reset

       :rtype: void
       """

        self.reset_button = Tkinter.Button(root, fg="red", text='Reset',
                                           command=(lambda v=vars_t: self.reset(v)))
        self.reset_button.pack()

    def init_show_cache_button(self):
        """
       Create the button for show cache

       :rtype: void
       """

        self.button_show_cache = Tkinter.Button(self.parent, text='Show Cache',
                                                command=(lambda v=vars_t: self.show_cache()))
        self.button_show_cache.pack()

    def init_show_dictionary_and_cache_button(self):
        """
       Create the button for showing dictionary and cache

       :rtype: void
       """

        self.button_show_dictionary_and_cache = Tkinter.Button(root, text='Show Dictionary',
                                                               command=(lambda v=vars_t: self.show_dictionary()))
        self.button_show_dictionary_and_cache.pack()

    def init_save_dictionary_and_cache_button(self):
        """
       Create the button for saving dictionary and cache

       :rtype: void
       """

        self.button_save_dictionary_and_cache = Tkinter.Button(root, text='Save Dictionary and cache',
                                                               command=(
                                                                   lambda v=vars_t: self.save_dictionary_and_cache()))
        self.button_save_dictionary_and_cache.pack()

    def init_load_dictionary_and_cache_button(self):
        """
       Create the button for loading dictionary and cache

       :rtype: void
       """

        self.button_load_dictionary_and_cache = Tkinter.Button(root, text='Load dictionary and cache folder path',
                                                               command=(
                                                                   lambda
                                                                       v=vars_t: self.get_path_cache_and_dictionary(v)))
        self.button_load_dictionary_and_cache.pack()

    def get_path_cache_and_dictionary(self, variables):

        data = []
        for variable in variables:
            data.append(variable.get())

        self.path_for_corpus_and_stop_words = data[0] if data[0] != "" else self.path_for_corpus_and_stop_words
        self.path_for_posting = data[1] if data[1] != "" else self.path_for_posting

        if 1 == self.stemmer_checkbox_val.get():
            self.to_stem = True
        elif 0 == self.stemmer_checkbox_val.get():
            self.to_stem = False

        self.path_for_posting_and_dictionary = tkFileDialog.askdirectory(parent=self.parent,
                                                                         initialdir="/",
                                                                         title='Pick a directory')

        self.view_model.load_dictionary_and_cache(self.path_for_corpus_and_stop_words,
                                                  self.path_for_corpus_and_stop_words, self.to_stem,
                                                  self.path_for_posting_and_dictionary)

    def start(self, variables):
        """
       Starts the program

       :rtype: void
       """

        # D:\Data_Test

        print "started"
        #
        # main_dictionary = self.view_model.get_dictionary()
        # doc_posting_folder = os.path.join(self.path_for_posting_and_dictionary,
        #                                        IR_CONFIG["storage"]["doc_posting_folder"])
        # stem_doc_posting_folder = os.path.join(self.path_for_posting_and_dictionary,
        #                                        IR_CONFIG["storage"]["stem_doc_posting_folder"])
        # if self.to_stem:
        #     doc_posting_file_target = os.path.join(stem_doc_posting_folder,
        #                                                 IR_CONFIG["storage"]["stem_doc_posting_file_name"])
        #
        # else:
        #     doc_posting_file_target = os.path.join(doc_posting_folder,
        #                                                 IR_CONFIG["storage"]["doc_posting_file_name"])
        # main_dictionary.initialize_document_dictionary(doc_posting_file_target)
        #
        # if 1 == self.stemmer_checkbox_val.get():
        #     self.to_stem = True
        # elif 0 == self.stemmer_checkbox_val.get():
        #     self.to_stem = False
        #
        # data = []
        # for variable in variables:
        #     data.append(variable.get())
        #
        # self.view_model.get_relevant_documents(data[1], [data[2]], self.to_stem, main_dictionary, doc_posting_file_target)


        self.disable_buttons()

        # self.delete_folder_content(IR_CONFIG["storage"]["posting_folder"].replace("\\", "/"))
        self.delete_folder_content(variables)

        # tkMessageBox.showinfo("Info Message", "The program has started to run")
        data = []
        for variable in variables:
            data.append(variable.get())

        self.path_for_corpus_and_stop_words = data[0] if data[0] != "" else self.path_for_corpus_and_stop_words
        self.path_for_posting = data[1] if data[1] != "" else self.path_for_posting

        if 1 == self.stemmer_checkbox_val.get():
            self.to_stem = True
        elif 0 == self.stemmer_checkbox_val.get():
            self.to_stem = False

        GUI.make_folders_if_not_exist(self.path_for_posting,
                                      [IR_CONFIG["storage"]["term_posting_folder"],
                                       IR_CONFIG["storage"]["doc_posting_folder"],
                                       IR_CONFIG["storage"]["stem_doc_posting_folder"],
                                       IR_CONFIG["storage"]["stem_term_posting_folder"], ])

        self.start_time = timeit.default_timer()

        corpus_directory_path = os.path.join(self.path_for_corpus_and_stop_words,
                                             IR_CONFIG["storage"]["corpus_folder_name"])
        stop_words_directory_path = os.path.join(self.path_for_corpus_and_stop_words,
                                                 IR_CONFIG["storage"]["stop_wards_filename"])

        self.view_model.build_index(corpus_directory_path, stop_words_directory_path, self.to_stem,
                                    os.path.join(self.path_for_posting, self.path_for_posting_and_dictionary))

    @staticmethod
    def make_folders_if_not_exist(base_folder, folder_list):
        """
        Makes folder if they are not exist

         :rtype: void
         """

        for file_name in folder_list:
            f_path = os.path.join(base_folder, file_name)
            if not os.path.exists(f_path):
                os.makedirs(f_path)

    def reset(self, variables):
        """
        Deletes the content of the folders

         :rtype: void
         """
        # self.delete_folder_content(variables)

        # TODO: delete the result files
        # TODO: show relevent data

        self.index_info_label_var.set(self.data_format.format("No info", "No info", "No info", "No info"))

    def delete_folder_content(self, variables):
        """
        Deletes the content of the folders

         :rtype: void
         """

        data = []
        for variable in variables:
            data.append(variable.get())

        self.path_for_posting = data[1] if data[1] != "" else self.path_for_posting

        to_delete = [IR_CONFIG["storage"]["doc_posting_folder"], IR_CONFIG["storage"]["stem_doc_posting_folder"],
                     IR_CONFIG["storage"]["term_posting_folder"], IR_CONFIG["storage"]["stem_term_posting_folder"],
                     IR_CONFIG["storage"]["dictionary_file_name"], IR_CONFIG["storage"]["dictionary_file_name_stem"],
                     IR_CONFIG["storage"]["cache_file_name"], IR_CONFIG["storage"]["cache_file_name_stem"]]

        if os.path.exists(self.path_for_posting):
            for the_file in to_delete:
                file_path = os.path.join(self.path_for_posting, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except OSError:
                    pass

    def show_cache(self):
        """
        Shows the cache

         :rtype: void
         """

        if self.is_cache_shown:
            return
        self.is_cache_shown = True
        scrollbar = Tkinter.Scrollbar(self.parent)
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        w = Tkinter.Label(self.parent, text="Cache Data")
        w.pack()
        tk_listbox = Tkinter.Listbox(self.parent, yscrollcommand=scrollbar.set)
        tk_listbox.config(width=0)

        cache = self.view_model.get_cache()

        cache_format = "term - {}, pointer - {}"

        for term in sorted(cache.data_dict):
            tk_listbox.insert(Tkinter.END, cache_format.format(term, cache.data_dict[term]))
        tk_listbox.pack(fill=Tkinter.BOTH)
        scrollbar.config(command=tk_listbox.yview)

    def show_dictionary(self):
        """
        Shows the dictionary

         :rtype: void
         """

        if self.is_dictionary_shown:
            return
        self.is_dictionary_shown = True
        scrollbar = Tkinter.Scrollbar(self.parent)
        scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        w = Tkinter.Label(self.parent, text="Dictionary Data")
        w.pack()
        tk_listbox = Tkinter.Listbox(self.parent, yscrollcommand=scrollbar.set)
        tk_listbox.config(width=0)

        dictionary = self.view_model.get_dictionary()
        dictionary_format = "term - {}, df - {}, tf - {}, pointer - {}"

        for term in sorted(dictionary.data_dict):
            tk_listbox.insert(Tkinter.END, dictionary_format.format(term, dictionary.data_dict[term][0],
                                                                    dictionary.data_dict[term][2],
                                                                    dictionary.data_dict[term][1]))

        tk_listbox.pack(fill=Tkinter.BOTH)
        scrollbar.config(command=tk_listbox.yview)

    def save_dictionary_and_cache(self):
        """
        Saves the dictionary and cache

         :rtype: void
         """

        dictionary_cache_directory = tkFileDialog.askdirectory(parent=self.parent,
                                                               initialdir="/",
                                                               title='Pick a directory')

        self.view_model.save_dictionary_and_cache(dictionary_cache_directory)

    # def load_dictionary_and_cache(self):
    #     """
    #     Loads the dictionary and cache
    #
    #      :rtype: void
    #      """
    #
    #     self.view_model.load_dictionary_and_cache(self.path_for_corpus_and_stop_words,
    #                                               self.path_for_corpus_and_stop_words, self.to_stem,
    #                                               self.path_for_posting_and_dictionary)


fields = IR_CONFIG["gui"]["label_docs_and_sw"], IR_CONFIG["gui"]["label_path_to_save_files"], "Single query"


def make_form(root_frame, fields_input):
    form = Tkinter.Frame(root_frame)
    left = Tkinter.Frame(form)
    rite = Tkinter.Frame(form)
    form.pack(fill=Tkinter.X)
    left.pack(side=Tkinter.LEFT)
    rite.pack(side=Tkinter.RIGHT, expand=Tkinter.YES, fill=Tkinter.X)

    variables = []
    for field in fields_input:
        lab = Tkinter.Label(left, width=45, text=field, bg=IR_CONFIG["gui"][
            "special_colors"]["background"])
        ent = Tkinter.Entry(rite)
        lab.pack(side=Tkinter.TOP)
        ent.pack(side=Tkinter.TOP, fill=Tkinter.X)
        var = Tkinter.StringVar()
        ent.config(textvariable=var)
        var.set('')
        variables.append(var)
    return variables


if __name__ == '__main__':
    model = Model()
    view_model = ViewModel(model)
    model.register(view_model)
    root = Tkinter.Tk()
    vars_t = make_form(root, fields)
    view = GUI(view_model, root)
    view.pack(side=Tkinter.RIGHT)
    view_model.register(view)
    root["bg"] = IR_CONFIG["gui"]["special_colors"]["background"]
    root.wm_title(IR_CONFIG["gui"]["title"])
    root.wm_iconbitmap(IR_CONFIG["gui"]["icon"])
    root.mainloop()

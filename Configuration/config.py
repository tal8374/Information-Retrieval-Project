from nltk.stem import PorterStemmer
from nltk.stem.snowball import EnglishStemmer
from nltk.stem import LancasterStemmer
import tempfile

IR_CONFIG = {
    "gui": {
        ### Main Window Prop ###
        "title": "Information Retrieval",
        "window_width": "600",
        "window_height": "400",
        "use_stemmer": True,
        "icon": "paper.ico",

        ### Labels and Text ###
        "about": "Created by: Yagil Ovadia & Tal Ivanov\nCourse: Information Retrieval\nYear: 2017",
        "stemming": "Stem Data",
        "label_docs_and_sw": "Path for corpus and stop words",
        "label_path_to_save_files": "Path for posting and dictionary",
        "reset_warning": "You are about to reset the data!",

        # Buttons
        "start": "Start",
        "reset": "Reset",
        "show_dict": "Show Dictionary",
        "show_cache": "Show Cache",
        "load_dict_and_cache": "Load Dictionary & Cache",
        "save_dict_and_cache": "Save Dictionary & Cache",
        "browse": "Browse",

        ### Additional ###
        "special_colors": {
            "background": "#BEE9F7",
            "background_but": "#BEBFF7",
        },
    },
    "storage": {
        "corpus_folder_name": "corpus",
        "stop_wards_filename": "stop_words.txt",

        "cache_file_name": "cache_data",
        "dictionary_file_name": "dictionary_data",

        "cache_file_name_stem": "cache_data_stem",
        "dictionary_file_name_stem": "dictionary_data_stem",

        "term_posting_folder": "TermPosting",
        "doc_posting_folder": "DocPosting",
        "stem_term_posting_folder": "TermPostingWithStem",
        "stem_doc_posting_folder": "DocPostingWithStem",

        "term_posting_file_name": "term_posting_file",
        "stem_term_posting_file_name": "stem_term_posting_file",
        "doc_posting_file_name": "doc_posting_file",
        "stem_doc_posting_file_name": "stem_doc_posting_file",

    },
    "read_file": {
        "base_tag": "DOC",
        "conditional_tag": "TEXT",
        "id_tag": "DOCNO",
        "headline_tag": "HEADLINE",
        "date_tag": "DATE",
        "date1_tag": "DATE1",
        "header_tag": "HEADER",
    },
    "corpus_handler": {
        "common_tags": ["data"],
        "FB": ["HEADER", "DATE1"],
        "FT": ["HEADLINE", "DATE"],
        "LA": ["HEADLINE", "DATE"],
    },
    "Stemmers": {
        "Porter": {"class": PorterStemmer, "function_list": []},  # Never use 'None' here for the function list
        "EnglishStemmer": {"class": EnglishStemmer, "function_list": []},
        "Lancaster": {"class": LancasterStemmer, "function_list": []},
    },
    "posting": {
        "temp_folder": tempfile.gettempdir(),
        "terms": {

        },
    },

    "indexer": {
        "doc_to_process": 30000
    }
}

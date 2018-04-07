import traceback
from Configuration.config import IR_CONFIG
from Stemming.IStemmer import IStemmer


class Stemmer(IStemmer):
    """
    Stemming class which implements a stemmer interface.
    Use this class to stem list of expressions
    
    If we would like the stemmer not to stem some kind of expression we can simply handle that
    with conditional functions
    """

    def __init__(self, in_stemmer = "Porter"):
        # type: (object) -> object
        self.__stemmer_as_dict = IR_CONFIG["Stemmers"][in_stemmer]
        self.__stemmer_obj = self.__stemmer_as_dict["class"]()
        self.__stemmer_dict = {}

        if 0 == len(self.__stemmer_as_dict["function_list"]):
            self.__stem_func = self.__stem_expression_list_without_condition
        else:
            self.__stem_func = self.__stem_expression_list_with_conditiondocumt
            self.__bool_func_list = self.__stemmer_as_dict["function_list"]

    def __test_conditions(self, expression):
        """
        For every function in the boolean function list check if the expression satisfies the condition.
        
        :param expression: A string representing the an expression to stem
        :return: True if the expression satisfies one of the function list
        """
        for bool_func in self.__bool_func_list():
            if bool_func(expression):
                return True
        return False

    def stem_expression_list(self, expr_list):
        """
        Stem each expression from the expression list given
        
        :param expr_list: list of expressions before stemming 
        :return: List of stemmed expressions using the stemmer configured in class
        """
        return self.__stem_func(expr_list)

    def __stem_expression_list_with_condition(self, expr_list):
        """
        Stem each expression from the expression list given

        :param expr_list: list of expressions before stemming 
        :return: List of stemmed expressions using the stemmer configured in class
        """
        stemmed_expressions = []

        for expression in expr_list:
            if self.__test_conditions(expression):
                stemmed_expressions.append(expression)
            else:
                stemmed_expressions.append(self.__stemmer_obj.stem(expression))
        return stemmed_expressions

    def __stem_expression_list_without_condition(self, expr_list):
        """
        Stem each expression from the expression list given

        :param expr_list: list of expressions before stemming 
        :return: List of stemmed expressions using the stemmer configured in class
        """
        stemmed_list = []
        list_append = stemmed_list.append
        stem_func = self.__stemmer_obj.stem
        for expression in expr_list:
            if expression in self.__stemmer_dict:
                list_append(self.__stemmer_dict[expression])
            else:
                try:
                    stemmed_expr = stem_func(expression)
                except UnicodeDecodeError, e:
                        print traceback.print_exc(e.message)
                self.__stemmer_dict[expression] = stemmed_expr
                list_append(stemmed_expr)
        return stemmed_list

    def reset_dictionary(self):
        self.__stemmer_dict = {}


if __name__ == "__main__":

    a = "D:\corpus_test\FB396237\FB396237"  # problematic file
    # a = "C:\Users\ISE\Desktop\IF\Data\corpus\FB396001\FB396001"
    with open(a, 'r') as fd:
        b = fd.read()
    b = b.split()
    stemmer = Stemmer()
    stemmed_ls = stemmer.stem_expression_list(b)
    # for i in stemmed_ls:
    #     print i #chardet.detect(i)['encoding']
    # print chardet.detect(expression)['encoding']
    #
    #
    # for i in b:
    #     if chardet.detect(i)['encoding'] != 'ascii':
    #         print i, chardet.detect(i)['encoding']
    # print stemmer.stem_expression_list("promise: an edict was published concerning organizing the return Main POLITICIANS,  PARTY PREFERENCES".split())

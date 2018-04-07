class ProjectStat(object):
    def __init__(self):
        pass
    def get_number_of_terms_with_no_stemming(self, in_file):
        pass
    def get_number_of_terms_with_stemming(self, in_file):
        pass
    def get_number_of_terms_which_are_numbers(self, in_file):
        number_counter = 0
        with open(in_file, 'r') as fd:
            for line in fd:
                try:
                    word = word[:line.index(';')]
                    if word.isdigit():
                        number_counter += 1
                except Exception:
                    pass
        return number_counter
    def get_most_frequent_terms(self, n, in_file):
        pass
    def get_least_frequent_terms(self, n, in_file):
        pass
    def get_posting_size(self, base_folder):
        pass



if __name__ == "__main__":
    project_stat = ProjectStat()

    # Q1
    print project_stat.get_number_of_terms_with_no_stemming(raw_input("> No stemming path"))

    # Q2
    print project_stat.get_number_of_terms_with_stemming(raw_input("> With stemming path"))

    # Q3
    print project_stat.get_number_of_terms_which_are_numbers(raw_input("> No stemming path"))

    # Q4
    print project_stat.get_most_frequent_terms(10, raw_input("> No stemming path"))

    # Q5
    print project_stat.get_least_frequent_terms(10, raw_input("> No stemming path"))

    # Q6
    project_stat.get_posting_size()

    # Q7

    # Q8

    # Q9

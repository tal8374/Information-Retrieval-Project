from abc import ABCMeta, abstractmethod


class IMergeStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def compare_inputs(self, input1, input2):
        """
        Condition if merge is needed for two inputs
        
        :param input1: First input
        :param input2: Second input
        :return: 0 if True, 1 if input2 greater than input1, -1 otherwise
        """
        raise NotImplementedError()

    @abstractmethod
    def get_key(self, input_stream):
        """
        
        :param input_stream: 
        :return: 
        """
        NotImplementedError()

    @abstractmethod
    def get_sum(self, input_stream):
        """
        
        :param input_stream: 
        :return: 
        """
        NotImplementedError()

    @abstractmethod
    def get_dict(self, input_stream):
        """
        
        :param input_stream: 
        :return: 
        """
        NotImplementedError()

    @abstractmethod
    def merge_lines(self, input_stream1, input_stream2):
        NotImplementedError()

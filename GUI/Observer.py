from abc import ABCMeta, abstractmethod


class Observer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        Updating that there was change

        :rtype: void
        """

        pass

# example -
#
# http://www.giantflyingsaucer.com/blog/?p=5117
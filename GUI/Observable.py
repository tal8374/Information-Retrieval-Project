class Observable(object):
    def __init__(self):
        self.observers = []

    def register(self, observer):
        """
        Adding to the observers list the new observer

        :rtype: void
        """

        if observer not in self.observers:
            self.observers.append(observer)

    def unregister(self, observer):
        """
        Removing from the observers list the observer

        :rtype: void
        """

        if observer in self.observers:
            self.observers.remove(observer)

    def unregister_all(self):
        """
        Removing all the observers from the observers list

        :rtype: void
        """

        if self.observers:
            del self.observers[:]

    def update_observers(self, *args, **kwargs):
        """
        Updating the observers with the change

        :rtype: void
        """

        for observer in self.observers:
            observer.update(*args, **kwargs)

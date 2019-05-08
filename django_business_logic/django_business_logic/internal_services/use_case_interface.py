import abc


class UseCaseInterface(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute(self):
        pass

    @abc.abstractmethod
    def is_valid(self):
        pass


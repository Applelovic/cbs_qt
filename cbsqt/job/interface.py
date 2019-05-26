from abc import ABCMeta, abstractmethod


class AbstractJob(metaclass=ABCMeta):

    @abstractmethod
    def run_singal(self):
        raise NotImplementedError

    @abstractmethod
    def set_time(self, time_obj):
        raise NotImplementedError

    @abstractmethod
    def run_snapshot(self):
        raise NotImplementedError

    @abstractmethod
    def termination(self):
        raise NotImplementedError

import abc
from h_params import h_params

class Score(metaclass=abc.ABCMeta):
    h_params = 'abc'


    @abc.abstractmethod
    def decisionMaking(self):
        pass

    @abc.abstractmethod
    def getCcoachingTip(self):
        pass

    def getSubScores(self):
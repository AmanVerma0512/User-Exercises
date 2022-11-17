import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


class Score(ABC):
    @abc.abstractmethod
    def coachingTip():
        pass

    @abc.abstractmethod
    def userProfileScore(history, current_score):  # given previous score, how to update
        pass

    @abc.abstractmethod
    def subScores():
        pass

    @abc.abstractmethod
    def score():  # aggregation, reassign from Policy.aggregation variants
        pass

    @abc.abstractmethod
    def compute():  # core computation of score
        pass

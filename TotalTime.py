import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


class TotalTime(Score):
    scoreType = "total time"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev  # getPrevScore()
        self.compute()
        self.coachingTip()

    def compute(self):
        start, end = getStartEnd(self.y)
        self.currScore = 0
        for i in range(start, end + 1):
            if self.y[i] > 0.1 * max(self.y):
                self.currScore += 1
        return self.currScore

    def coachingTip(self):
        self.coachingTipRes = coachingTipTemplate(TotalTime.scoreType, self.currScore)
        return self.coachingTipRes

    def userProfileScore(self):
        return userProfileTemplate(self.currScore, self.prevScore)

    def score(self):
        self.compute()
        return self.currScore

    def subScores(self):
        res = {}
        res[TotalTime.scoreType] = {}
        res[TotalTime.scoreType]["score"] = self.currScore
        res[TotalTime.scoreType]["coachingTip"] = self.coachingTipRes
        return res


class TotalTimeFactory():
    def configuredObject(y, configs):
        totalTime = TotalTime(y, configs)
        return totalTime


TotalTimeFactory.configuredObject(y, h_params1["stamina"]["total time"]).subScores()
TotalTime.scoreType
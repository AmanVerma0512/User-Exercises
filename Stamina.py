import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


# aggregated stamina class
class Stamina(Score):
    scoreType = "stamina"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev
        self.subScoresObjects = [
            AreaStaminaFactory.configuredObject(y, configs[AreaStamina.scoreType]),
            #         RingStaminaFactory.configuredObject(y,configs[RingStamina.scoreType])
            TotalTimeFactory.configuredObject(y, configs[TotalTime.scoreType]),
        ]
        self.compute()
        self.coachingTip()

    def compute(self):
        self.currScore = 0
        totalWeights = 0
        for subScore in self.subScoresObjects:
            w = self.config['w_' + subScore.scoreType]
            self.currScore += float(w) * subScore.score()
            totalWeights += w
        self.currScore /= totalWeights
        return self.currScore

    def coachingTip(self):
        self.coachingTipRes = ""
        for subScore in self.subScoresObjects:
            self.coachingTipRes += subScore.coachingTip() + ", "
        self.coachingTipRes = self.coachingTipRes[:-2]
        return self.coachingTipRes

    def userProfileScore(self):
        return userProfileTemplate(self.currScore, self.prevScore)

    def score(self):
        return self.currScore

    def subScores(self):
        resList = [subScore.subScores() for subScore in self.subScoresObjects]
        subScoreDict = dict(ChainMap(*resList))
        res = {}
        res["subScores"] = subScoreDict
        res["score"] = self.currScore
        res["coachingTip"] = self.coachingTipRes
        res = {
            Stamina.scoreType: res
        }
        return res


class StaminaFactory():
    def configuredObject(y,configs):
        if configs["peaks"]["scipyPeaks"]:
            global peaks
            currPeaks=peaks
            peaks = scipyPeaks
        stamina=Stamina(y,configs)
        if configs["peaks"]["scipyPeaks"]:
            peaks=currPeaks
        return stamina


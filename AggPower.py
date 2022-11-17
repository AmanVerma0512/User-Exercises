import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


class AggPowerScore(Score):
    scoreType = "agg power"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev
        self.subScoresObjects = [
            PowerFactory.configuredObject(y, configs[Power.scoreType]),
            ExplosivenessFactory.configuredObject(y, configs[Explosiveness.scoreType])
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
        #         binary string to choose
        resList = [subScore.subScores() for subScore in self.subScoresObjects]
        subScoreDict = dict(ChainMap(*resList))
        res = {}
        res["subScores"] = subScoreDict
        res["score"] = self.currScore
        res["coachingTip"] = self.coachingTipRes
        res = {
            AggPowerScore.scoreType: res
        }
        return res


class AggPowerScoreFactory():
    def configuredObject(y, configs):
        powerScore = AggPowerScore(y, configs)
        return powerScore
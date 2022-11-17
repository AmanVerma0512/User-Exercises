import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


class AggFormScore(Score):
    scoreType = "formscore"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev
        self.subScoresObjects = [
            JitterFactory.configuredObject(y, configs[Jitter.scoreType]),
            TempoFactory.configuredObject(y, configs[Tempo.scoreType]),
            SuddenReleaseFactory.configuredObject(y, configs[SuddenRelease.scoreType])
        ]
        self.compute()
        self.coachingTip()

    def compute(self):
        self.currScore = 0
        totalWeight = 0
        for subScore in self.subScoresObjects:
            w = self.config['w_' + subScore.scoreType]
            self.currScore += float(w) * subScore.score()
            totalWeight += w
        self.currScore /= totalWeight
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
            AggFormScore.scoreType: res
        }
        return res

class FormScoreFactory():
    def configuredObject(y,configs):
        if "scipyPeaks" in configs:
            global peaks
            currPeaks=peaks
            peaks = scipyPeaks
            formScore=AggFormScore(y,configs)
            peaks=currPeaks
            return formScore
        else:
            return AggFormScore(y,configs)
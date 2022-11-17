import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


class AreaStamina(Score):
    scoreType = "area stamina"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev  # getPrevScore()
        self.compute()
        self.coachingTip()

    def compute(self):
        referenceFactor = self.config["referenceFactor"]
        ref = int(max(self.y) * referenceFactor)
        start, end = getStartEnd(self.y)
        total_power = sum(self.y[start:end])
        ideal_power = ref * (end - start)
        self.currScore = total_power / ideal_power
        self.currScore *= 100
        self.currScore = clip100(self.currScore)
        return self.currScore

    def coachingTip(self):
        self.coachingTipRes = coachingTipTemplate(AreaStamina.scoreType, self.currScore)
        return self.coachingTipRes

    def userProfileScore(self):
        return userProfileTemplate(self.currScore, self.prevScore)

    def score(self):
        return self.currScore

    def subScores(self):
        res = {}
        res[AreaStamina.scoreType] = {}
        res[AreaStamina.scoreType]["score"] = self.currScore
        res[AreaStamina.scoreType]["coachingTip"] = self.coachingTipRes
        return res


class AreaStaminaFactory():
    def configuredObject(y, configs):
        if configs["peaks"]["scipyPeaks"]:
            global peaks
            currPeaks = peaks
            peaks = scipyPeaks
        areaStamina = AreaStamina(y, configs)
        if configs["peaks"]["scipyPeaks"]:
            peaks = currPeaks
        return areaStamina




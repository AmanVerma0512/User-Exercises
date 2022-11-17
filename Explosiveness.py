import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod

from numpy import diff


class Explosiveness(Score):
    scoreType = "explosiveness"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev
        self.compute()
        self.coachingTip()

    def compute(self):
        # calculate 2 paramters:
        #     1.y[peak] - y[base]
        #     2. total time of descent on smoothened curve in a rep
        xp = peaks(self.y)

        temp = [x for x in self.y]
        temp.sort()
        hi = sum(temp[-3:]) / 3
        dx = 1
        dy = diff(smoothen(y=y, window_size=5)) / dx
        ddy = diff(dy) / dx
        roots = []
        for i in range(len(ddy)):
            if dy[i] == 0 and ddy[i] <= sum(ddy) / (4 * len(ddy)) and y[i] > 0.1 * max(y):
                roots.append(i)
        temp = [y[i] for i in roots]
        base = mode(self.y)
        cumm = 0
        for i in range(len(self.y) - 1):
            if self.y[i + 1] > self.y[i]:
                cumm += 1
        avg_desc = cumm / len(xp)
        self.currScore = (hi - base) / avg_desc
        self.currScore *= 100

    def coachingTip(self):
        self.coachingTipRes = coachingTipTemplate(Explosiveness.scoreType, self.currScore)
        return self.coachingTipRes

    def userProfileScore(self):
        return userProfileTemplate(self.currScore, self.prevScore)

    def score(self):
        return self.currScore

    def subScores(self):
        res = {}
        res[Explosiveness.scoreType] = {}
        self.compute()
        res[Explosiveness.scoreType]["score"] = self.currScore
        res[Explosiveness.scoreType]["coachingTip"] = self.coachingTipRes
        return res


class ExplosivenessFactory():
    def configuredObject(y, configs):
        if configs["scipyPeaks"]:
            global peaks
            currPeaks = peaks
            peaks = scipyPeaks
        explosiveness = Explosiveness(y, configs)
        if configs["scipyPeaks"]:
            peaks = currPeaks

        return explosiveness
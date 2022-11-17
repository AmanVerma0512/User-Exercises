import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


class SuddenRelease(Score):
    scoreType = "sudden release"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev
        self.start, self.end = getStartEnd(y)
        self.compute()
        self.coachingTip()

    def compute(self):
        # detecting using high negative slope and low value
        max_to_fall_ratio = self.config["max_to_fall_ratio"]
        fall_time = self.config["fall_time"]
        start, end = self.start, self.end
        y = self.y
        if type(y) == tuple:
            y = y[0]
        m = max(y)
        delta = m * max_to_fall_ratio
        t0 = fall_time
        sud = []
        for i in range(len(y)):
            j = 0
            while j <= t0 and y[i - j] >= y[i]:
                j += 1
            if j != 0 and y[i - j + 1] - y[i] > delta:
                sud.append(i)
        self.currScore = Policy.rep_and_threshold(self.y, sud, 0) * 100
        self.currScore = clip100(self.currScore)
        return self.currScore

    def coachingTip(self):
        self.coachingTipRes = coachingTipTemplate(self.scoreType, self.currScore)
        return self.coachingTipRes

    def userProfileScore(self):
        return userProfileTemplate(self.currScore, self.prevScore)

    def score(self):
        self.compute()
        return self.currScore

    def subScores(self):
        res = {}
        res[SuddenRelease.scoreType] = {}
        self.compute()
        res[SuddenRelease.scoreType]["score"] = self.currScore
        res[SuddenRelease.scoreType]["coachingTip"] = self.coachingTipRes
        return res

class SuddenReleaseFactory():
    def configuredObject(y,configs):
        suddenRelease=SuddenRelease(y,configs)
        return suddenRelease
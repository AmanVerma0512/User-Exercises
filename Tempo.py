import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


class Tempo(Score):
    scoreType = "tempo"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev  # getPrevScore()
        self.compute()
        self.coachingTip()

    def compute(self):
        xp = peaks(self.y)
        xp = [int(i) for i in xp]
        curr_tempo = []
        for i in range(1, len(xp)):
            curr_tempo.append(xp[i] - xp[i - 1])
        self.currScore = np.var(curr_tempo)
        avg = sum(curr_tempo) / len(curr_tempo) if len(curr_tempo) else 0
        self.currScore /= avg
        self.currScore *= 100
        self.currScore = 100 - self.currScore
        self.currScore = clip100(self.currScore)
        return curr_tempo, avg, self.currScore

    # config variatitons: peaks

    def coachingTip(self):
        self.coachingTipRes = coachingTipTemplate(Tempo.scoreType, self.currScore)
        return self.coachingTipRes

    def userProfileScore(self):
        return userProfileTemplate(self.currScore, self.prevScore)

    def score(self):
        return self.currScore

    def subScores(self):
        res = {}
        res[Tempo.scoreType] = {}
        self.compute()
        res[Tempo.scoreType]["score"] = self.currScore
        res[Tempo.scoreType]["coachingTip"] = self.coachingTipRes
        return res


class TempoFactory():
    def configuredObject(y, configs):
        usingScipyPeaks = configs["scipyPeaks"]
        if usingScipyPeaks:
            global peaks
            currPeaks = peaks
            peaks = scipyPeaks
        tempo = Tempo(y, configs)
        if usingScipyPeaks:
            peaks = currPeaks

        return tempo
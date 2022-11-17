import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod

class RingStamina(Score):
    scoreType = "ring stamina"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev  # getPrevScore()
        self.compute()
        self.coachingTip()

    def compute(self):
        power_ref = h_params["ring_stamina"]["power_ref"]
        time_ref = h_params["ring_stamina"]["time_ref"]
        start, end = getStartEnd(self.y)
        xp = peaks(y)
        peakVals = [self.y[int(i)] for i in xp]
        ref_y = statistics.mean(peakVals[:min(3, len(peakVals))])
        ref_y *= power_ref
        ref = (end - start) * ref_y
        if ref == 0:
            self.currScoroe = 0
            return self.currScore
        ref2 = time_ref * ref_y
        A = Area(self.y)
        area = A
        pow = min(1, (ref2 - area) / ref)
        t = end - start
        t = min(1, (t) / time_ref)
        self.currScore = max(0, min(1 - (pow * t), 1)) * 100
        self.currScore = clip100(self.currScore)
        return self.currScore

    def peakBased(self):
        power_ref = self.config["peakBased"]["power_ref"]
        time_ref = self.config["peakBased"]["time_ref"]
        start, end = getStartEnd(self.y)
        xp = peaks(y)
        xp = [self.y[int(i)] for i in xp]
        ref_y = statistics.mean(xp[:min(3, len(xp))])
        m = mode(y)
        ref_y -= m
        ref_y *= power_ref
        ref = (end - start) * ref_y
        ref2 = time_ref * ref_y
        A = Area(self.y)
        area = A - m * (end - start)
        pow = min(1, (ref2 - area) / ref)
        t = end - start
        t = min(1, (t) / time_ref)
        self.currScore = max(0, min(1 - (pow * t), 1)) * 100
        self.currScore = clip100(self.currScore)
        return self.currScore

    def coachingTip(self):
        self.coachingTipRes = coachingTipTemplate(RingStamina.scoreType, self.currScore)
        return self.coachingTipRes

    def userProfileScore(self):
        return userProfileTemplate(self.currScore, self.prevScore)

    def score(self):
        self.compute()
        return self.currScore

    def subScores(self):
        res = {}
        res[RingStamina.scoreType] = {}
        res[RingStamina.scoreType]["score"] = self.currScore
        res[RingStamina.scoreType]["coachingTip"] = self.coachingTipRes
        return res


class RingStaminaFactory():
    def configuredObject(y, configs):
        ringStamina = RingStamina(y, configs)
        if configs["peakBased"]:
            ringStamina.compute = ringStamina.peakBased
        return ringStamina
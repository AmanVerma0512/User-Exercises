import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


class Power(Score):
    scoreType = "power"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev
        self.compute()
        self.coachingTip()

    def compute(self):
        bwt = self.config["bwt"]
        gender = self.config["gender"]
        exercise_mode = self.config["exercise_mode"]

        params = {
            "men's":
                {"Equipped Powerlifting":
                     {"A": 1236.25115,
                      "B": 1449.21864,
                      "C": 0.01644},
                 "Classic Powerlifting":
                     {"A": 1199.72839,
                      "B": 1025.18162,
                      "C": 0.00921},
                 "Equipped Bench Press":
                     {"A": 381.22073,
                      "B": 733.79378,
                      "C": 0.02398},
                 "Classic Bench Press":
                     {"A": 320.98041,
                      "B": 281.40258,
                      "C": 0.01008}},
            "women's":
                {"Equipped Powerlifting":
                     {"A": 758.63878,
                      "B": 949.31382,
                      "C": 0.02435},
                 "Classic Powerlifting":
                     {"A": 610.32796,
                      "B": 1045.59282,
                      "C": 0.03048},
                 "Equipped Bench Press":
                     {"A": 221.82209,
                      "B": 357.00377,
                      "C": 0.02937},
                 "Classic Bench Press":
                     {"A": 142.40398,
                      "B": 442.52671,
                      "C": 0.04724}},

        }
        xp = peaks(y)
        d = {}
        for i in xp:
            d[i] = self.y[i]
        d = {k: v for k, v in sorted(d.items(), key=lambda item: -item[1])}
        c = min(3, len(xp))
        o = 0
        power = 0
        for key in list(d.keys()):
            power += d[key]
            o += 1
            if (o > c):
                break
        power /= c
        coeff = 100 / (params[gender][exercise_mode]["A"] - params[gender][exercise_mode]["B"] * (
                2.718281828459 ** (-1 * params[gender][exercise_mode]["C"] * bwt)))
        self.normalizedScore = power * coeff
        self.unNormalizedScore = power

        self.currScore = power / (self.getPowerReferenceFromHistory() * self.config["growth factor"])

    def getPowerReferenceFromHistory(self):
        return self.unNormalizedScore

    def coachingTip(self):
        self.coachingTipRes = coachingTipTemplate(Power.scoreType, self.currScore)
        return self.coachingTipRes

    def userProfileScore(self):
        return userProfileTemplate(self.currScore, self.prevScore)

    def score(self):
        return self.currScore

    def unNormalizedScore(self):
        return self.unNormalizedScore

    def subScores(self):
        res = {}
        res[Power.scoreType] = {}
        self.compute()
        res[Power.scoreType]["score"] = self.currScore
        res[Power.scoreType]["coachingTip"] = self.coachingTipRes
        return res


class PowerFactory():
    def configuredObject(y,configs):
        if "scipyPeaks" in configs:
            global peaks
            currPeaks=peaks
            peaks = scipyPeaks
            power=Power(y,configs)
            peaks=currPeaks
            return power
        else:
            return Power(y,configs)
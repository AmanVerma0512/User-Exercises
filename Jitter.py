import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod


class Jitter(Score):
    scoreType = "jitter"

    def __init__(self, y, configs):
        self.y = y
        self.config = configs
        self.prevScore = dummy_prev
        self.compute()
        self.coachingTip()

    def compute(self):
        window_size = self.config["window_size"]
        delta = self.config["delta"]
        t0 = self.config["t0"]
        x_dist_rel = self.config["x_dist_rel"]
        jitterPolicyThreshold = self.config["jitterPolicyThreshold"]
        y = self.y
        m = mode(y)
        moving_averages = []
        jitter = []

        for i in range(len(y)):
            window_average = np.sum(y[max(0, i - window_size):i]) / window_size
            moving_averages.append(window_average)
            k = 0
            cross = []
            for j in range(t0):
                if y[i - j] > window_average and y[i - j - 1] < window_average or y[i - j] < window_average and y[
                    i - j - 1] > window_average and abs(y[i] - m) < x_dist_rel * max(y):
                    k += 1
                    cross.append(i - j)
            if k >= delta and abs(y[i] - m) < x_dist_rel * max(y):
                jitter.append(int(sum(cross) / len(cross)))
        start, end = getStartEnd(y)
        xp = peaks(y)
        xp = [int(i) for i in xp]

        dj = {}
        for p in xp:
            dj[p] = []

        xp.insert(0, 0)
        xp.append(len(y) - 1)

        # merging within a rep
        for j in jitter:
            for i in range(len(xp) - 1):
                l = xp[i]
                r = xp[i + 1]
                if i < (len(xp) - 1) and j >= l and j <= r:
                    dj[l].append(j)

        fj = []
        for key in dj.keys():
            if len(dj[key]) > 0:
                fj.append(int(sum(dj[key]) / len(dj[key])))

        for j in jitter:
            if y[j] < max(y) / 12:
                jitter.remove(j)
        self.currScore = 1 - Policy.rep_and_threshold(self.y, jitter, jitterPolicyThreshold)
        self.currScore *= 100
        self.currScore = clip100(self.currScore)
        return self.currScore

    def smooth_blips(self):
        config = self.config["smoothBlips"]
        smoothenFactor = config["smoothenFactor"]
        prominentPeaksProminence = config["prominentPeaksProminence"]
        prominentPeaksWidth = config["prominentPeaksWidth"]
        smallPeaksHeightLowerFactor = config["smallPeaksHeightLowerFactor"]
        smallPeaksHeightHigherFactor = config["smallPeaksHeightHigherFactor"]
        smallPeaksWidth = config["smallPeaksHeightHigherFactor"]

        temp = self.y
        temp.sort()
        y_max = statistics.mean(temp[max(-3, -len(temp) + 1):])
        y = smoothen(self.y, smoothenFactor)
        prominent_peaks, _ = find_peaks(y, prominence=prominentPeaksProminence * y_max, width=prominentPeaksWidth)
        small_peaks, _ = find_peaks(y,
                                    height=[smallPeaksHeightLowerFactor * y_max, smallPeaksHeightHigherFactor * y_max],
                                    width=smallPeaksWidth)
        self.currScore = 100 * len(prominent_peaks) / (len(small_peaks) + len(prominent_peaks))
        self.currScore = clip100(self.currScore)
        return self.currScore

    def coachingTip(self):
        self.coachingTipRes = coachingTipTemplate(Jitter.scoreType, self.currScore)
        return self.coachingTipRes

    def userProfileScore(self):
        return userProfileTemplate(self.currScore, self.prevScore)

    def score(self):
        self.compute()
        return self.currScore

    def subScores(self):
        res = {}
        res[Jitter.scoreType] = {}
        self.compute()
        res[Jitter.scoreType]["score"] = self.currScore
        res[Jitter.scoreType]["coachingTip"] = self.coachingTipRes
        return res

class JitterFactory():
    def configuredObject(y,configs):
        usingScipyPeaks=configs["scipyPeaks"]
        if usingScipyPeaks:
            global peaks
            currPeaks=peaks
            peaks = scipyPeaks
        jitter=Jitter(y,configs)
        if usingScipyPeaks:
            peaks=currPeaks
        if "smoothBlips" in configs:
            jitter.compute = jitter.smooth_blips
        return jitter
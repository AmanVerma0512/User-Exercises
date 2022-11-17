import abc
from utils import *
from FeatureExtraction import *
from SignalProcessing import *
from h_params import *
from abc import ABC, abstractmethod

def getScores(y, configs, header):
    subScoresObjects = [
        FormScoreFactory.configuredObject(y, h_params1["formScore"]), \
        StaminaFactory.configuredObject(y, h_params1["stamina"]), \
        AggPowerScoreFactory.configuredObject(y, h_params1["power"])
    ]

    resList = [subScore.subScores() for subScore in subScoresObjects]
    res = dict(ChainMap(*resList))
    res = {
        "scores": res
    }
    if header["score"] == False:
        removeKeys(res, "score")
    if header["coachingTip"] == False:
        removeKeys(res, "coachingTip")
    if header["subScores"] == False:
        removeKeys(res, "subScores")
    return res  
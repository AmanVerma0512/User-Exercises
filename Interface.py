from utils import FormScore,Scoring
import pandas as pd
import datetime
from os.path import exists
import time

class Interface():
    def __init__(self,h_params, y,log_dir="D:\Forge\Forge\Scores\MVP_cordova_ios_android\Scores/"):
        plot_dir = log_dir + "plots/" + str(time.time())
        self.fs=FormScore(y,plot_dir=plot_dir)
        self.fs.h_params=h_params


        response=Scoring(self.fs, "rep_and_threshold").scores()
        df_path=log_dir+"interface-logs.csv"
        if exists(df_path):
            df = pd.read_csv(df_path)
        else:
            df = pd.DataFrame(columns=["h_params","signal","response","time"])


        df=df.append({
            "h_params":str(h_params),
            "signal":str(y),
            "response":str(response),
            "time":str(datetime.datetime.now()),
            "plots":plot_dir
        },ignore_index=True)


        # add time index and save plots with same
        # name parameters in a readable format
        # readibility, for jason too
        # tidy up code, create abstract and factory
        # power form stamina
        # os.remove(df_path)
        df.to_csv(df_path)
        print(df.head())



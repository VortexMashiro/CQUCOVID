import pandas as pd
import numpy as np
import csv
import json
import os


# print(os.path.isfile("tmp/covid/Anguilla1.csv"))
# data = pd.read_csv("tmp/covid/Anguilla.csv")

def get_first_of(country, date, attribute, n):
    if os.path.isfile("tmp/data/" + country + ".csv"):
        data = pd.read_csv(
            open(os.path.join("tmp/data/", country + '.csv', ), "r", encoding="utf-8"),
           index_col="Updated")
        data = data.loc[date][[attribute,"AdminRegion1"]].dropna()
        data = data.sort_values(by=[attribute],ascending=False)
        return data.head(n)["AdminRegion1"].tolist()
    else:
        print("没有相关数据文件")
        return None

def get_contry_areas(country, area_list):
    if os.path.isfile("tmp/data/" + country + ".csv"):
        data = pd.read_csv(
            open(os.path.join("tmp/data/", country + '.csv', ), "r", encoding="utf-8"))
        result = []
        for area in area_list:
            data_tmp = data[data["AdminRegion1"]==area]
            data_tmp = data_tmp[["Updated","Confirmed","ConfirmedChange","Deaths","Recovered","AdminRegion1"]]
            # print(data_tmp)
            result_area = []
            for index in range(0,len(data_tmp)):
                result_area.append(data_tmp)
            result.append(result_area)
        return result
areas = get_first_of("China (mainland)", "06/25/2020",'ConfirmedChange',5)
print(areas)
print(get_contry_areas("China (mainland)",areas))


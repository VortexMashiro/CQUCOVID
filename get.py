import pandas as pd
import numpy as np
import os


def get_word_epidemic(date):
    """
    获取世界疫情数据
    :param date: 04/25/2020
    :return: list
    """
    date_name = date.replace("/", "-")
    if os.path.exists("data/world-epidemic/" + date_name + ".csv"):
        data = pd.read_csv(open(
            os.path.join("data/world-epidemic/", date_name + ".csv"),
            'r', encoding="utf-8"), dtype=np.object)
        result_list = []
        for index in range(0, data.shape[0]):
            item = data.iloc[index].tolist()
            result_list.append(item)
        return result_list
    else:
        print("没有这一天的数据！")
        return None


def get_country_epidemic(date, country):
    """
    获取国家的疫情数据
    :param date: 04/25/2020
    :param country:  China
    :return: list
    """
    date_name = date.replace("/", "-")
    file_name = "data/country-epidemic/" \
                + date_name + "-" + country + ".csv"
    if os.path.isfile(file_name):
        data = pd.read_csv(
            open(os.path.join("data/country-epidemic/", date_name + "-" + country + ".csv"),
                 "r", encoding="utf-8"), dtype=np.object)
        result = []
        for index in range(0, data.shape[0]):
            result.append(data.iloc[index].tolist())
        return result
    else:
        print("没有相关数据！")
        return None


def get_country_epidemic_summary(country):
    """
    获取国家疫情概述数据
    :param country:
    :return: list
    """
    file = "data/country-epidemic-summary/" + country + ".csv"
    if os.path.isfile(file):
        data = pd.read_csv(
            open(os.path.join("data/country-epidemic-summary/", country + ".csv"),
                 "r", encoding="utf-8"), dtype=np.object)
        confirmed_list = []
        death_list = []
        for index in range(0, data.shape[0]):
            item = data.iloc[index]
            date = item["Updated"]
            confirmed_list.append([date, item["Confirmed"]])
            death_list.append([date, item["Deaths"]])
        return confirmed_list, death_list
    else:
        print("没有相关数据！")
        return None, None


def get_confirmed_distribution(country, date):
    """
    获取累计确诊的分布情况
    :param country: China
    :param date: 04/25/2020
    :return: list
    """
    date_name = date.replace("/", "-")
    file_name = "data/country-epidemic/" \
                + date_name + "-" + country + ".csv"
    if os.path.isfile(file_name):
        data = pd.read_csv(
            open(os.path.join("data/country-epidemic/", date_name + "-" + country + ".csv"),
                 "r", encoding="utf-8"), dtype=np.object)
        data = data[["Confirmed", "AdminRegion1"]]
        result = []
        for index in range(0, data.shape[0]):
            result.append(data.iloc[index].tolist())
        return result
    else:
        print("没有相关数据！")
        return None


def get_new_confirmed_deaths(country):
    """
    获取各个国家各地的新增确诊和新增死亡数量
    :param country: "China"
    :return: list
    """
    file = "data/new-confirmed-death/" + country + ".csv"
    if os.path.isfile(file):
        data = pd.read_csv(
            open(os.path.join("data/new-confirmed-death/", country + ".csv"),
                 "r", encoding="utf-8"), dtype=np.object)
        new_confirmed_list = []
        new_death_list = []
        date_list = []
        for index in range(0, data.shape[0]):
            item = data.iloc[index]
            date = item["Updated"]
            date_list.append(item["Updated"])
            new_confirmed_list.append(item["ConfirmedChange"])
            new_death_list.append(item["DeathsChange"])
        return date_list, new_confirmed_list, new_death_list
    else:
        print("没有相关数据！")
        return None, None, None


def get_new_confirmed_top5(country, date):
    """
    根据日期和国家获取新增确诊的top5
    :param country:"China"
    :param date: "04/24/2020
    :return: list
    """
    date_name = date.replace("/", "-")
    file_name = "data/country-epidemic/" \
                + date_name + "-" + country + ".csv"
    print(file_name)
    if os.path.isfile(file_name):
        data = pd.read_csv(
            open(os.path.join("data/country-epidemic/", date_name + "-" + country + ".csv"),
                 "r", encoding="utf-8"), dtype=np.object)
        if data.shape[0] == 0:
            return None
        data.sort_values(by="ConfirmedChange", ascending=False, inplace=True)
        result = []
        area = []
        if data.shape[0] > 5:
            data = data.head(5)
        for index in range(0, data.shape[0]):
            item = data.iloc[index]
            area.append(item["AdminRegion1"])
            result.append(item["ConfirmedChange"])
        return [area, result]
    else:
        print("没有相关数据文件！")
        return None


def get_region_comparion(country, date):
    """
    获取地区对比的疫情数据
    :param country: "China"
    :param date:  04/25/2020
    :return:Nothing
    """
    date_name = date.replace("/", "-")
    file_name1 = "data/country-epidemic/" \
                 + date_name + "-" + country + ".csv"
    if os.path.isfile(file_name1):
        data = pd.read_csv(
            open(os.path.join("data/country-epidemic/", date_name + "-" + country + ".csv"),
                 "r",encoding="utf-8"),dtype=np.object)
        data_c = data.sort_values(by="Confirmed")
        data_d = data.sort_values(by="Deaths")
        data_r = data.sort_values(by="Recovered")
        data_cc = data.sort_values(by="ConfirmedChange")

        if data.shape[0]>5:
            data_c = data_c.head(5)
            data_d = data_d.head(5)
            data_r = data_r.head(5)
            data_cc = data_cc.head(5)

        data_c = data_c["AdminRegion"].tolist()
        data_d = data_c["AdminRegion"].tolist()
        data_r = data_c["AdminRegion"].tolist()
        data_cc = data_c["AdminRegion"].tolist()

        for region in data_c:
            file_name2 = "data/country-epidemic-summary/"+region+".csv"



    else:
        print("")
        return None

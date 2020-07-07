import pandas as pd
import numpy as np
import os
import json


def convert_to_int(value):
    return int(value)


def get_word_epidemic(date):
    """
    根据日期获取所有国家对应的累计确诊、累计死亡、累计治愈
    以及最大的累计确诊值和最小的累计确诊值
    格式： [["country",[confirmed,death,recovered]],...]
    """
    date_name = date.replace("/", "-")
    directory = "data/world-epidemic/"
    if os.path.isfile(directory + date_name + ".csv"):
        data = pd.read_csv(open(
            os.path.join(directory, date_name + ".csv"),
            'r', encoding="utf-8"))
        max = data["Confirmed"].max()
        min = data["Confirmed"].min()
        result_list = []
        for index in range(0, data.shape[0]):
            item = data.iloc[index]
            result_list.append([item["Country_Region"], [int(item["Confirmed"]),
                                                         int(item["Deaths"]), int(item["Recovered"])]])
        return int(max), int(min), result_list
    else:
        return None, None, None


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
                 "r", encoding="utf-8"))
        confirmed = data["Confirmed"].astype(int)
        max = confirmed.max()
        min = confirmed.min()
        result = []
        for index in range(0, data.shape[0]):
            result.append(data.iloc[index].tolist())
        return max, min, result
    else:
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
        date_list = []
        for index in range(0, data.shape[0]):
            item = data.iloc[index]
            date_list.append(item["Updated"])
            confirmed_list.append(item["Confirmed"])
            death_list.append(item["Deaths"])
        return date_list, confirmed_list, death_list
    else:
        return None, None, None


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
            date_list.append(item["Updated"])
            new_confirmed_list.append(item["ConfirmedChange"])
            new_death_list.append(item["DeathsChange"])
        return date_list, new_confirmed_list, new_death_list
    else:
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
        return None


def get_region_comparion(country, date, attribute):
    """
    获取地区对比的疫情数据
    :param country: "China"
    :param date:  04/25/2020
    :param attribbute:  属性名称{Confirmed|Deaths|Recovered|ConfirmedChange}
    :return:Nothing
    """
    date_name = date.replace("/", "-")
    file_name1 = "data/country-epidemic/" \
                 + date_name + "-" + country + ".csv"
    file_name2 = "data/region-comparision/" + country + ".csv"
    if os.path.isfile(file_name1) and os.path.isfile(file_name2):
        data = pd.read_csv(
            open(os.path.join("data/country-epidemic/", date_name + "-" + country + ".csv"),
                 "r", encoding="utf-8"), dtype=np.object)
        if attribute not in data.columns:
            return None
        data.sort_values(by=attribute, inplace=True, ascending=False)

        if data.shape[0] > 5:
            data = data.head(5)
        region_list = data["AdminRegion1"].tolist()

        data = pd.read_csv(
            open(os.path.join("data/region-comparision/", country + ".csv"),
                 "r", encoding="utf-8"), dtype=np.object)
        region_column = data["AdminRegion1"]
        result = {}
        for region in region_list:
            item = data[region_column == region][["Updated", attribute]]
            date_list = item["Updated"].tolist()
            data_list = item[attribute].tolist()
            result[region] = [date_list, data_list]
        return result
    else:
        return None


def get_country_position():
    """
    获取所有国家的经纬度
    :return: position list
    """
    file = "data/position/country-position.csv"
    if os.path.isfile(file):
        data = pd.read_csv(
            open(os.path.join("data/position/" + "country-position.csv"),
                 "r", encoding="utf-8"))
        position_list = []
        for index in range(0, data.shape[0]):
            position_list.append(data.iloc[index].tolist())
        return position_list
    else:
        return None


def get_date_list():
    """

    """
    file = "data/country-epidemic-summary/Worldwide.csv"
    if os.path.isfile(file):
        return pd.read_csv(file)["Updated"].tolist()
    else:
        return None


def get_time_axis_data(date):
    """

    :return:
    """
    date_name = date.replace("/", "-")
    file = "data/world-epidemic/" + date_name + ".csv"
    if os.path.isfile(file):
        data = pd.read_csv(file, encoding="utf-8")
        data.sort_values(by="Confirmed",ascending=False,inplace=True)
        if data.shape[0] > 30:
            data = data.head(30)
        result = []
        max = int(data.head(1)["Confirmed"])
        min = int(data.tail(1)["Confirmed"])
        for index in range(0, data.shape[0]):
            row = data.iloc[index]
            result.append([str(row["Country_Region"]),
                           [int(row["Confirmed"]), str(row["Country_Region"])]])
        return max, min ,result


def get_world_confirmed():
    """

    """
    result = []
    date_list = get_date_list()
    for date in date_list:
        date_name = date.replace("/", "-")
        file_name = "data/world-epidemic/" + date_name + ".csv"
        data = pd.read_csv(file_name, encoding="utf-8")
        result.append(int(data.iloc[0]["Confirmed"]))
    return result

def get_country_status(country="China"):
    """

    """
    file_name = "data/country-status/country_status.csv"
    if os.path.isfile(file_name):
        data = pd.read_csv(
            open(os.path.join("data/country-status/", "country_status.csv"),
                 "r", encoding="utf-8"), dtype=np.str)
        data = data[data["Country_Region"] == country]
        if data.shape[0] == 0:
            return None
        data = data.iloc[0].tolist()
        c = int(data[0])
        nc = int(data[1])
        d = int(data[2])
        nd = int(data[3])
        r = int(data[4])
        nr = int(data[5])
        total = c + r + d
        total_today = nc + nd + nr
        dict = {
            'total': format(total, ','),
            'total_today': format(total_today, ','),
            'confirm_total': format(c, ','),
            'confirm_today': format(nc, ','),
            'recover_total': format(d, ','),
            'recover_today': format(nd, ','),
            'death_total': format(r, ','),
            'death_today': format(nr, ',')
        }
        return dict
    else:
        return None


def get_country_list_with_data():
    """

    """
    file = "data/country-status/country_status.csv"
    if os.path.isfile(file):
        data = pd.read_csv(file, encoding="utf-8")
        country_list = []
        tmp = []
        for index in range(0, data.shape[0]):
            row = data.iloc[index]
            total = int(row["Confirmed"]) \
                    + int(row["Deaths"]) \
                    + int(row["Recovered"])
            country = row["Country_Region"]
            tmp.append([country, total])
        tmp_df = pd.DataFrame(data=tmp, columns=["country", "total"])
        tmp_df.sort_values(by="total", inplace=True, ascending=False)
        for index in range(0, tmp_df.shape[0]):
            row = tmp_df.iloc[index]
            country_list.append({"name": row["country"],
                                 "number": format(row["total"], ',')})
        return country_list
    else:
        return None


def get_samll_picture_data(country="China"):
    """

    """
    dire1 = "data/country-epidemic-summary/"
    dire2 = "data/new-confirmed-death/"
    file1 = dire1 + country + ".csv"
    file2 = dire2 + country + ".csv"
    if os.path.isfile(file1) & os.path.isfile(file2):
        data1 = pd.read_csv(
            open(os.path.join(dire1, country + ".csv"), "r", encoding="utf-8"))
        data1 = data1["Deaths"]
        data2 = pd.read_csv(
            open(os.path.join(dire2, country + ".csv"), "r", encoding="utf-8"))
        data2 = data2[["Updated", "ConfirmedChange"]]
        date_list = []
        confirmed_change = []
        deaths = []
        for index in range(0, data1.shape[0]):
            row1 = data1.iloc[index]
            row2 = data2.iloc[index]
            deaths.append(row1)
            date_list.append(row2["Updated"])
            confirmed_change.append(row2["ConfirmedChange"])
        return date_list, confirmed_change, deaths
    else:
        return None


def get_today():
    """
    返回最新日期
    :return str
    """
    file = "data/country-epidemic-summary/Worldwide.csv"
    if os.path.isfile(file):
        return str(pd.read_csv(file)["Updated"].tolist()[-1])
    else:
        return None

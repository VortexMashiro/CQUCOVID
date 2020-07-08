import pandas as pd
import numpy as np
import os
import json

# 预处理

dict_country = {'China (mainland)': 'China',
                'South Korea': 'Korea',
                'Laos': 'Lao PDR',
                'Eswatini': 'Swaziland',
                'South Sudan': 'S. Sudan',
                'Central African Republic': 'Central African Rep.',
                'Equatorial Guinea': 'Eq. Guinea',
                'Congo (DRC)': 'Dem. Rep. Congo',
                'North Macedonia': 'Macedonia',
                'Bosnia and Herzegovina': 'Bosnia and Herz.',
                'Czechia': 'Czech Rep.',
                'Faroe Islands': 'Faroe Is.',
                'Dominican Republic': 'Dominican Rep.',
                'Cabo Verde': 'Cape Verde',
                'Falkland Islands': 'Falkland Is.',
                "Hong Kong SAR":"香港",
                "Taiwan":"台湾"}

dict_province = {
    "Anhui": "安徽",
    "Beijing": "北京",
    "Chongqing": "重庆",
    "Fujian": "福建",
    "Gansu": "甘肃",
    "Guangdong": "广东",
    "Guangxi Zhuang": "广西",
    "Guizhou": "贵州",
    "Hainan": "海南",
    "Hebei": "河北",
    "Heilongjiang": "黑龙江",
    "Henan": "河南",
    "Hubei": "湖北",
    "Hunan": "湖南",
    "Inner Mongolia": "内蒙古",
    "Jiangsu": "江苏",
    "Jiangxi": "江西",
    "Jilin": "吉林",
    "Liaoning": "辽宁",
    "Ningxia": "宁夏",
    "Qinghai": "青海",
    "Shaanxi": "陕西",
    "Shandong": "山东",
    "Shanghai": "上海",
    "Shanxi": "山西",
    "Sichuan": "四川",
    "Tianjin": "天津",
    "Xinjiang": "新疆",
    "Xizang": "西藏",
    "Yunnan": "云南",
    "Zhejiang": "浙江",
}

def converte_int(string):
    return int(float(string))

def province_map(key):
    value = dict_province.get(key)
    if value == None:
        return key
    else:
        return value


def country_map(key):
    value = dict_country.get(key)
    if value == None:
        return key
    else:
        return value


# df = pd.read_csv("Bing-COVID19-Data.csv", dtype=np.object)
# df["Country_Region"] = df["Country_Region"].apply(country_map)
# df["AdminRegion1"] = df["AdminRegion1"].apply(province_map)
# df.to_csv("Bing-COVID19-Data.csv", index=None, encoding="utf-8")


# 预处理结束

def extra_source():
    if os.path.isfile("Bing-COVID19-Data.csv"):
        return pd.read_csv(
            "Bing-COVID19-Data.csv", index_col="ID", dtype=np.object)
    else:
        return None


def extra_date_list(source):
    country_column = source["Country_Region"]
    date_column = source[country_column == "Worldwide"]["Updated"]
    return date_column.tolist()


def extra_country_list(source):
    """
    抽取国家列表
    :param source: 源数据
    :return: list
    """
    country_list = []
    country_column = source["Country_Region"].unique()
    for index in range(0, len(country_column)):
        country_list.append(country_column[index])
    return country_list


def extra_word_epidemic(source, date_list):
    """
    抽取世界疫情数据
    :param source: 源数据
    :param date_list: 日期列表
    :return: Nothing
    """
    date_column = source["Updated"]
    country_column = source["AdminRegion1"].isna()
    for date in date_list:
        data = source[(date_column == date) & country_column]
        data = data[["Country_Region","Confirmed", "Deaths", "Recovered"]]
        data.drop(data.index[0],inplace=True)
        file_name = "world-epidemic/" + date.replace("/", "-") + ".csv"
        data.fillna(method="pad", inplace=True)
        data.fillna(value=0, inplace=True)
        data["Confirmed"] = data["Confirmed"].astype(int)
        data["Deaths"] = data["Deaths"].astype(int)
        data["Recovered"] = data["Recovered"].astype(int)
        data.sort_values(by="Country_Region",inplace=True)
        data.to_csv(file_name, index=None, encoding="utf-8")


def extra_country_epidemic(source, date_list, country_list):
    """
    抽取国家疫情数据
    :param source: 源数据
    :param date_list: 日期列表
    :param country_list:  国家列表
    :return: Nothing
    """
    for date in date_list:
        data_date = source[source.Updated == date]
        for country in country_list:
            c2 = data_date["AdminRegion1"].notna()
            data_country = pd.DataFrame()
            if country == "Worldwide":
                c2 = data_date["AdminRegion1"].isna()
                data_country_tmp = data_date[c2]
                data_country = data_country_tmp.drop(
                    index = data_country_tmp.index[0])
            else:
                c1 = data_date.Country_Region == country
                data_country = data_date[c1 & c2]

            if data_country.shape[0] == 0:
                continue
            if country == "Worldwide":
                data_country = data_country[["Confirmed", "ConfirmedChange","Deaths","Recovered","Country_Region"]]
            else:
                data_country = data_country[["Confirmed", "ConfirmedChange","Deaths","Recovered","AdminRegion1"]]
            data_country.fillna(method="pad", inplace=True)
            data_country.fillna(value=0, inplace=True)
            file_name = "country-epidemic/" \
                        + date.replace("/", "-") + "-" + country + ".csv"
            data_country.to_csv(file_name, encoding="utf-8", index=None)


def extra_country_epidemic_summary(source, country_list):
    """
    抽取国家疫情概述数据
    :param source: 源数据
    :param country_list: 国家列表
    :return: Nothing
    """
    areas = source["AdminRegion1"].isna()
    country_column = source["Country_Region"]
    for country in country_list:
        data = source[(country_column == country) & areas]
        data = data[["Updated", "Confirmed","ConfirmedChange",
                     "Deaths","DeathsChange"]]
        data.fillna(method="pad", inplace=True)
        data.fillna(value=0, inplace=True)
        file_name = "country-epidemic-summary/" + country + ".csv"
        data.to_csv(file_name, encoding="utf-8", index=None)


def extra_region_comparision(source, country_list):
    """

    :param source:
    :param country_list:
    :return:
    """
    areas = source["AdminRegion1"].notna()
    country_column = source["Country_Region"]
    for country in country_list:
        data = source[(country_column == country) & areas]
        if data.shape[0] == 0:
            continue
        data = data[["Updated", "Confirmed", "ConfirmedChange",
                     "Deaths", "Recovered", "AdminRegion1"]]
        data.fillna(method="pad", inplace=True)
        data.fillna(value=0, inplace=True)
        file_name = "region-comparision/" + country + ".csv"
        data.to_csv(file_name, encoding="utf-8", index=None)

def extra_time_axis_data(date_list):
    """

    :param date_list:
    :return:
    """
    directory = "world-epidemic/"
    DATA = []
    for date in date_list:
        date_name = date.replace("/", "-")
        file_name = directory + date_name + ".csv"
        data = pd.read_csv(file_name, dtype=np.object,encoding="utf-8")
        item_list = []
        for index in range(1, data.shape[0]):
            row = data.iloc[index]
            item_dict = [row["Confirmed"],row["Country_Region"]]
            item_list.append(item_dict)
        DATA.append({"time":date, "data":item_list})



def extra_country_status(source, country_list, date_list):
    """

    """
    date = date_list[-1]
    country_column = source["Country_Region"]
    area_column = source["AdminRegion1"].isna()
    column_list = ["Confirmed", "ConfirmedChange", "Deaths",
                   "DeathsChange", "Recovered", "RecoveredChange", "Country_Region"]
    print(date)
    result_list = []
    for country in country_list:
        data1 = source[(country_column == country) & area_column]
        data1 = data1[["Updated", "Confirmed", "ConfirmedChange", "Deaths",
                       "DeathsChange", "Recovered", "RecoveredChange", "Country_Region"]]
        data1.ffill(inplace=True)
        data1.fillna(value=0, inplace=True)
        updated_column = data1["Updated"]
        data = data1[updated_column == date]
        if data.shape[0] == 0:
            continue
        data = data[column_list]
        result_list.append(data.iloc[0].tolist())
    file_name = "country-status/country_status.csv"
    result = pd.DataFrame(data=result_list, columns=column_list)
    result.to_csv(file_name, encoding="utf-8", index=None)


# source_data = extra_source()
# print("extra_source")
# date_list_data = extra_date_list(source_data)
# print("extra_date_list")
# extra_word_epidemic(source_data, date_list_data)
# print("extra_word_epidemic")
# country_list_data = extra_country_list(source_data)
# print("extra_country_list")
# extra_country_epidemic(source_data, date_list_data, country_list_data)
# print("extra_country_epidemic")
# extra_country_epidemic_summary(source_data, country_list_data)
# print("extra_country_epidemic_summary")
# extra_region_comparision(source_data,country_list_data)
# print("extra_region_comparision")
# extra_country_position(source_data,country_list_data)
# print("extra_country_position")
# extra_time_axis_data(date_list_data)
# print("extra_time_axis_data")
# extra_country_status(source_data, country_list_data, date_list_data)
#
import pandas as pd
import numpy as np
import os


# 预处理

def extra_source():
    """
    获取数据源
    :return: dataframe
    """
    if os.path.isfile("Bing-COVID19-Data.csv"):
        return pd.read_csv(
            "Bing-COVID19-Data.csv", index_col="ID", dtype=np.object)
    else:
        print("没有源数据文件！")
        return None


def extra_date_list(source):
    """
    抽取时间线
    :return:list
    """
    country_column = source["Country_Region"]
    date_column = source[country_column == "Worldwide"]["Updated"]
    date_list = []
    for index in range(0, date_column.shape[0]):
        date_list.append(date_column.iloc[index])
    return date_list


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
    for date in date_list:
        data = source[date_column == date]
        data = data[["Confirmed", "ConfirmedChange",
                     "Deaths", "Recovered", "Country_Region"]]
        file_name = "data/world-epidemic/" + date.replace("/", "-") + ".csv"
        data.fillna(method="pad", inplace=True)
        data.fillna(value=0, inplace=True)
        data.to_csv(file_name, index=None, encoding="utf-8")
        print(date)


def extra_country_epidemic(source, date_list, country_list):
    """
    抽取国家疫情数据
    :param source: 源数据
    :param date_list: 日期列表
    :param country_list:  国家列表
    :return: Nothing
    """
    area_column = source["AdminRegion1"].notna()
    for date in date_list:
        date_column = source["Updated"]
        for country in country_list:
            country_column = source["Country_Region"]
            condition = (date_column == date) & (country_column == country)
            condition = condition & area_column
            data = source[condition]
            if data.shape[0] == 0:
                continue
            data = data[["Confirmed", "ConfirmedChange",
                         "Deaths", "Recovered", "AdminRegion1"]]
            data.fillna(method="pad", inplace=True)
            data.fillna(value=0, inplace=True)
            file_name = "data/country-epidemic/" \
                        + date.replace("/", "-") + "-" + country + ".csv"
            data.to_csv(file_name, encoding="utf-8", index=None)
            print(date, country)


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
        data = source[(country_column == country) & areas][["Updated", "Confirmed", "Deaths"]]
        data.fillna(method="pad", inplace=True)
        data.fillna(value=0, inplace=True)
        file_name = "data/country-epidemic-summary/" + country + ".csv"
        data.to_csv(file_name, encoding="utf-8", index=None)
        print(country)


def extra_new_confirmed_death(source, country_list):
    """
    抽取各个国家各地的新增确诊和新增死亡数量
    :param country_list: 国家列表
    :return: Nothing
    """
    country_column = source["Country_Region"]
    for country in  country_list:
        data = source[country_column==country][["Updated","ConfirmedChange","DeathsChange"]]
        data.fillna(method="pad", inplace=True)
        data.fillna(value=0, inplace=True)
        file_name = "data/new-confirmed-death/"+country+".csv"
        data.to_csv(file_name,encoding="utf-8", index=None)
        print(country)

source_data = extra_source()
# date_list_data = extra_date_list(source_data)
# print(date_list_data)
# extra_word_epidemic(source_data, date_list_data)
country_list_data = extra_country_list(source_data)
print(country_list_data)
# extra_country_epidemic(source_data, date_list_data, country_list_data)
# extra_country_epidemic_summary(source_data, country_list_data)
# extra_new_confirmed_death(source_data, country_list_data)

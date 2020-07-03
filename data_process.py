import pandas as pd
import numpy as np
import csv
import json
import os

source = pd.read_csv("Bing-COVID19-Data.csv",
                     index_col="ID", dtype=np.object)


def get_date_list():
    """
    按序返回日期列表
    """
    if os.path.isfile("tmp/data/Worldwide.csv"):
        return pd.read_csv("tmp/data/Worldwide.csv")["Updated"]
    else:
        print("请先将数据源按国家低去分离！")
        return None


def get_country_list():
    """
    返回按序排列且不重复的国家列表
    :return:
    """
    if os.path.isfile("data/country_list.csv"):
        return pd.read_csv("data/country_list.csv")["country"]
    else:
        print("请先统计有那些国家和地区")
        return None


def get_country_list_with_data():
    """
    :return:
    """
    return None

def get_covid_data_by_ctry(country):
    """
    获取一个国家的疫情数据
    :param country: 国家/地区名称
    :return: 疫情数据的DataFrame
    """
    if os.path.isfile("tmp/covid/" + country + ".csv"):
        data = pd.read_csv(
            open(os.path.join("tmp/covid/", country + ".csv"),
                 'r', encoding='utf-8'),
            dtype=np.object)
        return data
    else:
        print("没有" + country + "的数据文件！")
        return None


def get_covid_data_by_date(date):
    """

    :param date:
    :return:
    """
    return None





def statistics_country_list(data_source):
    """
    :data_source 数据源DataFrame:
    统计有哪些国家和地区
    结果存放在data/country_list.csv
    """
    if 'Country_Region' in data_source.columns:
        country_list = data_source["Country_Region"].unique()
        country_list_csv = open("data/country_list.csv",
                                mode="w", newline="", encoding="utf-8-sig")
        writer = csv.writer(country_list_csv)
        writer.writerow(["country"])
        for country in country_list:
            writer.writerow([country])
    else:
        print("数据源没有名字是Country_Region的列！")


def separate_source(data_source, country_list_u):
    """
    将数据按国家分开
    :data_source 数据源DataFrane:
    :country_list_u 国家地区按序排列的不重复列表:
    :return: 不返回数据，结果存放在tmp/data文件夹下
    """
    if "Country_Region" in data_source.columns:
        country_column = data_source["Country_Region"]
        for country in country_list_u:
            data_by_country_region = data_source[country_column == country]
            file_name = "tmp/data/" + country + ".csv"
            data_by_country_region.to_csv(file_name, index=None)
    else:
        print("数据源没有名字是Country_Region的列！")
        return None


def separate_covid_data_by_ctry(country_list_u):
    """
    统计每个国家的疫情数据
    :country_list_u 国家地区按序排列的不重复列表:
    :return: 不返回结果, 将结果存储在tmp/covid中
    """
    for country in country_list_u:
        if os.path.isfile("tmp/data/" + country + ".csv"):
            data = pd.read_csv(
                open(os.path.join("tmp/data/", country + ".csv"),
                     'r', encoding='utf-8'),
                dtype=np.object)
            data = data[data["AdminRegion1"].isna()]
            data.drop(columns=[
                "Latitude", "Longitude", "ISO2",
                "ISO3", "AdminRegion1", "AdminRegion2"], inplace=True)
            data.fillna(inplace=True, method="pad")
            data.fillna(inplace=True, value=0)
            file_name = "tmp/covid/" + country + ".csv"
            data.to_csv(file_name, index=None, mode='w', encoding='utf-8-sig')
        else:
            print("没有关于" + country + "的数据文件")


def separate_covid_data_by_date(dates, country_list_u):
    """
    对于每个日期，遍历所有的国家，找出对应的当天的全部数据
    :param dates: 日期列表
    :param country_list_u: 国家列表
    :return: 不返回数据，结果存储在data/covid
    """
    for date in dates:
        date_tmp = date.replace('/', '-')
        file_name = "data/covid/" + date_tmp + ".csv"
        csv_file = open(file_name, 'w', newline="", encoding="utf-8-sig")
        writer = csv.writer(csv_file)
        # 新文件的字段属性，不要更改对应的顺序
        writer.writerow(["confirmed", "n_confirmed", "death",
                         "n_death", "cured", "n_cured", "country"])
        for country in country_list_u:
            data = pd.read_csv(
                open(os.path.join("tmp/covid", country + ".csv"), 'r', encoding='utf-8'),
                index_col="Updated", dtype=np.object)
            try:
                # 如果找到当天的数据，就存储，否则跳过该文件
                item = data.loc[date]
                writer.writerow(item)
            except KeyError as ke:
                continue
        csv_file.close()
        print(date)


# 将数据转化为指定格式
# 不返回结果
# 将格式化好的数据存放在data/covid_result.json中
def format_data(dates, country_list_u):
    DATA = []
    for date in dates:
        date_tmp = date.replace("/", "-")
        print("data/covid/" + date_tmp + ".csv")
        csv_file = pd.read_csv("data/covid/" + date_tmp + ".csv",
                               index_col="country", dtype=np.object)
        covid_data = []
        for country in country_list_u:
            try:
                covid_data_list = csv_file.loc[country].tolist()
                covid_data_list.append(country)
                covid_data_dic = {"name": country, "value": covid_data_list}
            except KeyError:
                covid_data_dic = {"name": country, "value": [0, 0, 0, 0, 0, 0, country]}
            else:
                covid_data.append(covid_data_dic)
        item = {"time": date, "data": covid_data}
        DATA.append(item)
    result = open("data/covid_result.json", mode='w')
    result.write(json.dumps(DATA))
    result.close()


country_list = statistics_country_list(source)
# print("statistics_country_list")
separate_source(source, country_list)
# print("separate_source")
separate_covid_data(country_list)


# print("separate_covid_data")
# 统计到目前为止有多少日期

# country_list = pd.read_csv("data/country_list.csv")["country"]


# get_covid_data(date_list, country_list)
# format_data(date_list,country_list)


# 获取国家列表
# 返回国家列表
def get_country_list(date):
    COUNTRYLIST = []
    date_tmp = date.replace("/", "-")
    file = pd.read_csv(
        open(os.path.join("data/covid/", date_tmp + ".csv"), 'r', encoding='utf-8'),
        dtype=np.object)
    for index in range(0, file.shape[0]):
        item = file.iloc[index]
        item.fillna(0)
        print(item)
        confirmed = int(item["confirmed"])
        print(confirmed)
        death = int(item["death"])
        print(death)
        cured = int(item["cured"])
        print(cured)
        country = item["country"]
        # number = confirmed + cured + death
        # item = {"name": country, "number": number}
        # COUNTRYLIST.append(item)
    return COUNTRYLIST

# print(get_country_list('06/25/2020'))



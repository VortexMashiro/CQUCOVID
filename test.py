import get
import os
import pandas as pd
import datetime
from pyecharts import options as opts
from pyecharts.charts import Line, Pie, TreeMap, Page


def get_confirmed_pre(country):
    file_name = "prediction_data/" + country + ".csv"
    if os.path.isfile(file_name):
        data = pd.read_csv(file_name, encoding="utf-8")
        confirmed = []
        for index in range(0, data.shape[0]):
            confirmed.append(int(data.iloc[index]))
        return confirmed
    else:
        return None


def paint_country_summary_chart(country):
    date_data, confirmed_data, death_data = get.get_country_epidemic_summary(country)
    date_data1, new_confirmed_data, new_death_data = get.get_new_confirmed_deaths(country)

    predict_data = get_confirmed_pre(country)

    day = date_data[-1]
    temp = day.split('/')
    today = datetime.date(int(temp[2]), int(temp[0]), int(temp[1]))
    for i in range(1, int(len(predict_data)) - int(len(date_data))+1):
        today = today + datetime.timedelta(days=1)
        date_data.append(today.strftime('%m/%d/%Y'))
        confirmed_data.append(None)
        death_data.append(None)
        new_confirmed_data.append(None)
        new_death_data.append(None)

    charts = (
        Line()
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
            .add_xaxis(xaxis_data=date_data)
            .add_yaxis(
            series_name="累计确诊",
            y_axis=confirmed_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="累计死亡",
            y_axis=death_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="新增确诊",
            y_axis=new_confirmed_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="新增死亡",
            y_axis=new_death_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="预测累计确诊",
            y_axis=predict_data,
            symbol="emptyCircle",
            is_symbol_show=True,
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                subtitle="",
                pos_left="3%",
                pos_top="10",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=22,
                )
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(
                pos_left="center",
                textstyle_opts=opts.TextStyleOpts(
                    font_size=15,
                )
            ),
            axispointer_opts=opts.AxisOpts(
                min_interval=100,
            ),
            datazoom_opts=[
                opts.DataZoomOpts(is_show=False, range_start=0, range_end=100),
                opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
                opts.DataZoomOpts(pos_top='92%')
            ],
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )

    return charts



c = paint_country_summary_chart('China')
c.render('test.html')
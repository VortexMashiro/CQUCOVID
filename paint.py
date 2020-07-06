from pyecharts.commons.utils import JsCode

import get
from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Pie, Timeline, Map, Grid
from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts


def paint_country_summary(country):
    date_data, confirmed_data, death_data = get.get_country_epidemic_summary(country)

    charts = (
        Line(init_opts=opts.InitOpts(width="100%", height="400px"))
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
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="扩散趋势",
                subtitle="",
                pos_left="left",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=30,
                )
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(
                pos_left="center",
                textstyle_opts=opts.TextStyleOpts(
                    font_size=20,
                )
            ),
            axispointer_opts=opts.AxisOpts(
                min_interval=100,
            ),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=0, range_end=100),
                opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
            ],
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(type_="value"),
        )
    )

    return charts


def paint_confirmedchange_deathchange(country):
    date_data, new_confirmed_data, new_death_data = get.get_new_confirmed_deaths(country)

    charts = (
        Bar(
            init_opts=opts.InitOpts(
                width="100%",
                height="400px",
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000,
                    animation_easing="elasticOut",
                )
            )
        )
            .add_xaxis(date_data)
            .add_yaxis("新增确诊", new_confirmed_data)
            .add_yaxis("新增死亡", new_death_data)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="新增确诊数及死亡数"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
            legend_opts=opts.LegendOpts(selected_mode='single')
        )
    )

    return charts


def paint_confirmed_distributed(country, date):
    result = get.get_confirmed_distribution(country, date)

    for i in result:
        i.reverse()

    charts = (
        Pie(init_opts=opts.InitOpts(width="50%", height="500px"))
            .add(
            "",
            result,
            color=['#e4c6d0', '#cca4e3', '#4c8dae', '#56004f', '#003371', '#8d4bbb', '#425066', '#4a4266', '#3b2e7e',
                   '#2e4e7e', '#a1afc9', '#4b5cc4',
                   '#003472', '#065279', '#177cb0', '#1685a9', '#3eede7', '#70f3ff', '#00e09e', '#a4e2c6', '#549688',
                   '#789262', '#827100', '#ae7000',
                   '#c89b40', '#e29c45', '#eedeb0', '#e9bb1d', '#ffa631', '#fa8c35', '#ff7500', '#f9906f', '##9d2933'],
            radius=[0, 150],
            center=["40%", "60%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="累计确诊分布"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
        )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    return charts


def paint_confirmedchange_top5(country, date):
    result = get.get_new_confirmed_top5(country, date)

    x_data = result[0]
    y_data = result[1]

    charts = (
        Bar(init_opts=opts.InitOpts(width="100%", height="400px"))
            .add_xaxis(x_data)
            .add_yaxis('', y_data)
            .set_global_opts(title_opts=opts.TitleOpts(title="新增确诊最多的地区", subtitle=""))
    )

    return charts


def paint_regional_details(country, date):
    max_data, min_data, result = get.get_country_epidemic(date, country)

    for i in result:
        temp = i.pop()
        i.insert(0, temp)

    table = Table()

    headers = ["地区", "累计确诊", "新增确诊", "累计死亡", "累计治愈"]
    rows = result
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="统计数据（按地区)")
    )
    table.render("table_base.html")


def get_week_chart(date: str):
    date_list = get.get_date_list()
    confirmed = get.get_world_confirmed()

    maxNum, minNum, map_data = get.get_time_axis_data(date)
    min_data, max_data = (minNum, maxNum)
    data_mark: List = []
    i = 0
    for x in date_list:
        if x == date:
            data_mark.append(confirmed[i])
        else:
            data_mark.append("")
        i = i + 1
    date_part = date.split("/")
    map_title = str(date_part[2]) + "年" \
                + str(date_part[0]) + "月" \
                + str(date_part[1]) + "日累计确诊量（人）"
    map_chart = (
        Map()
            .add(
            maptype="world",
            series_name="",
            data_pair=map_data,
            zoom=1,
            center=[10, 0],
            is_map_symbol_show=False,
            tooltip_opts= opts.TooltipOpts(
                formatter= "{b}:{c}"
            ),
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                },
            },
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=map_title,
                subtitle="",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[2] + ': ' + params.data.value[0];
                    }
                }"""
                ),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                orient='horizontal',
                dimension=0,
                pos_left="50",
                pos_top="20%",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False)
        )
    )

    line_chart = (
        Line()
            .add_xaxis(date_list)
            .add_yaxis("", confirmed)
            .add_yaxis(
            "",
            data_mark,
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )

            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="世\n界\n累\n计\n确\n诊\n折\n线\n图", pos_left="44%", pos_top="75%"
            )
        )
    )
    bar_x_data = [x[0] for x in map_data]
    bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
    bar = (
        Bar()
            .add_xaxis(xaxis_data=bar_x_data)
            .add_yaxis(
            series_name="",
            y_axis=bar_y_data,
            bar_width='5%',
            bar_min_width='3%',
            label_opts=opts.LabelOpts(
                is_show=True, position="right", formatter="{b} : {c}"
            ),
        )
            # .reversal_axis()
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=maxNum, axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="80",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    grid_chart = (
        Grid()
            .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="15", pos_right="70%", pos_top="30%", pos_bottom="15"
            ),
        )
            .add(
            line_chart,
            grid_opts=opts.GridOpts(
                pos_left="50%", pos_right="100", pos_top="70%", pos_bottom="30"
            ),
        )
            .add(map_chart, grid_opts=opts.GridOpts())
    )

    return grid_chart

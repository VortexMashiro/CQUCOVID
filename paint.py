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


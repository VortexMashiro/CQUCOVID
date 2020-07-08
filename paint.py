from pyecharts.commons.utils import JsCode

import get
from pyecharts import options as opts
from pyecharts.charts import Line, Pie, TreeMap, Page
from pyecharts.components import Image
from pyecharts.options import ComponentTitleOpts


def paint_country_summary_chart(country):
    date_data, confirmed_data, death_data = get.get_country_epidemic_summary(country)
    date_data1, new_confirmed_data, new_death_data = get.get_new_confirmed_deaths(country)

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

def paint_confirmed_distributed_chart(country):
    date = get.get_today()
    result = get.get_confirmed_distribution(country, date)

    if result:
        charts = (
            Pie()
                .add(
                "",
                result,
                radius=[60, 160],

            )
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="累计确诊分布",
                    pos_left="3%",
                    pos_top="10",
                    title_textstyle_opts=opts.TextStyleOpts(
                        font_size=22,
                    )
                ),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left='80%', pos_top='20%', orient="vertical"),
            )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)", font_size=15, ))
        )

        return charts

    else:
        data = get.get_word_epidemic(date)[2]
        flag = False
        for index in range(0,len(data)):
            if data[index][0] == country:
                data = data[index][1][0]
                flag = True
                break

        if not flag:
            title_charts = (
                Pie()
                    .add(
                    "",
                    [[country, -1]],
                    radius=[0, 0],
                    center=['100%', '100%']
                )
                    .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="暂无数据",
                        pos_left="40%%",
                        pos_top="44%",
                        title_textstyle_opts=opts.TextStyleOpts(
                            font_size=30,
                        )
                    ),
                    legend_opts=opts.LegendOpts(is_show=False),
                )
                    .set_series_opts(label_opts=opts.LabelOpts(is_show=False ))
            )
            return title_charts

        draw_data = [[country, data]]

        empty_charts = (
            Pie()
                .add(
                "",
                draw_data,
                radius=[60, 160],
                # center=['50%', '65%']
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="确诊人数",
                    pos_left="3%",
                    pos_top="10",
                    title_textstyle_opts=opts.TextStyleOpts(
                        font_size=22,
                    )
                ),
                legend_opts=opts.LegendOpts(type_="scroll", pos_left='80%', pos_top='20%', orient="vertical"),
            )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)", font_size=15, ))
        )

    return empty_charts



def paint_treemap():
    data = get.get_treemap_data(get.get_today())
    charts = (
        TreeMap(init_opts=opts.InitOpts(width="80%", height="400%"))
            .add("world",
            data=data["children"],
            label_opts=opts.LabelOpts(position="inside"),
        )
            .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=True),
            title_opts=opts.TitleOpts(
                title="世界累计确诊分布", pos_left="leafDepth"
            ),
        )
    )
    return charts

def paint_together(country = 'China'):
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        paint_country_summary_chart(country),
        paint_confirmed_distributed_chart(country),
        paint_treemap(),
    )
    return page.dump_options_with_quotes()



def paint_tree(country = 'Worldwide'):
    return paint_treemap().dump_options_with_quotes()
def paint_line(country = 'Worldwide'):
    return paint_country_summary_chart(country).dump_options_with_quotes()
def paint_pie(country = 'Worldwide'):
    return paint_confirmed_distributed_chart(country).dump_options_with_quotes()



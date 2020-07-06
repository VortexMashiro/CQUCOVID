from cqu_covid import app
# from pyecharts import Scatter3D #this will not work because its pyecharts 0.5 version's approach , do check latest doc(http://pyecharts.org/#/zh-cn/basic_charts)
# (stupid origin 0.5 doc is here : https://05x-docs.pyecharts.org/#/zh-cn/flask)

# from flask import Flask (have done in __init__)

from random import randrange
import json
from flask import render_template, request
from flask import jsonify

from pyecharts import options as opts
# from pyecharts.charts import Bar

import get
import paint

from pyecharts.charts import Map, Geo, MapGlobe

from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line, Geo
from pyecharts.faker import Faker

from pyecharts.globals import WarningType

WarningType.ShowWarning = False  # https://github.com/pyecharts/pyecharts/issues/1638
# IMPORTANT : ALL CODE SHOULD FOLLOW THIS DOC : http://pyecharts.org/#/zh-cn/web_flask

#######GDP DEMO #########
date_list = get.get_date_list()[0::7]

confirmed = get.get_world_confirmed()

maxNum = 7711
minNum = 1


def get_year_chart(date: str):
    maxNum,minNum,map_data = get.get_time_axis_data(date)
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
                dimension=0,
                pos_left="40",
                pos_top="10%",
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
                title="世\n界\n累\n计\n确\n诊\n折\n线\n图", pos_left="44%", pos_top="70%"
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
            bar_min_width='10',
            label_opts=opts.LabelOpts(
                is_show=True, position="right", formatter="{b} : {c}"
            ),
        )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=maxNum, axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                orient='horizontal',
                dimension=0,
                pos_left="10",
                pos_top="top",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    # pie_data = [[x[0], x[1][0]] for x in map_data]
    # pie = (
    #     Pie()
    #         .add(
    #         series_name="",
    #         data_pair=pie_data,
    #         radius=["15%", "35%"],
    #         center=["80%", "82%"],
    #         itemstyle_opts=opts.ItemStyleOpts(
    #             border_width=1, border_color="rgba(0,0,0,0.3)"
    #         ),
    #     )
    #         .set_global_opts(
    #         tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
    #         legend_opts=opts.LegendOpts(is_show=False),
    #     )
    # )

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
            # .add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
            .add(map_chart, grid_opts=opts.GridOpts())
    )

    return grid_chart


@app.route('/')
def target():
    page_name = "COVID-MAP"
    return render_template('loading.html', messager_data=page_name)


@app.route('/covid')  # GDP demo
def get_index():
    # msg_data = "No data was passed"
    # print(data)
    # print(time_list)
    # print(request.args.to_dict(flat=False))
    # if request.args.to_dict(flat=False)['data'][0]:
    #     msg_data = str(request.args.to_dict(flat=False)['data'][0])

    timeline = Timeline(
        # init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK)
        init_opts=opts.InitOpts(width="100vw", height="100vh", theme=ThemeType.DARK)
    )

    for day in date_list:
        g = get_year_chart(date=day)
        timeline.add(g, time_point=day)

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=2000,
        pos_left="null",
        pos_right="20",
        pos_top="10",
        pos_bottom="10",
        width="60",
        label_opts=opts.LabelOpts(is_show=False, color="#fff"),
    )
    # timeline.render("china_gdp_from_1993_to_2018.html")
    return render_template(
        "demo.html",
        # passed_data=msg_data,
        myechart=timeline.render_embed(),
    )

######GDP DEMO END############

@app.route('/home')
def get_home_page():
    # Global_map = (
    #     Geo(init_opts=opts.InitOpts(width="100%", height="100%", theme=ThemeType.DARK))
    #         .add_schema(
    #         maptype="world")  # https://github.com/pyecharts/pyecharts/blob/master/pyecharts/datasets/map_filename.json
    #         .add("geo", [["上海",100],["西藏",100]])  # TODO Data Interface
    #         .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    #         .set_global_opts(
    #         visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title="TITLE")
    #     )
    #
    # )
    #
    # print(str(Global_map.js_dependencies.items))
    # print(str(Global_map.js_dependencies._values))

    countrylist = [{"name": "China", "number": 11}, {"name": "Japan", "number": 12}]
    countrylist_tmp = get.get_country_list_with_data()
    if countrylist_tmp:
        countrylist = countrylist_tmp
    global_status = {'total': '10,512,383',
                     'total_today': '17,364',
                     'confirm_total': '5,387,249',
                     'confirm_today': '15,676',
                     'recover_total': '5,387,249',
                     'recover_today': '15,676',
                     'death_total': '5,387,249',
                     'death_today': '15,676'}
    global_status_temp = get.get_country_status('Worldwide')
    if global_status_temp:
        global_status = global_status_temp
    return render_template(
        "home.html",
        countrylist=countrylist,
        # myechart=Global_map.render_embed(),# this is being replaced with AJAX
        global_status=global_status,
        data_date=str(get.get_today())
    )
    # return charts.render_embed()


@app.route("/getGlobalMap", methods=['GET'])
def get_global_map():
    country_name = json.loads(request.args.get('data', type=str))['name']
    center = None
    zoom = 1
    if country_name != 'Worldwide':
        with open('weizhi.json', 'r') as f:
            json_dict = json.load(f)
            if country_name in json_dict:
                center = json_dict.get(country_name)
                zoom = 5
    max_data, min_data, map_data = get.get_word_epidemic(get.get_today())
    symbol_size = 12
    Global_map = (
        Geo(init_opts=opts.InitOpts(width="100%", height="100%", theme=ThemeType.DARK))
            .add_schema(
            maptype="world",
            center=center,
            zoom=zoom)  # https://github.com/# pyecharts/pyecharts/blob/master/pyecharts/datasets/map_filename.json
            .add_coordinate_json('weizhi.json')
            .add("geo", map_data)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                type_="size",
                is_calculable=True,
                # range_size=[10, 100],
                min_=min_data,
                max_=max_data,
                dimension=0
                # pos_left="600", #javascript will do this.
                # pos_top="400",
                # range_text=["High", "Low"],
                # range_color=["lightskyblue", "yellow", "orangered"],
                # textstyle_opts=opts.TextStyleOpts(color="#ddd"),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter="""
                function(parameter){
                var tool_tip =
                parameter.name+
                "<br/>累计确诊：" + parameter.value[2][0] +
                "<br/>累计死亡："+parameter.value[2][1]+
                 "<br/>累计治愈："+parameter.value[2][2];
                return tool_tip;
                }
                """
            ),
            title_opts=opts.TitleOpts(title=country_name)
        )
    )
    # charts = paint.paint_world_map()
    return Global_map.dump_options_with_quotes()


# When user clicks a country in countrylist, ask here to get a line pyecharts.
@app.route("/getConuntryBar", methods=['GET'])
def get_country_chart():
    print("get a ajax GET request.")
    country_name = json.loads(request.args.get('data', type=str))['name']
    date_list, n_confirmed_list, deaths = get.get_country_epidemic_summary(country_name)
    c = (
        Bar()
            .add_xaxis(date_list)
            .add_yaxis("累计确诊", n_confirmed_list)
            .add_yaxis("累计死亡", deaths)
            .set_global_opts(title_opts=opts.TitleOpts(title=country_name),
                             legend_opts=opts.LegendOpts(pos_bottom=5),
                             yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=90)))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    return c.dump_options_with_quotes()


@app.route("/getCountryStatus", methods=['GET'])
def get_country_status():
    country_name = json.loads(request.args.get('data', type=str))['name']
    country_status = {'total': '10,512,383',
                      'total_today': '17,364',
                      'confirm_total': '5,387,249',
                      'confirm_today': '15,676',
                      'recover_total': '5,387,249',
                      'recover_today': '15,676',
                      'death_total': '5,387,249',
                      'death_today': '15,676'}
    country_status_tmp = get.get_country_status(country_name)
    if country_status_tmp:
        country_status = country_status_tmp
    return jsonify(country_status)


@app.route('/news')
def get_news():
    return render_template(
        'news.html'
        # newslist=newslist
        # TODO  News related, format:  [{'title'=title,'des'=des,'date'=date,'author'=author},...]
    )


# @app.route("/getGlobalMap3D", methods=['GET'])
@app.route("/getGlobalMap3D")
def get_global_map3D():
    # country_name = json.loads(request.args.get('data', type=str))['name']
    max_data, min_data, map_data = get.get_word_epidemic(get.get_today())
    # map_data : [["Canada",[1,2,3]],...]
    symbol_size = 12
    Global_map = (
        MapGlobe(init_opts=opts.InitOpts(width="100%", height="100%", theme=ThemeType.DARK))
            .add_schema(
            maptype="world"
        )
            .add("geo", map_data)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(

            visualmap_opts=opts.VisualMapOpts(
                type_="size",
                is_calculable=True,
                dimension=0,
                range_size=[5, 1000],
                min_=min_data,
                max_=max_data,
                # pos_left="600", #javascript will do this.
                # pos_top="400",
                # range_text=["High", "Low"],
                # range_color=["lightskyblue", "yellow", "orangered"],
                # textstyle_opts=opts.TextStyleOpts(color="#ddd"),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter="""
                    function(parameter){
                    var tool_tip =
                    parameter.name+
                    "<br/>累计确诊：" + parameter.value[2][0] +
                    "<br/>累计死亡："+parameter.value[2][1]+
                     "<br/>累计治愈："+parameter.value[2][2];
                    return tool_tip;
                    }
                    """
            ),
            # title_opts=opts.TitleOpts(title=country_name)
        )
    )
    return Global_map.render_embed()

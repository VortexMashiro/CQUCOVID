from cqu_covid import app
# from pyecharts import Scatter3D #this will not work because its pyecharts 0.5 version's approach , do check latest doc(http://pyecharts.org/#/zh-cn/basic_charts)
# (stupid origin 0.5 doc is here : https://05x-docs.pyecharts.org/#/zh-cn/flask)

# from flask import Flask (have done in __init__)

import json
from flask import render_template, request
from flask import jsonify

from pyecharts import options as opts

import get
import paint

from pyecharts.charts import Map, Geo, MapGlobe

from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Line, Geo

from pyecharts.globals import WarningType

WarningType.ShowWarning = False  # https://github.com/pyecharts/pyecharts/issues/1638
# IMPORTANT : ALL CODE SHOULD FOLLOW THIS DOC : http://pyecharts.org/#/zh-cn/web_flask

#######TIME LINE #########
date_list = get.get_date_list()[0::7]

confirmed = get.get_world_confirmed()[0::7]


def get_week_chart(date: str):
    maxNum,minNum,map_data = get.get_time_axis_data(date)
    min_data, max_data = (minNum, maxNum)
    data_mark = []
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
                pos_left="20",
                pos_top="25%",
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
                title="世\n界\n累\n计\n确\n诊\n折\n线\n图", pos_left="43%", pos_top="70%"
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
            .reversal_axis()
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=maxNum, axislabel_opts=opts.LabelOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="20",
                pos_top="20%",
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
                pos_left="15", pos_right="60%", pos_top="50%", pos_bottom="15"
            ),
        )
            .add(
            line_chart,
            grid_opts=opts.GridOpts(
                pos_left="48%", pos_right="100", pos_top="70%", pos_bottom="30"
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

    timeline = Timeline(
        # init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK)
        init_opts=opts.InitOpts(width="100vw", height="100vh", theme=ThemeType.DARK)
    )

    for day in date_list:
        g = get_week_chart(date=day)
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

######TIME LINE END############


########## HOME PAGE ########
@app.route('/home')
def get_home_page():

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
            zoom=zoom)
            .add_coordinate_json('weizhi.json')
            .add(series_name="geo", data_pair =  map_data)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                is_show=True,
                type_="size",
                is_calculable=True,
                range_size=[10, 100],
                min_= min_data,
                max_= max_data,
                dimension=3
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

##############HOMW PAGE##########################


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

from cqu_covid import app
#from pyecharts import Scatter3D #this will not work because its pyecharts 0.5 version's approach , do check latest doc(http://pyecharts.org/#/zh-cn/basic_charts) 
# (stupid origin 0.5 doc is here : https://05x-docs.pyecharts.org/#/zh-cn/flask)

# from flask import Flask (have done in __init__)

from random import randrange
import json
from flask import render_template,request

from pyecharts import options as opts
# from pyecharts.charts import Bar


from pyecharts.charts import Map,Geo


from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line,Geo
from pyecharts.faker import Faker

from pyecharts.globals import WarningType
WarningType.ShowWarning = False#https://github.com/pyecharts/pyecharts/issues/1638
#IMPORTANT : ALL CODE SHOULD FOLLOW THIS DOC : http://pyecharts.org/#/zh-cn/web_flask

#######GDP DEMO #########

f = open('data/covid_result.json', 'r')
content = f.read()
data = json.loads(content)
f.close()

time_list = [str(d) + "年" for d in range(1993, 2019)]


total_num = [
    3.4,
    4.5,
    5.8,
    6.8,
    7.6,
    8.3,
    8.8,
    9.9,
    10.9,
    12.1,
    14,
    16.8,
    19.9,
    23.3,
    28,
    33.3,
    36.5,
    43.7,
    52.1,
    57.7,
    63.4,
    68.4,
    72.3,
    78,
    84.7,
    91.5,
]
maxNum = 97300
minNum = 0


def get_year_chart(year: str):
    map_data = [
        [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == year
    ][0]
    min_data, max_data = (minNum, maxNum)
    data_mark: List = []
    i = 0
    for x in time_list:
        if x == year:
            data_mark.append(total_num[i])
        else:
            data_mark.append("")
        i = i + 1

    map_chart = (
        Map()
        .add(
            series_name="",
            data_pair=map_data,
            zoom=1,
            center=[119.5, 34.5],
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
                title="" + str(year) + "全国分地区GPD情况（单位：亿） 数据来源：国家统计局",
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
                pos_left="30",
                pos_top="center",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),
        )
    )

    line_chart = (
        Line()
        .add_xaxis(time_list)
        .add_yaxis("", total_num)
        .add_yaxis(
            "",
            data_mark,
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="全国GDP总量1993-2018年（单位：万亿）", pos_left="72%", pos_top="5%"
            )
        )
    )
    bar_x_data = [x[0] for x in map_data]
    bar_y_data = [{"name": x[0], "value": x[1][0]} for x in map_data]
    bar = (
        Bar()
        .add_xaxis(xaxis_data=bar_x_data)
        .add_yaxis(
            "",
            bar_y_data,
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

    pie_data = [[x[0], x[1][0]] for x in map_data]
    pie = (
        Pie()
        .add(
            series_name="",
            data_pair=pie_data,
            radius=["15%", "35%"],
            center=["80%", "82%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    grid_chart = (
        Grid()
        .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"
            ),
        )
        .add(
            line_chart,
            grid_opts=opts.GridOpts(
                pos_left="65%", pos_right="80", pos_top="10%", pos_bottom="50%"
            ),
        )
        .add(pie, grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
        .add(map_chart, grid_opts=opts.GridOpts())
    )

    return grid_chart

@app.route('/')
def target():
    page_name = "COVID-MAP"
    return render_template('loading.html', messager_data=page_name)

@app.route('/covid')#GDP demo
def get_index():
    msg_data = "No data was passed"
    if request.args.to_dict(flat=False)['data'][0]:
        msg_data = str(request.args.to_dict(flat=False)['data'][0])

    timeline = Timeline(
        #init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.DARK)
        init_opts=opts.InitOpts(width="100vw",height="100vh" ,theme=ThemeType.DARK)
    )
    for y in time_list:
        g = get_year_chart(year=y)
        timeline.add(g, time_point=str(y))

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )
    #timeline.render("china_gdp_from_1993_to_2018.html")
    return render_template(
        "demo.html",
        passed_data = msg_data,
        myechart=timeline.render_embed(),
    )

######GDP DEMO END############

@app.route('/home')
def get_home_page():
    Global_map = (
        Geo(init_opts=opts.InitOpts(width="100vw",height="100vh" ,theme=ThemeType.DARK))
        .add_schema(maptype="world")#https://github.com/pyecharts/pyecharts/blob/master/pyecharts/datasets/map_filename.json
        .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])#TODO Data Interface
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title="TITLE")
        )
    
    )


    countrylist=[{"name": "China", "number": 11},{"name": "Japan", "number": 12}]#TODO Data Interface
    return render_template(
        "home.html",
        countrylist=countrylist,
        myechart=Global_map.render_embed()
    )

#When user clicks a country in countrylist, ask here to get a line pyecharts.
@app.route("/getConuntryBar",methods=['GET'])
def get_bar_chart():
    print("get a ajax GET request.")
    country_name= json.loads(request.args.get('data', type=str))['name']

    c = (#TODO, a correct corresponding graph with the country_name is required.
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title=country_name, subtitle="我是副标题"))
    )
    return c.dump_options_with_quotes()
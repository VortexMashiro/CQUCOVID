import  get
from pyecharts import options as opts
from pyecharts.charts import Map

def paint_world_map(country_name):
    max_data, min_data, result = get.get_word_epidemic('05/25/2020')

    max_data = int(max_data)
    min_data = int(min_data)

    map_data = []
    for i in result:
        i = i[1::3]
        i.reverse()
        i[1] = int(i[1])
        map_data.append(i)
    map_data = map_data[1:]

    map_chart = (
        Map(init_opts=opts.InitOpts(width="150%", height="1000px"))
            .add(
            series_name="",
            data_pair=map_data,
            maptype='world',
            zoom=1,
            center=[116.419, 5],
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {"areaColor": "rgba(255,255,255, 0.5)"},
            },
        )

            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))

            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=country_name,
                subtitle="",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25,
                    color="rgba(255,255,255, 0.9)"
                ),
            ),

            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger='item',
                hide_delay=200,
                background_color='#fffbf0',
                border_color='#75878a',
                border_width=2,
                    formatter='<span style="color: black; font-size: 15px; font-family: courier-new; display:inline-block; width:120px; text-align: center"><b>{b}</b></span><br>\
                                <hr>\
                                <span style="font-size: 15px; color: red">累计确诊&nbsp;&nbsp;&nbsp;{c0}</span>'
                # #                 <br><hr>\
                # #                 <span style="font-size: 12px; color: black">现有确诊&nbsp;&nbsp;&nbsp;{c}</span><br>\
                # #                 <span style="font-size: 12px; color: black">累计治愈&nbsp;&nbsp;&nbsp;{c}</span><br>\
                # #                 <span style="font-size: 12px; color: black">累计死亡&nbsp;&nbsp;&nbsp;{@[2]}</span>'
            ),

            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="30",
                pos_top="bottom",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data,
            ),

        )
    )

    return map_chart



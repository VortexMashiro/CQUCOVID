from cqu_covid import app
#from pyecharts import Scatter3D #this will not work because its pyecharts 0.5 version's approach , do check latest doc(http://pyecharts.org/#/zh-cn/basic_charts) 
# (stupid origin 0.5 doc is here : https://05x-docs.pyecharts.org/#/zh-cn/flask)

# from flask import Flask (have done in __init__)

from random import randrange
from flask import render_template

from pyecharts import options as opts
from pyecharts.charts import Bar

#IMPORTANT : ALL CODE SHOULD FOLLOW THIS DOC : http://pyecharts.org/#/zh-cn/web_flask

@app.route('/')
def index():
    return app.config['TITLE'] #pure backend mode.


def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

@app.route("/test")#handler for http request
def test():
    return render_template("pyechart_test.html")#separation mode.


@app.route("/barChart")#handler for the ajax request, but still available for http.
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()


#An half-separation mode example :
# def hello():
#     return render_template(
#         "pyecharts.html",
#         host=REMOTE_HOST,
#         script_list=s3d.get_js_dependencies(),
#     )
# Then use liquid language to get value.
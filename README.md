# CQUCOVID
![Build and deploy Python app to Azure Web App - cqu-covidmap](https://github.com/VortexMashiro/CQUCOVID/workflows/Build%20and%20deploy%20Python%20app%20to%20Azure%20Web%20App%20-%20cqu-covidmap/badge.svg)

---

COVID-19 Data Visualization

## How to run

1. cd into root
2. run `python -m pip install -r requirements.txt`
3. run`flask run`  or `py app.py`

Note: this will start flask in your local machine with debug mode: off , default URL is http://127.0.0.1:5000/.

Note: when using `flask run`, we are actually directly booting the server, which is the `cqu_covid` package. To boot with specific config, you can use `py app.py` to use custom python script to run the app. However, we recommend that build the config in `__init__.py`. 

## Package

The application is currently packed as a package `cqu_covid`. To import this package, pleause use `from from cqu_covid import app` , the file tree is :
```
├─cqu_covid
│  ├─static
│  ├─templates
│  └─`__init__.py`
└─`app.py`
```



1. Noticed that there's a loop import between `__init__.py` and `views.py` , this is fine in flask, but not recommended in python.  Please see https://dormousehole.readthedocs.io/en/latest/patterns/packages.html

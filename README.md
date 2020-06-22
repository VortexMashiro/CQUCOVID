# CQUCOVID
![CQUCOVIDCI](https://github.com/VortexMashiro/CQUCOVID/workflows/CQUCOVIDCI/badge.svg) 

---

COVID-19 Data Visualization

## How to run

1. cd into root
2. run `python -m pip install -r requirements.txt`
3. run`flask run`

Note: this will start flask in your local machine with debug mode: off , default URL is http://127.0.0.1:5000/.

## Package

The application is currently packed as a package `cqu_covid`. To import this package, pleause use `from from cqu_covid import app` , the file tree is :
├─cqu_covid
│  ├─static
│  ├─templates
│  └─`__init__.py`
└─`app.py`

##TODOs
1. Noticed that there's a loop import between `__init__.py` and `views.py` , this is fine in flask, but not recommended in python.  Please see https://dormousehole.readthedocs.io/en/latest/patterns/packages.html
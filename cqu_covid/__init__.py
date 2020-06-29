from flask import Flask
import config
# import yaml
app = Flask(__name__)
#app = Flask(__name__)
#init app config
# def read_yaml(yaml_file_path):
#     with open(yaml_file_path, 'rb') as f:
#         cf= yaml.safe_load(f.read()) 
#         #yaml.load(f.read())
#     return cf
# cf = read_yaml("_config.yaml")
# app.config.update(cf)
app.config.from_object(config) 
#import app modules
import cqu_covid.views
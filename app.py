from cqu_covid import app
import yaml
def read_yaml(yaml_file_path):
    with open(yaml_file_path, 'rb') as f:
        cf= yaml.safe_load(f.read()) # yaml.load(f.read())
    return cf
cf = read_yaml("_config.yaml")
app.config.update(cf)
app.run(debug = True)
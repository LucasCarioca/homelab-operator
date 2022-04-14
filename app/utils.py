import os

def get_template(version, template, type): 
    path = os.path.join(os.path.dirname(__file__), f"templates/{version}-{template}-{type}.yml")
    return open(path, 'rt').read()
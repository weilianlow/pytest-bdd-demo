import json
import yaml
from jsonpath_ng.ext import parse


def load_from_file(parse_type, file_path):
    f = open(file_path)
    if parse_type.lower() == "yaml":
        return yaml.safe_load(f)
    elif parse_type.lower() == "json":
        return json.load(f)
    else:
        raise ValueError("parse_type:{parse_type} not available")


def load_from_text(parse_type, text):
    if parse_type.lower() == "yaml":
        return yaml.safe_load(text)
    elif parse_type.lower() == "json":
        return json.loads(text)
    else:
        raise ValueError("parse_type:{parse_type} not available")


def get_json_path(jsonpath, json_data):
    jsonpath_expr = parse(jsonpath)
    return [match.value for match in jsonpath_expr.find(json_data)]

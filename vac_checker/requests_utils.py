import json
from urllib.request import urlopen


def get_json_data(url):
    # read json file from url
    with urlopen(url) as res:
        source = res.read()
    json_data = json.loads(source)
    return json_data


def get_json_data_from_file(filename):
    with open(filename, 'r') as f:
        json_data = json.load(f)
    return json_data

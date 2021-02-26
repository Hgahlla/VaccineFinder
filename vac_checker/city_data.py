import json
from urllib.request import urlopen
from geocoding import *


def get_json(url):
    # read json file from url
    with urlopen(url) as res:
        source = res.read()

    # json data
    data = json.loads(source)

    return data


def save_original_json(data):
    # Save the original json to a file
    with open('../data/covid-19-vaccine.vaccine-status.TX.json', 'w') as f:
        json.dump(data, f, indent=2)


def save_locations_part_from_json(data):
    # json object, 'TX'
    locations = data['responsePayloadData']['data']

    # renaming the json object, 'TX' to 'locations'
    locations['locations'] = locations.pop('TX')

    with open('locations.json', 'w') as f:
        json.dump(locations, f, indent=2)


def add_lat_long_to_locations():
    with open('locations.json') as f:
        data = json.load(f)

    for loc in data['locations']:
        # Convert city name to latitude and longitude
        coord = get_lat_long(loc['city'] + ', ' + loc['state'])

        # Add lat and long keys to json file
        loc['latitude'] = coord[0]
        loc['longitude'] = coord[1]

    # Save file with the lat and long
    with open('locations.json', 'w') as f:
        json.dump(data, f, indent=2)


def update_status_in_locations(new_data):
    # Store the values of the 'status' key from the new data
    new_status = []
    for loc in new_data['responsePayloadData']['data']['TX']:
        new_status.append(loc['status'])

    with open('locations.json') as f:
        old_data = json.load(f)

    # Update the old values with the new values
    for i, loc in enumerate(old_data['locations']):
        loc['status'] = new_status[i]

    # Save file with the lat and long
    with open('locations.json', 'w') as f:
        json.dump(old_data, f, indent=2)


def get_status():
    with open('locations.json') as f:
        data = json.load(f)

    avail_cities = []
    for loc in data['locations']:
        if loc['status'] == 'Available':
            avail_cities.append(loc['city'])

    return avail_cities

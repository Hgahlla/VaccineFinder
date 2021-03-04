import secret as s
from requests_utils import get_json_data
from database import Database
from location import Location
from travel import MapsClient
from notification import MessageClient
import datetime


# Populate the location database from the cvs pharmacy json data
def populate_location_db(data):
    count = Location.count_rows()
    if count == 0:
        for loc in data['responsePayloadData']['data']['TX']:
            # Convert city name to latitude and longitude
            lat, long = MapsClient.get_lat_long(loc['city'] + ', ' + loc['state'])
            Location.save_to_db(loc['city'], loc['state'], lat, long, loc['status'])
            print(loc['city'] + ", " + loc['state'], lat, long, loc['status'])


# Update the status of each location in the location database
def update_location_db(data):
    for loc in data['responsePayloadData']['data']['TX']:
        #print(loc['city'] + ", " + loc['state'], loc['status'])
        Location.update_status(loc['city'], loc['status'])


# Notify users of available locations within in certain drive time
def get_locations_within_travel_time(source, locations, hr, m):
    msg_client = MessageClient()
    lat, long = MapsClient.get_lat_long(source)
    for loc in locations:
        maps = MapsClient(lat, long, loc.latitude, loc.longitude)
        maps.get_route()

        if maps.get_duration() < datetime.timedelta(hours=hr, minutes=m):
            msg = f"{loc.city}, {loc.state}\n{maps.display_duration()}\n{maps.get_distance()} miles\n"
            print(msg)
            notification = msg_client.send_notification(msg)
            print(f"Message Successfully Sent ({notification.sid})")


# Calculate travel time and distance for all available locations
def calculate_travel_info(source, locations):
    lat, long = MapsClient.get_lat_long(source)
    for loc in locations:
        maps = MapsClient(lat, long, loc.latitude, loc.longitude)
        maps.get_route()
        maps.get_duration()
        print(f"{loc.city}, {loc.state}\n{maps.display_duration()}\n{maps.get_distance()} miles\n")


def main():
    url = "https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.TX.json"
    data = get_json_data(url)
    Database.initialise(host=s.host, database=s.database, user=s.user, password=s.password, port=s.port)

    populate_location_db(data)
    update_location_db(data)
    locations = Location.load_from_db_by_status('Available')
    get_locations_within_travel_time(s.source, locations, 0, 30)


if __name__ == '__main__':
    main()

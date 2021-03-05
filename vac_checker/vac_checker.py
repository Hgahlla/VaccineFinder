from requests_utils import get_json_data
from database import Database
from location import Location
from travel import MapsClient
from notification import MessageClient
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


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
        print(loc['city'] + ", " + loc['state'], loc['status'])
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


# Main function (Entry point for Google's Cloud Functions)
def vaccine_finder(request=None):
    # Pass arguments (hour & minute) to Google's Cloud Function
    if request is not None:
        request_json = request.get_json(silent=True)
        if request.args and 'hour' in request.args and 'minute' in request.args:
            hour = request.args.get('hour')
            minute = request.args.get('minute')
        elif request_json and 'hour' in request_json and 'minute' in request_json:
            hour = request_json['hour']
            minute = request_json['minute']
        else:
            hour = 0
            minute = 30
        Database.initialise(host=os.environ.get("GCP_HOST"), database=os.environ.get("DB_NAME"),
                            user=os.environ.get("DB_USERNAME"), password=os.environ.get("DB_PASSWORD"))
    # Run program locally
    else:
        hour = 0
        minute = 30
        Database.initialise(host=os.environ.get("PUBLIC_HOST"), database=os.environ.get("DB_NAME"),
                            user=os.environ.get("DB_USERNAME"), password=os.environ.get("DB_PASSWORD"),
                            port=int(os.environ.get("DB_PORT")))

    url = "https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.TX.json"
    data = get_json_data(url)
    populate_location_db(data)
    update_location_db(data)
    locations = Location.load_from_db_by_status('Available')
    get_locations_within_travel_time(os.environ.get("SOURCE"), locations, hour, minute)


if __name__ == '__main__':
    vaccine_finder()

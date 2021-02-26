import requests
import json
from geopy.geocoders import Nominatim
import datetime


# Convert city name to latitude and longitude
def get_lat_long(location):
    nom = Nominatim(user_agent="my_user_agent")
    loc = nom.geocode(location)
    coordinates = (loc.latitude, loc.longitude)
    return coordinates


def get_route(src_lat, src_long, dest_lat, dest_long):
    # Call the OSMR API
    res = requests.get(f"http://router.project-osrm.org/route/v1/car/{src_long},{src_lat};{dest_long},{dest_lat}?overview=false""")

    # Load the response with the json library
    # By default you get only one alternative so you access 0-th element of the `routes`
    routes = json.loads(res.content)
    route_1 = routes.get("routes")[0]

    return route_1


def get_travel_time(route):
    duration = datetime.timedelta(seconds=route["duration"])
    return duration


def display_travel_time(time):
    t = str(time).split(":")

    if t[0] != "0":
        return t[0] + " hr " + t[1] + " min"
    else:
        return t[1] + " min"


def get_travel_distance(route):
    miles = round(route["distance"] * 0.000621371192, 2)
    return miles


def travel_to_locations(home, hr, m):
    src = get_lat_long(home)
    src_lat, src_long = src[0], src[1]

    with open('locations.json') as f:
        data = json.load(f)

    out = open('travel_info.txt', 'w')

    for loc in data['locations']:
        route = get_route(src_lat, src_long, loc['latitude'], loc['longitude'])

        time = get_travel_time(route)

        if time < datetime.timedelta(hours=hr, minutes=m):
            print(loc['city'])
            print(display_travel_time(time))
            print(get_travel_distance(route), "miles\n")

            out.write(loc['city'] + "\n")
            out.write(display_travel_time(time) + "\n")
            out.write(str(get_travel_distance(route)) + " miles\n\n")

    out.close()


def get_travel_info(home, city):
    src = get_lat_long(home)
    src_lat, src_long = src[0], src[1]

    with open('locations.json') as f:
        data = json.load(f)

    out = open('travel_info_to_available_cities.txt', 'w')

    idx = 0
    for loc in data['locations']:
        if idx > len(city) - 1:
            break

        if city[idx] == loc['city']:
            route = get_route(src_lat, src_long, loc['latitude'], loc['longitude'])
            time = get_travel_time(route)

            print(loc['city'])
            print(display_travel_time(time))
            print(get_travel_distance(route), "miles\n")

            out.write(loc['city'] + "\n")
            out.write(display_travel_time(time) + "\n")
            out.write(str(get_travel_distance(route)) + " miles\n\n")
            idx += 1

    out.close()

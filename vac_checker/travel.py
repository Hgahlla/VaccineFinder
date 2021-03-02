import requests
import json
from geopy.geocoders import Nominatim
import datetime


class MapsClient:
    def __init__(self, src_lat, src_long, dest_lat, dest_long):
        self.src_lat = src_lat
        self.src_long = src_long
        self.dest_lat = dest_lat
        self.dest_long = dest_long
        self.route = None
        self.duration = None
        self.distance = None

    @classmethod
    def get_lat_long(cls, location):
        nom = Nominatim(user_agent="my_user_agent")
        loc = nom.geocode(location)
        lat, long = (loc.latitude, loc.longitude)
        return lat, long

    def get_route(self):
        # Call the OSMR API
        res = requests.get(
            f"http://router.project-osrm.org/route/v1/car/{self.src_long},{self.src_lat};{self.dest_long},{self.dest_lat}?overview=false""")

        # Load the response with the json library
        # By default you get only one alternative so you access 0-th element of the `routes`
        routes = json.loads(res.content)
        route_1 = routes.get("routes")[0]
        self.route = route_1
        return route_1

    def get_duration(self):
        duration = datetime.timedelta(seconds=self.route["duration"])
        self.duration = duration
        return duration

    def display_duration(self):
        t = str(self.duration).split(":")

        if t[0] != "0":
            return t[0] + " hr " + t[1] + " min"
        else:
            return t[1] + " min"

    def get_distance(self):
        miles = round(self.route["distance"] * 0.000621371192, 2)
        self.distance = miles
        return miles

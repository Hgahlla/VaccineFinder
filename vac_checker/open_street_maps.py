import requests
import json
from geopy.geocoders import Nominatim
import datetime


class OSMClient:
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
        response = requests.get(
            f"http://router.project-osrm.org/route/v1/car/{self.src_long},{self.src_lat};{self.dest_long},{self.dest_lat}?overview=false""")

        # Load the response with the json library
        # By default you get only one alternative so you access 0-th element of the `routes`
        routes = json.loads(response.content)
        self.route = routes.get("routes")[0]
        return self.route

    def get_duration(self):
        self.duration = datetime.timedelta(seconds=self.route["duration"])
        return self.duration

    def display_duration(self):
        t = str(self.duration).split(":")

        if t[0] != "0":
            return t[0] + " hr " + t[1] + " min"
        else:
            return t[1] + " min"

    def get_distance(self):
        self.distance = round(self.route["distance"] * 0.000621371192, 2)
        return self.distance

    def display_distance(self):
        return f"{self.distance} mi"

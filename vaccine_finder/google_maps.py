import requests
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class GoogleMapsClient:
    def __init__(self, origin, destination):
        self.GOOGLE_MAPS_API = os.environ.get("GOOGLE_MAPS_API")
        self.origin = origin
        self.destination = destination
        self.route = None
        self.duration = None
        self.distance = None

    def get_route(self):
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={self.origin}&destinations={self.destination}&units=imperial&key={self.GOOGLE_MAPS_API}")
        self.route = json.loads(response.content)
        return self.route

    def get_duration(self):
        seconds = self.route["rows"][0]["elements"][0]["duration"]["value"]
        self.duration = datetime.timedelta(seconds=seconds)
        return self.duration

    def display_duration(self):
        return self.route["rows"][0]["elements"][0]["duration"]["text"]

    def get_distance(self):
        self.distance = round(self.route["rows"][0]["elements"][0]["distance"]["value"] * 0.000621371192, 2)
        return self.distance

    def display_distance(self):
        return self.route["rows"][0]["elements"][0]["distance"]["text"]

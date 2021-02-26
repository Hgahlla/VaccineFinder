from city_data import *
from geocoding import *

def first_run():
    url = "https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.TX.json"
    data = get_json(url)
    save_locations_part_from_json(data)
    add_lat_long_to_locations()

def travel():
    # home address
    home = "3721 Goose Creek Pkwy"
    travel_to_locations(home, 0, 30)

def check_availability():
    url = "https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.TX.json"
    data = get_json(url)
    update_status_in_locations(data)

    avail_cities = get_status()

    # home address
    home = "3721 Goose Creek Pkwy"
    get_travel_info(home, avail_cities)


if __name__ == "__main__":
    #first_run()
    #travel()
    check_availability()
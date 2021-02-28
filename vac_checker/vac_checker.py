from city_data import get_json, get_status
from city_data import save_locations_part_from_json
from city_data import add_lat_long_to_locations
from city_data import update_status_in_locations
from geocoding import travel_to_locations
from geocoding import get_travel_info
import secret


def first_run():
    url = "https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.TX.json"
    data = get_json(url)
    save_locations_part_from_json(data)
    add_lat_long_to_locations()


def travel():
    # home address
    home = secret.home
    travel_to_locations(home, 1, 0)


def check_availability():
    url = "https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.TX.json"
    data = get_json(url)
    update_status_in_locations(data)

    avail_cities = get_status()

    # home address
    home = secret.home
    get_travel_info(home, avail_cities)


def main():
    first_run()
    travel()
    check_availability()


if __name__ == "__main__":
    main()

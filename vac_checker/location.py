from database import CursorFromConnectionPool


class Location:
    def __init__(self, city, state, latitude, longitude):
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude

    @classmethod
    def save_to_db(cls, city, state, lat, long, status):
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                "INSERT INTO location (city, state, latitude, longitude, status) VALUES (%s, %s, %s, %s, %s)",
                (city, state, lat, long, status))

    @classmethod
    def update_status(cls, city, status):
        with CursorFromConnectionPool() as cursor:
            cursor.execute("UPDATE location SET status = (%s) WHERE city = (%s) AND status <> (%s)",
                           (status, city, status))

    @classmethod
    def load_from_db_by_status(cls, status):
        with CursorFromConnectionPool() as cursor:
            # Note the (status,) to make it a tuple!
            cursor.execute("SELECT city, state, latitude, longitude FROM location WHERE status = (%s)", (status,))
            row = cursor.fetchall()
            data = []
            for city, state, lat, long in row:
                data.append(cls(city=city, state=state, latitude=lat, longitude=long))
            return data

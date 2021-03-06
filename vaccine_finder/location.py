from database import CursorFromConnectionPool


class Location:
    def __init__(self, city, state):
        self.city = city
        self.state = state

    @classmethod
    def count_rows(cls):
        with CursorFromConnectionPool() as cursor:
            cursor.execute("SELECT COUNT(location_id) FROM location")
            result = cursor.fetchone()
            return result[0]

    @classmethod
    def save_to_db(cls, city, state, status):
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                "INSERT INTO location (city, state, status) VALUES (%s, %s, %s)",
                (city, state, status))

    @classmethod
    def update_status(cls, city, status):
        with CursorFromConnectionPool() as cursor:
            cursor.execute("UPDATE location SET status = (%s) WHERE city = (%s) AND status <> (%s)",
                           (status, city, status))

    @classmethod
    def load_from_db_by_status(cls, status):
        with CursorFromConnectionPool() as cursor:
            # Note the (status,) to make it a tuple!
            cursor.execute("SELECT city, state FROM location WHERE status = (%s)", (status,))
            row = cursor.fetchall()
            data = []
            for city, state in row:
                data.append(cls(city=city, state=state))
            return data

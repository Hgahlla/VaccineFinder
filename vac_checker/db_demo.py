from database import Database
from database import Cursor

def save_to_db(emp_id, emp_name):
    with Cursor() as cursor:
        cursor.execute("INSERT INTO employees (id, name) VALUES (%s, %s)", (emp_id, emp_name))

if __name__ == '__main__':
    Database.initialise(host="localhost", database="test", user="postgres", password="happydb", port=5432)
    save_to_db(2222, "Conor")
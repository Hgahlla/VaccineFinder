import psycopg2

# connect to the db
con = psycopg2.connect(
    host="localhost",
    database="test",
    user="postgres",
    password="happydb",
    port=5432
)

# cursor
cur = con.cursor()

# insert
cur.execute("insert into employees (id, name) values (%s, %s)", (77, "Luka"))

# commit transaction
con.commit()

# execute query
cur.execute("select id, name from employees")

rows = cur.fetchall()

for id, name in rows:
    print(id, name)

# close cursor
cur.close()

# close the connection
con.close()
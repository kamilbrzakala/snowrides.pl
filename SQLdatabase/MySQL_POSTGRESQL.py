import json, sys

import psycopg2
sys.path.insert(0,r'C:\Users\PREZES\Desktop\snowridess\venv\lib\python3.6\site-packages')
import mysql.connector as conn
from pprint import pprint


### REITERATE JSON FILE AND CREATE ONE LIST WITH JSON
myjson = json.load(open(r'C:\Users\PREZES\Desktop\snowridess\venv\all_trips.json', encoding="utf8"))

db = []
temp_store_info = {}

for i in range(len(myjson)):
    for y in range(len(myjson[i])):
        # print(myjson[i][y]["City"])
        # print(myjson[i][y]["Country"])
        # print(myjson[i][y]["Date"])
        # print(myjson[i][y]["Price"])
        # print(myjson[i][y]["Free slots"])
        # print(myjson[i][y]["Link"])
        # print("\n")

        temp_store_info={
            'Organizator': myjson[i][y]["Organizator"],
            'City': myjson[i][y]["City"],
            'Country': myjson[i][y]["Country"],
            'Date': myjson[i][y]["Date"],
            'Price': myjson[i][y]["Price"],
            'Free slots': myjson[i][y]["Free slots"],
            'Link': myjson[i][y]["Link"]

        }
        db.append(temp_store_info)

with open(r'C:\Users\PREZES\Desktop\snowridess\venv\temp.json', 'w', encoding="utf8") as json_file:
    json.dump(db, json_file, indent=4,ensure_ascii=False)

#### MYSQL CONNECTION
conn = conn.connect(user='root', password='',
                              host='127.0.0.1',
                              database='trips')
cur = conn.cursor()


cur.execute("DROP TABLE TRIPS;")
# Create database:
try:
###Execute the SQL command
    cur.execute("CREATE TABLE trips (id int NOT NULL PRIMARY KEY AUTO_INCREMENT, organizator text, country text, city text, trip_date text, price text, "
            "free_slots text,  link text);")
# Commit your changes in the database
    conn.commit()
except:
## Rollback in case there is any error
    conn.rollback()

try:
    cur.executemany("""INSERT INTO trips(organizator, country, city, trip_date, price, free_slots, link)
                VALUES (%(Organizator)s,%(Country)s, %(City)s, %(Date)s, %(Price)s, %(Free slots)s, %(Link)s)""", db)
    conn.commit()
except:
    conn.rollback()

cur.execute("SELECT * FROM trips;")
print(cur.fetchall())
# close cursor object
cur.close()
# disconnect from server
conn.close()

######################## POSTGRESQL CONNECTOR ########################
#
# try:
#     conn = psycopg2.connect("dbname='postgres' user='postgres' password=''")
# except:
#     print("I am unable to connect to the database")
#
#
# cur = conn.cursor()
#
# cur.execute("CREATE TABLE test2 (id serial PRIMARY KEY, trip_date varchar, price varchar, free_slots varchar,"
#             " country varchar, city varchar, link varchar);")
#
# cur.executemany("""INSERT INTO test2(country, city, trip_date, price, free_slots, link)
#                 VALUES (%(Country)s, %(City)s, %(Date)s, %(Price)s, %(Free slots)s, %(Link)s)""", db)
#
# cur.execute("SELECT * FROM test2;")
# print(cur.fetchall())
# conn.commit()
# cur.close()
# conn.close()


#### REMOVE TEMP JSON FILE
# try:
#     os.remove('/Users/brzakkam/Documents/PyCharmProjects/SnowTripScrap/venv/Script/temp.html')
#     print("TEMP file has been removed")
# except OSError:
#     print(OSError)
#     pass

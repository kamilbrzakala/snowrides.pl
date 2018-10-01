import json, sys, csv

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
        print(myjson[i][y]["City"])
        print(myjson[i][y]["Country"])
        print(myjson[i][y]["Date"])
        print(myjson[i][y]["Price"])
        print(myjson[i][y]["Free slots"])
        print(myjson[i][y]["Link"])
        print("\n")

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
z=1
with open(r'C:\Users\PREZES\Desktop\snowridess\venv\temp.csv', 'w', newline='', encoding="utf8") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i, j in enumerate(db):
        print()

    for i in range(len(myjson)):

        for y in range(len(myjson[i])):

            writer.writerow([z,myjson[i][y]["Organizator"],myjson[i][y]["Country"],myjson[i][y]["City"],myjson[i][y]["Date"],myjson[i][y]["Price"],myjson[i][y]["Free slots"],myjson[i][y]["Link"]])
            z+=1
print("temp.csv created successfully")
#
# #### MYSQL CONNECTION
# conn = conn.connect(user='root', password='',
#                               host='127.0.0.1',
#                               database='trips')
# cur = conn.cursor()
#
#
# cur.execute("DROP TABLE TRIPS;")
# # Create database:
# try:
# ###Execute the SQL command
#     cur.execute("CREATE TABLE trips (id int NOT NULL PRIMARY KEY AUTO_INCREMENT, organizator text, trip_date text, price text, "
#             "free_slots text,country text, city text, link text);")
# # Commit your changes in the database
#     conn.commit()
# except:
# ## Rollback in case there is any error
#     conn.rollback()
#
# try:
#     cur.executemany("""INSERT INTO trips(organizator, country, city, trip_date, price, free_slots, link)
#                 VALUES (%(Organizator)s,%(Country)s, %(City)s, %(Date)s, %(Price)s, %(Free slots)s, %(Link)s)""", db)
#     conn.commit()
# except:
#     conn.rollback()
#
# # cur.execute("SELECT * FROM trips;")
# # print(cur.fetchall())
# # close cursor object
# cur.close()
# # disconnect from server
# conn.close()

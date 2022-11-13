import mysql.connector
import csv


connection = mysql.connector.connect(
    user='root', 
    password='root', 
    host='mysql', 
    port='3301',
    database='db')


cursor = connection.cursor()

csv_data = csv.reader(open('/db/data.csv'))


for row in csv_data:
    cursor.execute("INSERT INTO People (name, age) VALUES (%s, %s)", row)

connection.commit()

cursor.execute("SELECT * FROM People")

result = cursor.fetchall()

for row in result:
    print(row)

connection.close()


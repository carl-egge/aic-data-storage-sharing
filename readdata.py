import sqlite3

# Establish a connection to the SQLite database
connection = sqlite3.connect('sensor_data.db')
cursor = connection.cursor()

# Select all rows from the sensor_data table
select_query = "SELECT * FROM sensor_data"
cursor.execute(select_query)

# Fetch all rows as a list of tuples
rows = cursor.fetchall()

# Iterate over the rows and print the data
for row in rows:
    id_, timestamp, pollution_level, sensor_value = row
    print("ID:", id_)
    print("Timestamp:", timestamp)
    print("Pollution Level:", pollution_level)
    print("Sensor Value:", sensor_value)
    print()

# Close the cursor and connection
cursor.close()
connection.close()

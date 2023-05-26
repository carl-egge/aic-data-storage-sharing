#######################  UPLOAD SENSOR DATA TO STORAGE  ###########################

# This script consumes the data from the grovepi sensors and uploads it to the Cloud
# storage. The data is consumend in user-defined batch sizes. Using a symmetric
# encryption scheme the data is encrypted before it is uploaded to the storage. The 
# data is stored encrypted with little metadata in a SQL database.

# General imports (maybe we don't need all of them)
import os, sys, argparse, time, signal

# Imports for the GrovePi
import grovepi
import sqlalchemy

# local imports
from encryption.symmetric import encrypt_data, read_key
from gcp.get_sql_connection import getconn

# temporary imports
import sqlite3

#-------------------------------------------------------------------------------

# Maybe we can use arparse here to get the "batch size from the user"
# TODO: Later I cloud add a command line interface to the script here or we can 
#      just use a config file to set the batch size and other parameters. Or we
#      do this in a graphical user interface.


# This function is called when the script is terminated by the user
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#-------------------------------------------------------------------------------

# TODO: Ahmad, change this such that it consumes the data from the grovepi sensors
# and stores it in this dictionary:

# data = {
#     'time': "",
#     'pollution_level': "",
#     'sensor_value': 0,
#     'sensor_type': "",
# }

data = {}

####################  Grovepi sensor data consumption  #########################
# In this section we consume the data from the grovepi sensors. We can use the
# grovepi library for this. For now we can just use a predefined batch size and
# store the data in a simple data structure like a list or dictionary.


# Establish a connection to the SQLite database
connection = sqlite3.connect('sensor_data.db')
cursor = connection.cursor()

# Create a table to store the sensor data
create_table_query = '''CREATE TABLE IF NOT EXISTS sensor_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
                            pollution_level TEXT,
                            sensor_value INTEGER
                        );'''
cursor.execute(create_table_query)

# Connect the Grove Air Quality Sensor to analog port A0
# SIG,NC,VCC,GND
air_sensor = 0

grovepi.pinMode(air_sensor, "INPUT")

# If this should run forever we need to export this to a worker
# in order to not block the main thread
i = 0
while i < 20:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(air_sensor)

        if sensor_value > 700:
            pollution_level = "High pollution"
        elif sensor_value > 300:
            pollution_level = "Low pollution"
        else:
            pollution_level = "Air fresh"

        print("pollution_level =", pollution_level)
        print("sensor_value =", sensor_value)

        # Insert sensor data into the table
        insert_query = "INSERT INTO sensor_data (pollution_level, sensor_value) VALUES (?, ?)"
        cursor.execute(insert_query, (pollution_level, sensor_value))

        # Commit the changes to the database
        connection.commit()

        time.sleep(2)
        i += 1

    except IOError:
        print("Error")

# Close the cursor and connection
cursor.close()
connection.close()


#-------------------------------------------------------------------------------

###########################    Data encryption    ##############################

# Convert to string
data_str = str(data)

# Call encryption function
encrypted_data = encrypt_data(data_str, read_key())

#-------------------------------------------------------------------------------

#################### Upload data to cloud storage  #############################

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
  # TODO: Create table sql statement for the sensor data table
  # The columns should be: id, encrypted_data
  db_conn.execute(
    sqlalchemy.text(
      "CREATE TABLE IF NOT EXISTS ..."
    )
  )

  db_conn.commit()

  # insert data into our ratings table
  # TODO: Insert the encrypted data into the table
  insert_stmt = sqlalchemy.text(
      "INSERT INTO ...",
  )

  # insert entries into table
  db_conn.execute(insert_stmt, parameters={"encrypted_data": encrypted_data})

  # commit transactions
  db_conn.commit()


print("Success! Data uploaded to cloud storage!")
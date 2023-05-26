#######################  UPLOAD SENSOR DATA TO STORAGE  ###########################

# This script consumes the data from the grovepi sensors and uploads it to the Cloud
# storage. The data is consumend in user-defined batch sizes. Using a symmetric
# encryption scheme the data is encrypted before it is uploaded to the storage. The 
# data is stored encrypted with little metadata in a SQL database.

# General imports (maybe we don't need all of them)
import os, sys, argparse, time, signal

# Imports for the GrovePi
import grovepi
import time
import sqlite3
# Imports for the encryption

# Imports for the database connection
# I would recommend 'mysql.connector' or 'sqlalchemy' or something like that

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

# TODO: Ahmad, please write a function that consumes the data from the grovepi

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

while True:
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

    except IOError:
        print("Error")

# Close the cursor and connection
cursor.close()
connection.close()









#-------------------------------------------------------------------------------

# TODO: Rayhan, please write a function that encrypts the data

#################### Symmetric encryption of the data  #########################
# In this section we encrypt the data using a symmetric encryption scheme. I am
# sure there are helpful libraries. Goal should just be to turn some plaintext
# string into a ciphertext string. The key should be stored in a separate file.










#-------------------------------------------------------------------------------

# TODO: Lingo, please write a function that uploads the data to a local database

#################### Upload data to cloud storage  #############################
# In this section we upload the data to the database. For now we can just use a
# local database on the Raspberry Pi. Later we can switch to the cloud storage.
# You can use sqlite3 for a small database in the file system or mysql for a
# local database server. For that you would need to install and start MariaDB or 
# MySQL on the Raspberry Pi. I would recommend to use a local database server.





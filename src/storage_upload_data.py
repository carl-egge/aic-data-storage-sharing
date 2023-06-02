#######################  UPLOAD SENSOR DATA TO STORAGE  ###########################

# This script consumes the data from the grovepi sensors and uploads it to the Cloud
# storage. The data is consumend in user-defined batch sizes. Using a symmetric
# encryption scheme the data is encrypted before it is uploaded to the storage. The 
# data is stored encrypted with little metadata in a SQL database.

# General imports (maybe we don't need all of them)
import os, sys, signal, math
from datetime import datetime
# import argparse, time

# Imports for the GrovePi and GCP
import grovepi
import sqlalchemy

# Local imports
from encryption.symmetric import encrypt_data, read_key, generate_encryption_key
from gcp.get_sql_connection import getconn

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

####################  Grovepi sensor data consumption  #########################

# In this section we consume the data from the grovepi sensors. We can use the
# grovepi library for this. For now we can just use a predefined batch size and
# store the data in a simple data structure like a list/dictionary.

data = []  # List to store sensor data

# Connect the Grove Temperature & Humidity Sensor Pro to digital port D4
sensor = 4  # The Sensor goes on digital port 4.

# Connect the Grove Air Quality Sensor to analog port A0
air_sensor = 0

grovepi.pinMode(air_sensor, "INPUT")

# temp_humidity_sensor_type
blue = 0  # The Blue colored sensor.

try:
    [temp, humidity] = grovepi.dht(sensor, blue)
    if not (math.isnan(temp) or math.isnan(humidity)):
        temperature_status = 'Hot' if temp > 30 else 'Cold' if temp < 20 else 'Normal'
        temperature_data = {
            "time": datetime.now(),
            "sensor_type": "Temperature",
            "value": temp,
            "description": temperature_status
        }

        humidity_status = 'High humidity' if humidity > 70 else 'Normal humidity'
        humidity_data = {
            "time": datetime.now(),
            "sensor_type": "Humidity",
            "value": humidity,
            "description": humidity_status
        }

        data.append(temperature_data)
        data.append(humidity_data)

    sensor_value = grovepi.analogRead(air_sensor)

    if sensor_value > 700:
        pollution_status = "High pollution"
    elif sensor_value > 300:
        pollution_status = "Low pollution"
    else:
        pollution_status = "Air fresh"

    air_quality_data = {
        "time": datetime.now(),
        "sensor_type": "Air Quality",
        "value": sensor_value,
        "description": pollution_status
    }

    data.append(air_quality_data)


except IOError:
    print("Error")

#-------------------------------------------------------------------------------

###########################    Data encryption    ##############################

# In this section we check if a symmetric key is already stored in the filesystem.
# If not we generate a new key. Also we encrypt the data with the key.

if not os.path.exists("../encryption_key_storage.txt"):
    generate_encryption_key()
    print("New key generated")

# Call encryption function
encrypted_data = encrypt_data(str(data), read_key())

#-------------------------------------------------------------------------------

#################### Upload data to cloud storage  #############################

# In this section we upload the encrypted data to the cloud storage. We can use
# a sqlalchemy connection pool for this. The data is stored in a SQL database.
# We use the getconn() function from the get_sql_connection.py script to get a
# connection to the database.

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
    # create table if not exists
    db_conn.execute(
        sqlalchemy.text(
            "CREATE TABLE IF NOT EXISTS sensors_data "
            "( id SERIAL NOT NULL, encrypted_data VARCHAR(2550) NOT NULL, "
            "PRIMARY KEY (id));"
        )
    )

    db_conn.commit()

    # insert data into our ratings table
    insert_stmt = sqlalchemy.text(
        "INSERT INTO sensors_data (encrypted_data) VALUES (:encrypted_data)",
    )

    # insert entries into table
    db_conn.execute(insert_stmt, parameters={"encrypted_data": encrypted_data})

    # commit transactions
    db_conn.commit() 

print("Success! Data uploaded to cloud storage!")
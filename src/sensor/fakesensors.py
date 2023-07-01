#########################    READ SENSOR DATA   #############################

# This file holds a helper function that produces sensor data. It is used to
# get exaclty one read out from the sensors. The data is returned as a list of
# dictionaries. Each dictionary holds the data for one sensor. The data is
# structured as follows:
# {
#   "time": datetime.now(),
#   "sensor_type": "Temperature",
#   "value": temp,
#   "description": temperature_status
# }
#
# The sensor data is read out from the following sensors:
# - Temperature & Humidity Sensor Pro
# - Air Quality Sensor
#   
# The data is read out from the sensors using the grovepi library. The library
# is used to read out the data from the sensors. The data is then stored in a
# list of dictionaries and returned to the caller.

# THIS FILE JUST SERVES FAKE SENSOR DATA FOR TESTING PURPOSES
# USE THIS IF YOU DON'T HAVE THE SENSORS AND CANNOT WORK WITH THE GROVEPI LIBRARY

import random
from datetime import datetime

def one_sensor_data_readout():

    # intialize data list
    data = []

    temperature_data = {
        "time": datetime.now(),
        "sensor_type": "Temperature",
        "value": random.uniform(20.0, 30.0),
        "description": "Normal"
    }

    humidity_data = {
        "time": datetime.now(),
        "sensor_type": "Humidity",
        "value": random.uniform(20.0, 30.0),
        "description": "Normal"
    }

    pollution_data = {
        "time": datetime.now(),
        "sensor_type": "Air Quality",
        "value": random.uniform(20.0, 30.0),
        "description": "Normal"
    }

    data.append(temperature_data)
    data.append(humidity_data)
    data.append(pollution_data)
    
    return data
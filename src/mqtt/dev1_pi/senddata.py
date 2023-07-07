# this script is taken from sensor, you do not need it
import math, random
from datetime import datetime
import grovepi

def one_sensor_data_readout():

    # intialize data list
    data = []

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
        print("Error reading data from sensor")

    return data
import random, time, threading
from flask import Flask, render_template, request, redirect, flash, url_for
from turbo_flask import Turbo
import grovepi 
import os, sys, signal, math
from datetime import datetime

sensor = 4  # The Sensor goes on digital port 4.

# Connect the Grove Air Quality Sensor to analog port A0
air_sensor = 0

grovepi.pinMode(air_sensor, "INPUT")

# temp_humidity_sensor_type
blue = 0  # The Blue colored sensor.

app = Flask(__name__)
turbo = Turbo(app)

# Set a secret key to use for sessions -> needed for flash messages
app.secret_key = b'_5#x3K"F5Y8z\n\xec]/'
# Currently we store the batch size in a global variable
# TODO: Store the batch size in a config file
batch_size = 10
# TODO: Don't store the shared secret in a global variable
shared_secret = 'NaN'

@app.context_processor
def inject_load():
    '''
    Injects the sensor data into the template context
    Currently just generates random data
    TODO: Replace with real sensor data
    '''
    [temp, humidity] = grovepi.dht(sensor, blue)
    sensor_value = grovepi.analogRead(air_sensor)
    if sensor_value > 700:
        pollution_status = "High pollution"
    elif sensor_value > 300:
        pollution_status = "Low pollution"
    else:
        pollution_status = "Air fresh"

    temperature_status = 'Unknown'
    if not (math.isnan(temp) or math.isnan(humidity)):
        temperature_status = 'Hot' if temp > 30 else 'Cold' if temp < 20 else 'Normal'

    humidity_status = 'High humidity' if humidity > 70 else 'Normal humidity'

    return { 
        'temp': {'time': datetime.now(), 'value': temp, 'desc': temperature_status},
        'humi': {'time': datetime.now(), 'value': humidity, 'desc': humidity_status},
        'poll': {'time': datetime.now(), 'value': sensor_value, 'desc': pollution_status}
    }


@app.context_processor
def inject_load():
    '''
    Injects the output of the data sharing and data storage functions into the template context
    TODO: Replace with real data
    '''
    return { 
        'output': 'Here we could display the output of the data sharing and data storage functions'
    }


@app.route('/')
def index():
    '''
    Renders the index.html template (home page)
    '''
    return render_template('index.html', batch_size=batch_size, shared_secret=shared_secret)

##########################################################################################
# The following routes are called with POST requests from the forms on the home page
# They are used to actually control and run the application
# TODO: Implement the actual functionality

@app.route('/store-data', methods=['POST'])
def store_data():
    '''
    Stores the sensor data in the GCP instance
    '''
    flash('Not implemented yet')
    # flash('Success! Data stored in GCP')
    return redirect("/")


@app.route('/retrieve-data', methods=['POST'])
def retrieve_data():
    '''
    Retrieves the sensor data from the GCP instance
    '''
    flash('Not implemented yet')
    # flash('Success! Data retrieved from GCP')
    return redirect("/")


@app.route('/share-data', methods=['POST'])
def share_data():
    '''
    Shares the sensor data with other peer device
    '''
    flash('Not implemented yet')
    # flash('Success! Data shared with other peer')
    return redirect("/")


@app.route('/set-batch-size', methods=['POST'])
def set_batch_size():
    '''
    Only called with POST requests and form data
    Sets the batch size to the value of the batch_size form field
    '''
    global batch_size
    batch_size = int(request.form.get('batch_size'))
    flash(f'Success! Batch size set to {batch_size}')
    return redirect("/")


@app.route('/generate-sym-key', methods=['POST'])
def generate_sym_key():
    '''
    Only called with POST requests
    Generates a new symmetric key and stores it in the filesystem
    TODO: Actually generate a symmetric key and store it
    '''
    flash('Not implemented yet')
    # flash('Success! Symmetric key generated')
    return redirect("/")


@app.route('/connect-to-gcp', methods=['POST'])
def connect_to_gcp():
    '''
    Establishes a connection to the Google Cloud Platform
    TODO: Actually connect to the GCP
    '''
    flash('Not implemented yet')
    # flash('Success! Connected to GCP')
    return redirect("/")


@app.route('/exchange-keys', methods=['POST'])
def exchange_keys():
    '''
    Run asymmetric key exchange through mqtt and calculate the shared secret
    '''
    flash('Not implemented yet')
    # flash('Success! Shared secret calculated')
    return redirect("/")


##########################################################################################

def update_load():
    '''
    Updates the sensor data every second using turbo.js
    '''
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('loaddata.html'), 'sensor'))
            turbo.push(turbo.replace(render_template('output.html'), 'output'))


th = threading.Thread(target=update_load)
th.daemon = True
th.start()
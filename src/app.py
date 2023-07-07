#########################   app.py   #############################

# This file is the entry point to the application. It starts the 
# flask application and handles the main business logic.

import time, threading
from flask import Flask, render_template, request, redirect, flash, url_for
from turbo_flask import Turbo
# from flask import session

from sensor.sensors import one_sensor_data_readout
from sharing import DataSharing
from storage import DataStorage

app = Flask(__name__)
turbo = Turbo(app)

##########################################################################################
# Set a secret key to use for sessions -> needed for flash messages
app.secret_key = b'_5#x3K"F5Y8z\n\xec]/'

# Globally create our storage and sharing objects
store = DataStorage()
share = DataSharing()

# Globally store the current sensor data and output
sensor_data = []
output = "No output yet"


##########################################################################################
@app.context_processor
def inject_load():
    '''
    Injects the sensor data into the template context
    '''
    global sensor_data
    sensor_data = one_sensor_data_readout()
    return { 
        'temp': {'time': sensor_data[0]["time"], 'value': sensor_data[0]["value"], 'desc': sensor_data[0]["description"]},
        'humi': {'time': sensor_data[1]["time"], 'value': sensor_data[1]["value"], 'desc': sensor_data[1]["description"]},
        'poll': {'time': sensor_data[2]["time"], 'value': sensor_data[2]["value"], 'desc': sensor_data[2]["description"]},
        'output': output, 
    }


@app.route('/')
def index():
    '''
    Renders the index.html template (home page)
    '''
    return render_template('index.html', batch_size=store.batch_size, shared_secret=share.shared_secret, sym_key=store.sym_key)

##########################################################################################
# The following routes are called with POST requests from the forms on the home page
# They are used to actually control and run the application

@app.route('/store-data', methods=['POST'])
def store_data():
    '''
    Stores the sensor data in the GCP instance
    '''
    global output
    output = "Store Sensor Data: \n" + str(sensor_data)
    if store.batch_size == 1:
        encrypted_data = store.store_data(sensor_data)
    else:
        # If batch size is larger than 1, we cannot just store the current sensor data
        # We need to fetch multiple data points (batch) and store them
        # store_data() will take care of this
        encrypted_data = store.store_data()
    flash('Successfully stored data')
    output = "\n\nEncrypted Data: \n" + str(encrypted_data)
    return redirect("/")


@app.route('/retrieve-data', methods=['POST'])
def retrieve_data():
    '''
    Retrieves the sensor data from the GCP instance
    '''
    global output
    output = "Retrieving Sensor Data..."
    decrypted_data = store.retrieve_data()
    flash('Successfully retrieved data')
    output = "Retrieve Sensor Data: \n" + str(decrypted_data)
    return redirect("/")


@app.route('/generate-sym-key', methods=['POST'])
def generate_sym_key():
    '''
    Only called with POST requests
    Generates a new symmetric key and stores it in the filesystem
    '''
    store.generate_sym_key()
    flash('Success! Symmetric key generated')
    return redirect("/")


@app.route('/exchange-keys', methods=['POST'])
def exchange_keys():
    '''
    Run asymmetric key exchange through mqtt and calculate the shared secret
    '''
    share.run_key_exchange()
    flash('Success! Shared secret calculated')
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
    store.batch_size = int(request.form.get('batch_size'))
    share.batch_size = int(request.form.get('batch_size'))
    flash(f'Success! Batch size set to {store.batch_size}')
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

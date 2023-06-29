import random, time, threading
from flask import Flask, render_template, request, redirect, flash, url_for
from turbo_flask import Turbo
import grovepi 
import os, sys, signal, math
from datetime import datetime
import os
from google.cloud.sql.connector import Connector
from dotenv import load_dotenv
import sqlalchemy
from cryptography.fernet import Fernet



# This function generates a new key and stores it in the filesystem
def generate_encryption_key():
    encryption_key = Fernet.generate_key()
    encoded_key = encryption_key.decode()  # Convert bytes to string
    with open("../encryption_key_storage.txt", "w") as texttxt:
        texttxt.write(encoded_key)

# This function reads the key from the filesystem
def read_key():
    with open("../encryption_key_storage.txt", "r") as file:
        encoded_key = file.read()
        encryption_key = encoded_key.encode() # Convert string to bytes
    return encryption_key

# This function encrypts the data with the key and returns
# the encrypted data as a string
def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# This function decrypts the data with the key and returns
# the decrypted data as a string
def decrypt_data(data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data)
    return decrypted_data


# function to return the database connection
def getconn():

	# GCP IAM authentication using service account key
	# In order for this script to work you need to create a service account key, store the JSON and update the path below!
	# How to create a service account key: https://cloud.google.com/iam/docs/keys-create-delete?hl=de#iam-service-account-keys-create-console
	# Alternatively you can authenticate using the Google Cloud SDK.
	credential_path = "/home/pi/aic/gcp_key/aic23-groupb1-data-storage-4f89199ed283.json" # IMPORTANT: Change this to your own path
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

	# set config
	# The .env file with the database credentials is needed for this to work.
	load_dotenv()

	project_id = os.getenv("project_id")
	region = os.getenv("region")
	instance_name = os.getenv("instance_name")
	db_user = os.getenv("db_user")
	db_pass = os.getenv("db_pass")
	db_name = os.getenv("db_name")

	# initialize parameters
	INSTANCE_CONNECTION_NAME = f"{project_id}:{region}:{instance_name}"
	print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")

	# initialize Connector object
	connector = Connector()

	# Establish connection
	conn = connector.connect(
		INSTANCE_CONNECTION_NAME,
		"pymysql",
		user=db_user,
		password=db_pass,
		db=db_name
	)
	return conn


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
    
    sensor_data = inject_load()
    string_data = str(sensor_data)
    encrypted_data_string = encrypt_data(string_data, read_key())
    app.config['encrypted_data_string'] = encrypted_data_string  # Store decrypted_data in app context
    '''
    flash('Not implemented yet')
    return redirect("/")


'''
@app.context_processor
def inject_load():
   
    Injects the output of the data sharing and data storage functions into the template context
    TODO: Replace with real data
    
    encrypted_data_string = app.config.get('encrypted_data_string')
    
    return {
        'output': encrypted_data_stringy
    }
'''
@app.route('/retrieve-data', methods=['POST'])
def retrieve_data():
    '''
    Retrieves the sensor data from the GCP instance
    '''
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    with pool.connect() as db_conn:
        # query and fetch test table
        results = db_conn.execute(sqlalchemy.text("SELECT * FROM sensors_data")).fetchall()

        last_row = results[-1]
        token = last_row[1].encode()  # Convert token to bytes
        decrypted_data = decrypt_data(token, read_key())

        app.config['decrypted_data'] = decrypted_data  # Store decrypted_data in app context

    return redirect("/")


@app.context_processor
def inject_load():
    '''
    Injects the output of the data sharing and data storage functions into the template context
    TODO: Replace with real data
    '''
    decrypted_data = app.config.get('decrypted_data')  # Retrieve decrypted data from app context
    return {
        'output': decrypted_data 
    }



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
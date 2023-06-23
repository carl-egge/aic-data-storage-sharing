import random, time, threading
from flask import Flask, render_template, request, redirect, flash, url_for
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)

# Set a secret key to use for sessions -> needed for flash messages
app.secret_key = b'_5#x3K"F5Y8z\n\xec]/'
# Currently we store the batch size in a global variable
# TODO: Store the batch size in a config file
batch_size = 10

@app.context_processor
def inject_load():
    '''
    Injects the sensor data into the template context
    Currently just generates random data
    TODO: Replace with real sensor data
    '''
    load = [int(random.random() * 100) / 100 for _ in range(3)]
    return { 
        'temp': {'time': load[0], 'value': load[1], 'desc': load[2]},
        'humi': {'time': load[0], 'value': load[1], 'desc': load[2]},
        'poll': {'time': load[0], 'value': load[1], 'desc': load[2]}
    }


@app.route('/')
def index():
    '''
    Renders the index.html template (home page)
    '''
    return render_template('index.html', batch_size=batch_size)

##########################################################################################
# The following routes are called with POST requests from the forms on the home page
# They are used to actually control and run the application
# TODO: Implement the actual functionality

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

##########################################################################################
def update_load():
    '''
    Updates the sensor data every second using turbo.js
    '''
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('loaddata.html'), 'sensor'))


th = threading.Thread(target=update_load)
th.daemon = True
th.start()
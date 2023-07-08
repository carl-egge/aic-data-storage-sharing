#########################   DATA SHARING CLASS   #############################

# This file is the entry point to the application. It starts the 
# flask application and handles the main business logic.

import paho.mqtt.client as mqtt
import pyDH, base64


# TODO: Change this import to the real sensor data consumption if working on the pi:
from sensor.sensors import one_sensor_data_readout, sensor_data_readout
# from sensor.fakesensors import one_sensor_data_readout, 

from encryption.symmetric import encrypt_data

class DataSharing:
    '''
    This class implements the functionality for the data sharing system of the project.
    It is used to run the Diffie-Hellman key exchange and to encrypt and decrypt data
    that is shared between the two parties.
    '''

    def __init__(self, batch_size = 1, shared_secret = "NaN"):
        '''
        Constructor for the DataSharing class
        This is executed when the class is instantiated
        '''
        self.batch_size = batch_size
        self.shared_secret = shared_secret

        # In the server_channel the pi initiate the key-exchange and publishes sensor data.
        self.server_channel = "server_channel"
        # In the client_channel the pi subscribe to the incoming messages.
        self.client_channel = "client_channel"
        # In the data_sharing channel the pi publishes actual sensor data.
        self.data_sharing_channel = "data_sharing"

        print("DataSharing object created with batch size: ", self.batch_size)

    # -----------------------------------------------------------------------------------
    def run_key_exchange(self):
        '''
        Runs the Diffie-Hellman key exchange
        '''
        # Connect to the MQTT broker
        client = self.connect_mqtt_broker()
        print("MQTT client connected to broker.")

        # Reset the shared secret
        self.shared_secret = "NaN"

        # Create a Diffie-Hellman object
        dh = pyDH.DiffieHellman()
        dh_pubkey = dh.gen_public_key()

        # Subscribe to the topic
        client.subscribe(self.client_channel)

        # Define callback function for the MQTT client
        def on_message(client, userdata, message):
            # Get the public key of the other party
            other_pubkey = int(message.payload.decode("utf-8"))
            # Calculate the shared secret
            self.shared_secret = dh.gen_shared_key(other_pubkey)
            # Print the shared secret
            # print("Shared secret: ", self.shared_secret)
            # Encode the shared secret to base64
            self.shared_secret = base64.urlsafe_b64encode(bytes.fromhex(self.shared_secret))
            # Print the shared secret encoded
            print("Shared encoded secret : ", self.shared_secret)

        # Set the callback function
        client.on_message = on_message
        # Run the MQTT loop
        client.loop_start()
        
        # Publish your public key
        client.publish(self.server_channel, dh_pubkey)

        # Wait for the shared secret to be calculated
        while self.shared_secret == "NaN":
            pass

        # Stop the MQTT loop
        client.loop_stop()
        # Disconnect from the MQTT broker
        client.disconnect()

        return self.shared_secret
    
    
    def share_data(self):
        '''
        Shares the encrypted sensor data with the other party
        '''
        # Connect to the MQTT broker
        client = self.connect_mqtt_broker()
        print("MQTT client connected to broker.")
        
        # Read the sensor data according to the batch size
        data = sensor_data_readout(self.batch_size)

        # Encrypt the data
        encry_data = encrypt_data(str(data), self.shared_secret)

        # Publish the encrypted data
        client.publish(self.data_sharing_channel, encry_data)

        # Disconnect from the MQTT broker
        client.disconnect()

    # -----------------------------------------------------------------------------------

    def set_batch_size(self, batch_size):
        # Sets the batch size for the data sharing system
        self.batch_size = batch_size


    def connect_mqtt_broker(self, broker_address = '84.58.225.213', port = 1883):
        '''
        Connects to the MQTT broker
        '''
        # Create a MQTT client
        client = mqtt.Client()
        # Connect to the MQTT broker
        client.connect(broker_address, port)
        return client

#########################   DATA SHARING CLASS   #############################

# This file is the entry point to the application. It starts the 
# flask application and handles the main business logic.

import paho.mqtt.client as mqtt
import pyDH

# TODO: Change this import to the real sensor data consumption if working on the pi:
# from sensor.sensor import one_sensor_data_readout
from sensor.fakesensors import one_sensor_data_readout

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
        print("DataSharing object created with batch size: ", self.batch_size)

    # -----------------------------------------------------------------------------------
    def run_key_exchange(self):
        '''
        Runs the Diffie-Hellman key exchange
        '''
        # Connect to the MQTT broker
        client = self.connect_mqtt_broker()
        print("MQTT client connected to broker.")

        # Create a Diffie-Hellman object
        dh = pyDH.DiffieHellman()
        dh_pubkey = dh.gen_public_key()

        # Subscribe to the topic
        client.subscribe("key_exchange")

        # Define callback function for the MQTT client
        def on_message(client, userdata, message):
            # Get the public key of the other party
            other_pubkey = int(message.payload.decode("utf-8"))
            # Calculate the shared secret
            self.shared_secret = dh.gen_shared_key(other_pubkey)
            # Print the shared secret
            print("Shared secret: ", self.shared_secret)

        # Set the callback function
        client.on_message = on_message
        # Run the MQTT loop
        client.loop_start()
        
        # Publish your public key
        client.publish("key_exchange", dh_pubkey)

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
        # Subscribe to the topic
        client.subscribe("data_sharing")
        
        #
        # TODO: @Rayhan
        # Please implement the functionality to share the encrypted data with the other party
        # The data can be retrieved using the one_sensor_data_readout() function from the sensor.py file
        # The data should be symmetrically encrypted using the shared secret as the key
        # You can use our implementation of the AES encryption from the encryption.py file
        # The encrypted data should be sent to the other party using the MQTT client
        #
        print("TODO: Implement the data sharing functionality here.")

        # -----------------------
        # YOUR CODE GOES HERE
        # -----------------------

        # Disconnect from the MQTT broker
        client.disconnect()


    # -----------------------------------------------------------------------------------

    def set_batch_size(self, batch_size):
        '''
        Sets the batch size for the data sharing system
        '''
        self.batch_size = batch_size


    def connect_mqtt_broker(self, broker_address = '192.168.1.105', port = 1883):
        '''
        Connects to the MQTT broker
        '''
        # Create a MQTT client
        client = mqtt.Client()
        # Connect to the MQTT broker
        client.connect(broker_address, port)
        return client
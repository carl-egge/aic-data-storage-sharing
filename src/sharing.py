#########################   DATA SHARING CLASS   #############################

# This file is the entry point to the application. It starts the 
# flask application and handles the main business logic.

import paho.mqtt.client as mqtt
import pyDH

from .encryption.symmetric import decrypt_data, read_key
from .gcp.get_sql_connection import getconn


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

        # d1 = pyDH.DiffieHellman()
        # d1_pubkey = d1.gen_public_key()

        print('Not yet implemented')
        # # Subscribe to the topic
        # client.subscribe("key_exchange")
        # # Run the MQTT loop
        # client.loop_start()
        # # Wait for the key exchange to finish
        # while self.shared_secret == "NaN":
        #     pass
        # # Stop the MQTT loop
        # client.loop_stop()
        # # Disconnect from the MQTT broker
        # client.disconnect()
        # # Return the shared secret
        # return self.shared_secret
    
    def share_data(self):
        '''
        Shares the data with the other party
        '''
        # Connect to the MQTT broker
        client = self.connect_mqtt_broker()
        
        print('Not yet implemented')

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
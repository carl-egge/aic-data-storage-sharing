#####################  RECEIVER OF SHARING DATA  #########################

# This script should be started on the raspberry pi that receives the data from the
# other party. The shared secret is used to decrypt the data. This script will run until
# the user presses CTRL-C. In the first phase it will listen to the server_channel and
# try to establish a shared secret using DH. In the second phase it will listen to the 
# data_sharing and decrypt the data using the shared secret.

import pyDH, paho.mqtt.client as mqtt
from encryption.symmetric import decrypt_data
import base64, os, time
from dotenv import load_dotenv

print("Starting the script...")
print("Ready to run the key exchange and receive encrypted sensor data.")

load_dotenv()

# GOBAL VARIABLES
# In the server_channel the pi initiate the key-exchange and publishes sensor data.
server_channel = "server_channel"
# In the client_channel the pi subscribe to the incoming messages.
client_channel = "client_channel"
# In the data_sharing channel the pi subscribe to the incoming data.
data_sharing_channel = "data_sharing"        
# The shared secret is established during the key exchange
shared_secret = "NaN"
# IP address of the MQTT broker
broker_address = os.getenv("broker_address")
# Port of the MQTT broker
port = int(os.getenv("broker_port"))

# BROKER FUNCTIONS
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT client connected to broker.")
        # Subscribe to both incoming channels
        client.subscribe(server_channel)
        client.subscribe(data_sharing_channel)
    else:
        print("MQTT client connection failed.")


def on_message(client, userdata, msg):
    global shared_secret
    print("\nMessage received : "  + str(msg.payload) + " on " + msg.topic)

    # Listen to the server channel
    if msg.topic == server_channel:
        # Get the public key of the other party
        other_pubkey = int(msg.payload.decode("utf-8"))
        # Return the diffie-Hellman key
        client.publish(client_channel, dh_pubkey)
        # Calculate the shared secret
        shared_secret = dh.gen_shared_key(other_pubkey)
        # Print the shared secret
        # print("Shared secret : ", shared_secret)
        # Encode the shared secret
        shared_secret = base64.urlsafe_b64encode(bytes.fromhex(shared_secret))
        # Print the shared secret encoded
        print("\nShared encoded secret : ", shared_secret)

    # Listen to the data sharing channel
    if msg.topic == data_sharing_channel:
        # Decrypt the data
        decrypted_data = decrypt_data(msg.payload, shared_secret)
        # Print the decrypted data
        print("\nReceived and decrypted data:", decrypted_data)


# Create a MQTT client and connect to broker
client = mqtt.Client()
client.on_connect= on_connect    
client.on_message= on_message  
client.connect(broker_address, port)

# Create a Diffie-Hellman object
dh = pyDH.DiffieHellman()
dh_pubkey = dh.gen_public_key()

# Run the MQTT loop
client.loop_start()

# Run until the user presses CTRL-C
try:
    while True:
        time.sleep(0.01)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
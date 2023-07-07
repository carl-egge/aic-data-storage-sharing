import pyDH, paho.mqtt.client as mqtt
from encryption.symmetric import decrypt_data

# In the server_channel the pi initiate the key-exchange and publishes sensor data.
server_channel = "server_channel"

# In the client_channel the pi subscribe to the incoming messages.
client_channel = "client_channel"        

broker_address = '84.58.225.213'
port = 1883

shared_secret = "NaN"

# Create a MQTT client
client = mqtt.Client()
# Connect to the MQTT broker
client.connect(broker_address, port)


# Connect to the MQTT broker

print("MQTT client connected to broker.")

# Create a Diffie-Hellman object
dh = pyDH.DiffieHellman()
dh_pubkey = dh.gen_public_key()

# Subscribe to the topic
client.subscribe(server_channel)

# Define callback function for the MQTT client
def on_message(client, userdata, message):
    # Get the public key of the other party
    other_pubkey = int(message.payload.decode("utf-8"))

    # Return the diffie-Hellman key
    client.publish(client_channel, dh_pubkey)

    # Calculate the shared secret
    shared_secret = dh.gen_shared_key(other_pubkey)
    # Print the shared secret
    print("Shared secret: ", shared_secret)

# Set the callback function
client.on_message = on_message
# Run the MQTT loop
client.loop_start()

# Wait for the shared secret to be calculated
while shared_secret == "NaN":
    pass

# Stop the MQTT loop
client.loop_stop()

# Subscribe to the topic
client.subscribe("data_sharing")

def on_message(client, userdata, msg):
    encrypted_data = msg.payload
    decrypted_data = decrypt_data(shared_secret, encrypted_data)
    print("Received and decrypted data:", decrypted_data)

client.on_message = on_message
client.loop_start()
# you need to think about the timeout and delete the first message Hallo

import time
import paho.mqtt.client as mqtt
from pyDH import DiffieHellman

broker_address = '84.58.225.213'  # Replace with the actual IP address of your MQTT broker
device1_topic = 'device1_channel'
device2_topic = 'device2_channel'

dh = DiffieHellman()
dh_pubkey = dh.gen_public_key()

shared_key = None
key_generated = False
timeout = 5  # 5 seconds timeout

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(device1_topic)  # Subscribe to Device 1's channel upon successful connection
    send_public_key()

def on_message(client, userdata, msg):
    global shared_key, key_generated

    if msg.topic == device1_topic:
        if msg.payload.decode('utf-8') == "Hallo":
            return  # Drop the message if it contains "Hallo"

        received_pubkey = int(msg.payload.decode('utf-8'))  # Convert the received public key to an integer

        shared_secret = dh.gen_shared_key(received_pubkey)
        shared_key = str(shared_secret)  # Convert the shared key to a string for simplicity

        print("Shared key generated:", shared_key)
        write_shared_key()
        key_generated = True

def send_public_key():
    client.publish(device2_topic, str(dh_pubkey))  # Publish Device 2's public key in its channel
    client.publish(device1_topic, "Hallo")  # Publish "Hallo" on Device 1's channel

def write_shared_key():
    with open('device2_shared_key.txt', 'w') as file:
        file.write(shared_key)
        print("Device 2 shared key written to file.")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address)

start_time = time.time()

while not key_generated:
    client.loop()
    if not key_generated:
        send_public_key()

    elapsed_time = time.time() - start_time
    if elapsed_time >= timeout:
        print("Timeout: Shared key generation failed.")
        break

    time.sleep(1)

client.loop_stop()
client.disconnect()

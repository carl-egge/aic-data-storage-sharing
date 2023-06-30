import time
import random
import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = '192.168.1.105' #You have to insert your own Ip Adress 
broker_port = 1883

# Create a MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Publish messages every second
while True:
    # Generate random temperature value
    temperature = random.uniform(20.0, 30.0)

    # Publish temperature value to the topic "sensors/temperature"
    client.publish("sensors/temperature", temperature)

    # Wait for 1 second
    time.sleep(1)


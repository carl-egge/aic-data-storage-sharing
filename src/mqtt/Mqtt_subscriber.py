import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = '84.58.225.213' #replace with your own address
broker_port = 1883

# Callback function to handle MQTT messages
def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    print(f"Received message: Topic='{topic}', Payload='{payload}'")

# Create a MQTT client
client = mqtt.Client()

# Set the callback function for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

# Subscribe to the topic "sensors/temperature"
client.subscribe("sensors/temperature")

# Loop to continuously listen for MQTT messages
client.loop_forever()

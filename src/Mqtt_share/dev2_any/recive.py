import paho.mqtt.client as mqtt
import base64
from cryptography.fernet import Fernet

broker_address = '84.58.225.213'
topic = 'sensors/tem'

shared_key_file = 'device2_shared_key.txt'  # File containing the shared key

def read_shared_key():
    with open(shared_key_file, 'r') as file:
        shared_key = file.read()
        return shared_key.strip()

def decrypt_message(encrypted_message, key):
    fernet_key = Fernet(key)
    decrypted_message = fernet_key.decrypt(encrypted_message)
    return decrypted_message.decode()

# Convert the provided key to the appropriate format
provided_key = read_shared_key()
key = base64.urlsafe_b64encode(bytes.fromhex(provided_key))

def on_message(client, userdata, message):
    encoded_message = message.payload.decode()
    encrypted_message = base64.b64decode(encoded_message)
    decrypted_message = decrypt_message(encrypted_message, key)
    print('Received message:', decrypted_message)

client = mqtt.Client()
client.connect(broker_address)
client.subscribe(topic)
client.on_message = on_message

client.loop_forever()

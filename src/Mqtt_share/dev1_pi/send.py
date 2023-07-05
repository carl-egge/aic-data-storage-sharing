#please run the key_ex first on both device
# Do not forget to run the recive.py on the other device before publishing the data
from senddata import one_sensor_data_readout
import paho.mqtt.client as mqtt
import base64
from cryptography.fernet import Fernet

broker_address = '84.58.225.213'
topic = 'sensors/tem'

shared_key_file = 'device1_shared_key.txt'  # File containing the shared key

def read_shared_key():
    with open(shared_key_file, 'r') as file:
        shared_key = file.read()
        return shared_key.strip()

def encrypt_message(message, key):
    fernet_key = Fernet(key)
    encrypted_message = fernet_key.encrypt(message.encode())
    return encrypted_message
# you do not need this function here 
def decrypt_message(encrypted_message, key):
    fernet_key = Fernet(key)
    decrypted_message = fernet_key.decrypt(encrypted_message)
    return decrypted_message.decode()

# Convert the provided key to the appropriate format
provided_key = read_shared_key()
key = base64.urlsafe_b64encode(bytes.fromhex(provided_key))

# usage
sensor_data = one_sensor_data_readout()
message = str(sensor_data)  # Convert the list to a string representation
encrypted_message = encrypt_message(message, key)
encoded_message = base64.b64encode(encrypted_message).decode()

client = mqtt.Client()
client.connect(broker_address)
client.publish(topic, encoded_message)
client.disconnect()



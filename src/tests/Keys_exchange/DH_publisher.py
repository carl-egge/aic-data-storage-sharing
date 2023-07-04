import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh

# Generate Diffie-Hellman parameters
parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
private_key = parameters.generate_private_key()
public_key = private_key.public_key()

# Save the private key to a file 
private_key_path = "/Users/admin2/encore2/private_key.pem"
with open(private_key_path, "wb") as key_file:
    key_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Get the public key
public_key = private_key.public_key()

# Save the public key to a file 
public_key_path = "/Users/admin2/encore2/public_key.pem"
with open(public_key_path, "wb") as key_file:
    key_file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

# Connect to the MQTT broker
mqtt_broker = "84.58.225.213"
mqtt_port = 1883
mqtt_topic = "diffie_hellman_key_exchange"

def on_connect(client, userdata, flags, rc):
    print('Connection established')
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print("Encrypted message before decryption:", msg.payload)

    # Decrypt the message using the private key
    decrypted_message = private_key.decrypt(
        msg.payload,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("decrypted message:", decrypted_message.decode("utf-8"))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)
client.loop_forever()


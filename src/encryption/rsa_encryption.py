import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Generate the RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Save the private key to a file (PEM format)
private_key_path = "/home/pi/Project/project_b1/src/Last/private_key.pem" #define your own path
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

# Save the public key to a file (PEM format)
public_key_path = "/home/pi/Project/project_b1/src/Last/public_key.pem" #define your own path
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
mqtt_topic = "encryption_topic"

client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)
print('Connection established')

# Publish the public key
with open(public_key_path, "rb") as key_file:
    public_key_pem = key_file.read()
    client.publish(mqtt_topic + "/public_key", public_key_pem)

# Encrypt and publish the message
message = "Data asymmetric encryption is almost done !!!!!!!!!!!!"

# Encrypt the message using the PC's public key
pc_public_key = None

def on_connect(client, userdata, flags, rc):
    client.subscribe(mqtt_topic + "/public_key")

def on_message(client, userdata, msg):
    global pc_public_key
    if msg.topic == mqtt_topic + "/public_key":
        pc_public_key = serialization.load_pem_public_key(
            msg.payload,
            backend=default_backend()
        )
        # Encrypt the message
        encrypted_message = pc_public_key.encrypt(
            message.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # Print the encrypted message
        print('Encrypted message:', encrypted_message)
        # Publish the encrypted message
        client.publish(mqtt_topic, encrypted_message)

print('Message:', message)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()

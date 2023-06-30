import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
# Generate the Diffie-Hellman key pair
private_key_dh = ec.generate_private_key(ec.SECP384R1(), default_backend())
public_key_dh = private_key_dh.public_key()

# Save the private key to a file (PEM format)
private_key_dh_path = "/Users/admin2/Rasp/private_key_dh.pem"
with open(private_key_dh_path, "wb") as key_file:
    key_file.write(
        private_key_dh.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Get the public key
public_key_dh_path = "/Users/admin2/Rasp/public_key_dh.pem"
with open(public_key_dh_path, "wb") as key_file:
    key_file.write(
        public_key_dh.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

# Connect to the MQTT broker
mqtt_broker = "192.168.1.103"
mqtt_port = 1883
mqtt_topic = "encryption_topic"

client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port, 60)
print('Connection established')

# Publish the Diffie-Hellman public key
with open(public_key_dh_path, "rb") as key_file:
    public_key_dh_pem = key_file.read()
    client.publish(mqtt_topic + "/public_key_dh", public_key_dh_pem)

# Perform Diffie-Hellman key exchange and publish the shared secret
shared_secret = None

def on_connect(client, userdata, flags, rc):
    client.subscribe(mqtt_topic + "/public_key_dh")

def on_message(client, userdata, msg):
    global shared_secret
    if msg.topic == mqtt_topic + "/public_key_dh":
        peer_public_key_dh = serialization.load_pem_public_key(
            msg.payload,
            backend=default_backend()
        )
        shared_key = private_key_dh.exchange(ec.ECDH(), peer_public_key_dh)
        shared_secret = hashes.Hash(hashes.SHA256(), backend=default_backend())
        shared_secret.update(shared_key)
        shared_secret = shared_secret.finalize()
        # Print the shared secret
        print('Shared Secret:', shared_secret)
        # Publish the shared secret
        #client.publish(mqtt_topic, shared_secret)

client.on_connect = on_connect
client.on_message = on_message

client.loop_start()

# Wait until shared secret is established
while shared_secret is None:
    pass

#encryption function 

def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# Encrypt and publish the message
message = "Data symmetric encryption is almost done guyyyyyy!!!!!!!!!!!!"
print(message)
# Encrypt the message using the shared secret
#cipher = Fernet(shared_secret[:32])  # Use the first 16 bytes of shared secret as the key
#encrypted_message = cipher.encrypt(message.encode("utf-8"))
encrypted_message = encrypt_data("Hello Word", shared_secret.encode("utf-8"))
# Publish the encrypted message
client.publish(mqtt_topic + "/encrypted_message", encrypted_message)

client.loop_forever()


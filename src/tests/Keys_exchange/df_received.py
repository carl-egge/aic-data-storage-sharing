import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization, hashes

# Generate the Diffie-Hellman key pair
private_key_dh = ec.generate_private_key(ec.SECP384R1(), default_backend())
public_key_dh = private_key_dh.public_key()

# Save the private key to a file (PEM format)
private_key_dh_path = "/Users/admin2/Last/private_key_dh.pem"
with open(private_key_dh_path, "wb") as key_file:
    key_file.write(
        private_key_dh.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Get the public key
public_key_dh_path = "/Users/admin2/Last/public_key_dh.pem"
with open(public_key_dh_path, "wb") as key_file:
    key_file.write(
        public_key_dh.public_bytes(
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
print('connection established')

# Subscribe to the MQTT topic
client.subscribe(mqtt_topic)

# Publish the Diffie-Hellman public key
with open(public_key_dh_path, "rb") as key_file:
    public_key_dh_pem = key_file.read()
    client.publish(mqtt_topic + "/public_key_dh", public_key_dh_pem)

# Perform Diffie-Hellman key exchange and publish the shared secret
shared_secret = None

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

client.on_message = on_message

client.loop_start()

# Wait until shared secret is established
while shared_secret is None:
    pass

# Decrypt and print the received message
def on_message(client, userdata, msg):
    print("Encrypted message:", msg.payload)

    # Decrypt the message using the shared secret
    decrypted_message = shared_secret[:16]  # Use the first 16 bytes of shared secret as the key
    cipher = Fernet(decrypted_message)
    decrypted_payload = cipher.decrypt(msg.payload)
    print("Received message:", decrypted_payload.decode("utf-8"))

client.on_message = on_message
client.loop_forever()


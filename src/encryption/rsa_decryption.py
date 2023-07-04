import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives import serialization, padding
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes


# Generate the RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Save the private key to a file (PEM format)
private_key_path = "/Users/admin2/Last/private_key.pem" #replace with your own path
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
public_key_path = "/Users/admin2/Last/public_key.pem" #replace with your own path
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
print('connection etablish')
# Subscribe to the MQTT topic
client.subscribe(mqtt_topic)

# Publish the public key
with open(public_key_path, "rb") as key_file:
    public_key_pem = key_file.read()
    client.publish(mqtt_topic + "/public_key", public_key_pem)

#print("The message before the encryption is",msg.payload)
# Decrypt and print the received message
def on_message(client, userdata, msg):
   
    print("Encrypted message:", msg.payload)

    # Decrypt the message using the private key
    decrypted_message = private_key.decrypt(
        msg.payload,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print("Received message:", decrypted_message.decode("utf-8"))

client.on_message = on_message

client.loop_forever()

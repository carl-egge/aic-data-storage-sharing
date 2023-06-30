## The server.py and the client.py should run at the same device because we are using the same IP
#for the server and the client

import socket
import pickle
import pyDH

d2 = pyDH.DiffieHellman()
d2_pubkey = d2.gen_public_key()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)   # Queue

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    # Send device 2's public key to device 1
    d2_pubkey_bytes = pickle.dumps(d2_pubkey)
    clientsocket.send(d2_pubkey_bytes)

    # Receive device 1's public key
    d1_pubkey_bytes = clientsocket.recv(1024)
    d1_pubkey = pickle.loads(d1_pubkey_bytes)

    # Generate the shared key
    d2_sharedkey = d2.gen_shared_key(d1_pubkey)

    print("Shared key:", d2_sharedkey)

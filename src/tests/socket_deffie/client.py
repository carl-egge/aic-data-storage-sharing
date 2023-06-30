#make sure that the server is running at first (server.py)
## The server.py and the client.py should run at the same device because we are using the same IP
#for the server and the client

import socket
import pickle
import pyDH

d1 = pyDH.DiffieHellman()
d1_pubkey = d1.gen_public_key()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

# Send device 1's public key to device 2
d1_pubkey_bytes = pickle.dumps(d1_pubkey)
s.send(d1_pubkey_bytes)

# Receive device 2's public key
d2_pubkey_bytes = s.recv(1024)
d2_pubkey = pickle.loads(d2_pubkey_bytes)

# Generate the shared key
d1_sharedkey = d1.gen_shared_key(d2_pubkey)

print("Shared key:", d1_sharedkey)

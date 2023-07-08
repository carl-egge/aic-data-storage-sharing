#######################    SYMMETRIC ENCRYPTION    ###########################

# This file contains the symmetric encryption and decryption functions. It can
# be used to encrypt and decrypt data with a symmetric key. The key is stored in
# the filesystem.

# imports
import os
from cryptography.fernet import Fernet

# This function generates a new key and stores it in the filesystem
def generate_encryption_key(path):
    encryption_key = Fernet.generate_key()
    string_key = encryption_key.decode()  # Convert bytes to string
    with open(path, "w") as file:
        file.write(string_key)
    return string_key.encode()

# This function reads the key from the filesystem
# If no key exists, a new key is generated
def read_key():
    path = "encryption_key_storage.txt"
    # Check if key exists
    if not os.path.exists(path):
        print("No key found, generating new key...")
        generate_encryption_key(path)
    # Read key from file
    with open(path, "r") as file:
        string_key = file.read()
    return string_key.encode()

# This function encrypts the data with the key and returns
# the encrypted data as a string
def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

# This function decrypts the data with the key and returns
# the decrypted data as a string
def decrypt_data(data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(data)
    return decrypted_data
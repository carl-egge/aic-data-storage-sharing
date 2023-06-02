#######################    SYMMETRIC ENCRYPTION    ###########################

# This file contains the symmetric encryption and decryption functions. It can
# be used to encrypt and decrypt data with a symmetric key. The key is stored in
# the filesystem.

# imports
from cryptography.fernet import Fernet

# This function generates a new key and stores it in the filesystem
def generate_encryption_key():
    encryption_key = Fernet.generate_key()
    encoded_key = encryption_key.decode()  # Convert bytes to string
    with open("../encryption_key_storage.txt", "w") as texttxt:
        texttxt.write(encoded_key)

# This function reads the key from the filesystem
def read_key():
    with open("../encryption_key_storage.txt", "r") as file:
        encoded_key = file.read()
        encryption_key = encoded_key.encode() # Convert string to bytes
    return encryption_key

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
#######################    SYMMETRIC ENCRYPTION    ###########################

# This file contains the symmetric encryption and decryption functions. It can
# be used to encrypt and decrypt data with a symmetric key. The key is stored in
# the filesystem.

# imports
import cryptography
from cryptography.fernet import Fernet

# This function generates a new key and stores it in the filesystem
def generate_key():
    return Fernet.generate_key()

file_path = "../encryption_key_storage.txt"

def write_key():
    with open(file_path, "w") as texttxt:
        texttxt.write(str(generate_key()))

# This function reads the key from the filesystem
def read_key():
    with open(file_path, "r") as file:
        encryption_key = file.read()
    return str(encryption_key)

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
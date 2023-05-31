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

encryption_key = generate_key()

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

# This function reads the key from the filesystem
def read_key():
    print("Not implemented yet!")

 # Encrypt the data
plaintext = "I can encrypt data!"
encrypted_data = encrypt_data(plaintext, encryption_key)
print("Encrypted data:", encrypted_data)

# Decrypt the encrypted data
decrypted_data = decrypt_data(encrypted_data, encryption_key)
print("Decrypted data:", decrypted_data.decode())
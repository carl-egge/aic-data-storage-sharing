#####################  RETRIEVE ENCRYPTED DATA TO STORAGE #########################

# This script connects to the Cloud storage and retrieves the encrypted data. The
# sensor data was stored in a SQL database. The data is decrypted and can then be
# shown to the user. The requirement of the project is that the data can only be
# decrypted on the raspberry pi that uploaded the data because it holds the key.

from storage import DataStorage

print("Hint: This is just a script to retrieve the data from the storage. It is not part of the flask application.")

print("Retrieving encrypted data from storage...\n")

# Initialize DataStorage object
data_storage = DataStorage()

# Retrieve data from storage
data_storage.retrieve_data()

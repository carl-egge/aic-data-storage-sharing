#######################  UPLOAD SENSOR DATA TO STORAGE  ###########################

# This script consumes the data from the grovepi sensors and uploads it to the Cloud
# storage. The data is consumend in user-defined batch sizes. Using a symmetric
# encryption scheme the data is encrypted before it is uploaded to the storage. The 
# data is stored encrypted with little metadata in a SQL database.

from storage import DataStorage

print("Hint: This is just a script to store the data from the storage. It is not part of the flask application.")

print("Retrieving encrypted data from storage...\n")

# Initialize DataStorage object
data_storage = DataStorage()

# Retrieve data from storage
data_storage.store_data()

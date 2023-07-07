#####################  DIFFIE HELLMANN KEY EXCHANGE #########################

# This script is can be run on two raspberry pis to perform the Diffie-Hellman key
# exchange. The shared secret is then used to encrypt the data that is sent to the
# other party. The functionality of this script is implemented in the DataSharing
# class in src/sharing.py

from sharing import DataSharing

print("Hint: This is just a script to test the DH without the UI. It is not part of the flask application.")

print("Starting the Key Exchange...\n")

# Initialize DataSharing object
data_sharing = DataSharing()

# Run the key exchange
data_sharing.run_key_exchange()

data_sharing.share_data()

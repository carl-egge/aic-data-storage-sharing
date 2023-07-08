#####################   SENDER OF SHARING DATA    #############################

# This script is supposed to be started on the raspberry pi that sends the data
# to the other party. The shared secret is used to encrypt the data. This script
# will run the key exchange and then send the data to the other party. The functionality
# of this script is implemented in the DataSharing class in src/sharing.py

from sharing import DataSharing
import time

print("Hint: This is just a script to test the DH without the UI. It is not part of the flask application.")

print("Starting the Key Exchange...\n")

# Initialize DataSharing object
data_sharing = DataSharing()

# Run the key exchange
data_sharing.run_key_exchange()

# Send the data every 5 seconds for 25 seconds
try:
    for i in range(5):
        print("Sending new data batch in 5 seconds...")
        time.sleep(5)
        
        # Send the data
        data_sharing.share_data()
        print("Data sent.\n")

except KeyboardInterrupt:
    print("script stopped by user.")
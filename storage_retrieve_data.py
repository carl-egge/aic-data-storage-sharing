#####################  RETRIEVE ENCRYPTED DATA TO STORAGE #########################

# This script connects to the Cloud storage and retrieves the encrypted data. The
# sensor data was stored in a SQL database. The data is decrypted and can then be
# shown to the user. The requirement of the project is that the data can only be
# decrypted on the raspberry pi that uploaded the data because it holds the key.

# General imports (maybe we don't need all of them)
import os, sys, argparse, time, signal

# Imports for the decryption

# Imports for the database connection

#-------------------------------------------------------------------------------

# This function is called when the script is terminated by the user
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#-------------------------------------------------------------------------------

print('Not implemented yet! Bye!')



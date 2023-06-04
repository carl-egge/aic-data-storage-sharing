#####################  RETRIEVE ENCRYPTED DATA TO STORAGE #########################

# This script connects to the Cloud storage and retrieves the encrypted data. The
# sensor data was stored in a SQL database. The data is decrypted and can then be
# shown to the user. The requirement of the project is that the data can only be
# decrypted on the raspberry pi that uploaded the data because it holds the key.

# General imports (maybe we don't need all of them)
import sys, signal

import sqlalchemy

# local imports
from encryption.symmetric import decrypt_data, read_key
from gcp.get_sql_connection import getconn

#-------------------------------------------------------------------------------

# This function is called when the script is terminated by the user
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#-------------------------------------------------------------------------------

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

# connect to connection pool
with pool.connect() as db_conn:
  # query and fetch test table
  results = db_conn.execute(sqlalchemy.text("SELECT * FROM sensors_data")).fetchall()

  # show results
  #for row in results:
    # decrypt data
   # decrypt_data = decrypt_data(row[1], read_key())

    #print(f"Decrypted data: {decrypt_data}\n")
    # show results
  last_row = results[-1]
  token = last_row[1].encode()  # Convert token to bytes

  decrypt_data = decrypt_data(token, read_key())
  print(f"Decrypted data: {decrypt_data}\n")
#########################   DATA STORAGE CLASS   #############################

# Import libraries
import sqlalchemy

from encryption.symmetric import decrypt_data, read_key, encrypt_data, generate_encryption_key
from gcp.get_sql_connection import getconn

# TODO: Change this import to the real sensor data consumption if working on the pi:
from sensor.sensors import one_sensor_data_readout, sensor_data_readout
# from sensor.fakesensors import one_sensor_data_readout


class DataStorage:
    '''
    This class implements the functionality for the data storage system of the project.
    It is used to connect to the Google Cloud SQL database instance and to store 
    and retrieve data from the sensors. The data is symmetrically encrypted.
    '''

    sym_key = ''

    def __init__(self, batch_size = 1):
        '''
        Constructor for the DataStorage class
        This runs every time a new object is created
        '''
        # Set batch size
        self.batch_size = batch_size
        # Read encryption key
        self.sym_key = read_key()
        print("DataStorage object created with symmetric key: ", self.sym_key)

    # ------------------------------------------------------------------------------------------
    def store_data(self, sensor_data=None):
        '''
        This function consumes the data from the grovepi sensors and uploads it to the Cloud
        storage. The data is consumend in user-defined batch sizes. Using a symmetric
        encryption scheme the data is encrypted before it is uploaded to the storage. The 
        data is stored encrypted with little metadata in a SQL database.
        '''

        # Grovepi sensor data consumption
        if sensor_data is None:
            print("Consuming data from sensors...")
            data = sensor_data_readout(self.batch_size)
        else:
            data = sensor_data

        # Call encryption function
        print("Encrypting data...")
        encrypted_data = encrypt_data(str(data), self.sym_key)

        # Test print statements
        # print(f"data: {str(data)}\n")
        # print(f"data after encrypting: {encrypted_data}\n")        

        # Upload data to cloud storage
        print("Uploading data to cloud storage...")
        # create connection pool
        pool = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
        )

        # connect to connection pool
        with pool.connect() as db_conn:
            # create table if not exists
            db_conn.execute(
                sqlalchemy.text(
                    "CREATE TABLE IF NOT EXISTS sensors_data "
                    "( id SERIAL NOT NULL, encrypted_data VARCHAR(2550) NOT NULL, "
                    "PRIMARY KEY (id));"
                )
            )
            db_conn.commit()

            # insert data into our ratings table
            insert_stmt = sqlalchemy.text(
                "INSERT INTO sensors_data (encrypted_data) VALUES (:encrypted_data)",
            )

            # insert entries into table
            db_conn.execute(insert_stmt, parameters={"encrypted_data": encrypted_data})

            # commit transactions
            db_conn.commit() 

        print("Success! One Data Entry uploaded to cloud storage!")

        return encrypted_data


    # ------------------------------------------------------------------------------------------
    def retrieve_data(self):
        '''
        This function connects to the Cloud storage and retrieves the encrypted data. The
        sensor data was stored in a SQL database. The data is decrypted and can then be
        shown to the user. The requirement of the project is that the data can only be
        decrypted on the raspberry pi that uploaded the data because it holds the key.
        '''

        # create connection pool
        pool = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
        )

        # connect to connection pool
        with pool.connect() as db_conn:
            # query and fetch test table
            results = db_conn.execute(sqlalchemy.text("SELECT * FROM sensors_data")).fetchall()

        # Show all results
        # for row in results:
            # decrypt data
        # decrypt_data = decrypt_data(row[1], read_key())
        #print(f"Decrypted data: {decrypt_data}\n")
            
        # Show Last Element from results
        last_row = results[-1]
        # Convert token to bytes
        token = last_row[1].encode()
        print(f"data: {token}\n")
        decrypted_data = decrypt_data(token, read_key())
        print(f"Decrypted data: {decrypted_data}\n")

        return decrypted_data

    # ------------------------------------------------------------------------------------------
    def generate_sym_key(self):
        '''
        This function generates a new symmetric key and stores it in the filesystem.
        '''
        self.sym_key = generate_encryption_key("encryption_key_storage.txt")
        print("New symmetric key generated: ", self.sym_key)
        return self.sym_key

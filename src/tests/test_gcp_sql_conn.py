#########################   TEST GCP SQL CONNECTION   #############################

# Source
# - https://dev.to/gabrielosluz/get-data-from-cloud-sql-with-python-51jm
# - https://cloud.google.com/blog/topics/developers-practitioners/how-connect-cloud-sql-using-python-easy-way?hl=en
# - https://github.com/GoogleCloudPlatform/cloud-sql-python-connector

# This file is just to establish and test the connection to the GCP SQL database.
# The credentials are in the .env file and correspond to the test-db instance on the
# data-storage project. The database is empty and we can use it to test the connection.

import os, sys
from google.cloud.sql.connector import Connector
import sqlalchemy
from dotenv import load_dotenv

# GCP IAM authentication using service account key
# How to create a service account key: https://cloud.google.com/iam/docs/keys-create-delete?hl=de#iam-service-account-keys-create-console
# Alternatively you can authenticate using the Google Cloud SDK.
credential_path = "/home/pi/aic/gcp_key/aic23-groupb1-data-storage-4f89199ed283.json" # IMPORTANT: Change this to your own path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# set config
load_dotenv()

project_id = os.getenv("project_id")
region = os.getenv("region")
instance_name = os.getenv("instance_name")
db_user = os.getenv("db_user")
db_pass = os.getenv("db_pass")
db_name = os.getenv("db_name")

print("DB: ", db_name)

# initialize parameters
INSTANCE_CONNECTION_NAME = "%s:%s:%s" % (project_id, region, instance_name)
print("Your instance connection name is: ", INSTANCE_CONNECTION_NAME)

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=db_user,
        password=db_pass,
        db=db_name
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)


# connect to connection pool
with pool.connect() as db_conn:
  # create ratings table in our sandwiches database
  db_conn.execute(
    sqlalchemy.text(
      "CREATE TABLE IF NOT EXISTS ratings "
      "( id SERIAL NOT NULL, name VARCHAR(255) NOT NULL, "
      "origin VARCHAR(255) NOT NULL, rating FLOAT NOT NULL, "
      "PRIMARY KEY (id));"
    )
  )

  # commit transaction (SQLAlchemy v2.X.X is commit as you go)
  db_conn.commit()

  # insert data into our ratings table
  insert_stmt = sqlalchemy.text(
      "INSERT INTO ratings (name, origin, rating) VALUES (:name, :origin, :rating)",
  )

  # insert entries into table
  db_conn.execute(insert_stmt, parameters={"name": "HOTDOG", "origin": "Germany", "rating": 7.5})
  db_conn.execute(insert_stmt, parameters={"name": "BANH MI", "origin": "Vietnam", "rating": 9.1})
  db_conn.execute(insert_stmt, parameters={"name": "CROQUE MADAME", "origin": "France", "rating": 8.3})

  # commit transactions
  db_conn.commit()

  # query and fetch ratings table
  results = db_conn.execute(sqlalchemy.text("SELECT * FROM ratings")).fetchall()

  # show results
  for row in results:
    print(row)

#########################     GCP SQL CONNECTION   #############################

# This file is just to establish and the connection to the GCP SQL database.
# The credentials are in the .env file and correspond to the test-db instance on the
# data-storage project.

import os, sys
from google.cloud.sql.connector import Connector
import sqlalchemy
import configparser

# GCP IAM authentication using service account key
# TODO: In order for this script to work you need to create a service account key, store the JSON and update the path below!
# How to create a service account key: https://cloud.google.com/iam/docs/keys-create-delete?hl=de#iam-service-account-keys-create-console
# Alternatively you can authenticate using the Google Cloud SDK.
credential_path = "/home/carl-egge/aic/aic23-groupb1-data-storage-4f89199ed283.json" # IMPORTANT: Change this to your own path
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# set config
# TODO: The .env file with the database credentials is needed for this to work.
parser = configparser.ConfigParser()
parser.read(".env")

project_id = parser.get("DEFAULT", "project_id")
region = parser.get("DEFAULT", "region")
instance_name = parser.get("DEFAULT", "instance_name")
db_user = parser.get("DEFAULT", "db_user")
db_pass = parser.get("DEFAULT", "db_pass")
db_name = parser.get("DEFAULT", "db_name")

# initialize parameters
INSTANCE_CONNECTION_NAME = f"{project_id}:{region}:{instance_name}"
print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")

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
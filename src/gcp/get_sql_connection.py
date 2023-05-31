#########################     GCP SQL CONNECTION   #############################

# This file is just to establish and the connection to the GCP SQL database.
# The credentials are in the .env file and correspond to the test-db instance on the
# data-storage project.

import os, sys
from google.cloud.sql.connector import Connector
import sqlalchemy
from dotenv import load_dotenv


# function to return the database connection
def getconn():

	# GCP IAM authentication using service account key
	# In order for this script to work you need to create a service account key, store the JSON and update the path below!
	# How to create a service account key: https://cloud.google.com/iam/docs/keys-create-delete?hl=de#iam-service-account-keys-create-console
	# Alternatively you can authenticate using the Google Cloud SDK.
	credential_path = "/home/pi/aic/gcp_key/aic23-groupb1-data-storage-4f89199ed283.json" # IMPORTANT: Change this to your own path
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

	# set config
	# The .env file with the database credentials is needed for this to work.
	load_dotenv()

	project_id = os.getenv("project_id")
	region = os.getenv("region")
	instance_name = os.getenv("instance_name")
	db_user = os.getenv("db_user")
	db_pass = os.getenv("db_pass")
	db_name = os.get("db_name")

	# initialize parameters
	INSTANCE_CONNECTION_NAME = f"{project_id}:{region}:{instance_name}"
	print(f"Your instance connection name is: {INSTANCE_CONNECTION_NAME}")

	# initialize Connector object
	connector = Connector()

	# Establish connection
	conn = connector.connect(
		INSTANCE_CONNECTION_NAME,
		"pymysql",
		user=db_user,
		password=db_pass,
		db=db_name
	)
	return conn

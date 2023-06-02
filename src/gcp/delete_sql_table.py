########################   Delete SQL table    ###############################

# This is a helper script that delete the sensors_data table from the database.
# During testing we need to delete the table to avoid duplicate entries.

import sqlalchemy
from get_sql_connection import getconn

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
            "DROP TABLE sensors_data;"
        )
    )

    db_conn.commit()

print("Success! The 'sensors_data' table was dropped!")
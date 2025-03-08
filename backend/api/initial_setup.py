import os
from .utils import get_db_last_modified_time

DB_PATH = 'backend/db.sqlite3'
TIMESTAMP_PATH = 'backend/api/db_timestamp.txt'

def initial_setup():
    current_timestamp = get_db_last_modified_time(DB_PATH)
    with open(TIMESTAMP_PATH, 'w') as timestamp_file:
        timestamp_file.write(str(current_timestamp))

if __name__ == '__main__':
    initial_setup()
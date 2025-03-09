import os
from .utils import get_db_last_modified_time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
TIMESTAMP_PATH = os.path.join(BASE_DIR, 'api', 'db_timestamp.txt')

def initial_setup():
    current_timestamp = get_db_last_modified_time(DB_PATH)
    with open(TIMESTAMP_PATH, 'w') as timestamp_file:
        timestamp_file.write(str(current_timestamp))

if __name__ == '__main__':
    initial_setup()
import os

def get_db_last_modified_time(db_path):
    return os.path.getmtime(db_path)
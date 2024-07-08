import pymysql
import os
from pymysql import cursors

def get_db_connection():
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    db = os.getenv('MYSQL_DB')
    
    if None in [host, user, password, db]:
        raise ValueError('MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DB must be set in the environment')
    
    return pymysql.connect(
        host=host,
        user=user,
        password=password, # type: ignore
        db=db,
        cursorclass=cursors.DictCursor
    ) # type: ignore
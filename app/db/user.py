from db.connection import get_db_connection

def find_user(email: str, password: str):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        return cursor.fetchone()